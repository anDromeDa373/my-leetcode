#include <dirent.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>

#define MAX_FILE_SIZE (256 * 1024)
#define MAX_HISTORY 1024

typedef struct {
    char date[32];
    char result[8];
    char memo[512];
} HistoryEntry;

typedef struct {
    char id[64];
    char title[256];
    char url[512];
    char difficulty[32];
    int points;
    long last_attempt;
    HistoryEntry history[MAX_HISTORY];
    int history_count;
} ProblemStatus;

static char repo_root[PATH_MAX];

static int is_dir(const char *path) {
    struct stat st;
    return stat(path, &st) == 0 && S_ISDIR(st.st_mode);
}

static int find_repo_root(void) {
    char path[PATH_MAX];
    if (!getcwd(path, sizeof(path))) {
        return -1;
    }

    for (int depth = 0; depth < 20; depth++) {
        char test[PATH_MAX];
        snprintf(test, sizeof(test), "%s/src", path);
        if (is_dir(test)) {
            strncpy(repo_root, path, sizeof(repo_root) - 1);
            repo_root[sizeof(repo_root) - 1] = '\0';
            return 0;
        }

        char *slash = strrchr(path, '/');
        if (!slash || (slash == path && path[1] == '\0')) {
            break;
        }
        if (slash == path) {
            *slash = '\0';
        } else {
            *slash = '\0';
        }
    }

    return -1;
}

static char *read_file(const char *path, size_t *out_len) {
    FILE *fp = fopen(path, "rb");
    if (!fp) {
        return NULL;
    }

    if (fseek(fp, 0, SEEK_END) != 0) {
        fclose(fp);
        return NULL;
    }

    long size = ftell(fp);
    if (size < 0) {
        fclose(fp);
        return NULL;
    }

    if (fseek(fp, 0, SEEK_SET) != 0) {
        fclose(fp);
        return NULL;
    }

    char *buf = malloc((size_t)size + 1);
    if (!buf) {
        fclose(fp);
        return NULL;
    }

    size_t read = fread(buf, 1, (size_t)size, fp);
    fclose(fp);
    buf[read] = '\0';
    if (out_len) {
        *out_len = read;
    }
    return buf;
}

static int write_file(const char *path, const char *content) {
    FILE *fp = fopen(path, "wb");
    if (!fp) {
        return -1;
    }
    if (fputs(content, fp) == EOF) {
        fclose(fp);
        return -1;
    }
    fclose(fp);
    return 0;
}

static const char *skip_ws(const char *p) {
    while (*p && (*p == ' ' || *p == '\t' || *p == '\n' || *p == '\r')) {
        p++;
    }
    return p;
}

static int parse_json_string(const char *json, const char *key, char *out, size_t out_size) {
    char pattern[128];
    snprintf(pattern, sizeof(pattern), "\"%s\"", key);
    const char *pos = strstr(json, pattern);
    if (!pos) {
        return -1;
    }

    pos = strchr(pos + strlen(pattern), ':');
    if (!pos) {
        return -1;
    }
    pos = skip_ws(pos + 1);
    if (*pos != '"') {
        return -1;
    }
    pos++;

    size_t i = 0;
    while (*pos && *pos != '"' && i + 1 < out_size) {
        if (*pos == '\\' && pos[1]) {
            pos++;
            switch (*pos) {
            case 'n':
                out[i++] = '\n';
                break;
            case 'r':
                out[i++] = '\r';
                break;
            case 't':
                out[i++] = '\t';
                break;
            case '"':
            case '\\':
                out[i++] = *pos;
                break;
            default:
                out[i++] = *pos;
                break;
            }
        } else {
            out[i++] = *pos;
        }
        pos++;
    }
    out[i] = '\0';
    return 0;
}

static int parse_json_int(const char *json, const char *key, long *out) {
    char pattern[128];
    snprintf(pattern, sizeof(pattern), "\"%s\"", key);
    const char *pos = strstr(json, pattern);
    if (!pos) {
        return -1;
    }

    pos = strchr(pos + strlen(pattern), ':');
    if (!pos) {
        return -1;
    }
    pos = skip_ws(pos + 1);

    if (*pos == '"') {
        pos++;
        char buf[64];
        size_t i = 0;
        while (*pos && *pos != '"' && i + 1 < sizeof(buf)) {
            buf[i++] = *pos++;
        }
        buf[i] = '\0';
        if (buf[0] == '\0') {
            *out = 0;
            return 0;
        }
        char *end = NULL;
        *out = strtol(buf, &end, 10);
        return (end && *end == '\0') ? 0 : -1;
    }

    char *end = NULL;
    *out = strtol(pos, &end, 10);
    return end ? 0 : -1;
}

static void json_escape(const char *src, char *dst, size_t dst_size) {
    size_t j = 0;
    for (size_t i = 0; src[i] && j + 2 < dst_size; i++) {
        char c = src[i];
        if (c == '"' || c == '\\') {
            dst[j++] = '\\';
            dst[j++] = c;
        } else if (c == '\n') {
            dst[j++] = '\\';
            dst[j++] = 'n';
        } else if (c == '\r') {
            dst[j++] = '\\';
            dst[j++] = 'r';
        } else if (c == '\t') {
            dst[j++] = '\\';
            dst[j++] = 't';
        } else {
            dst[j++] = c;
        }
    }
    dst[j] = '\0';
}

static void shell_escape(const char *src, char *dst, size_t dst_size) {
    size_t j = 0;
    for (size_t i = 0; src[i] && j + 2 < dst_size; i++) {
        char c = src[i];
        if (c == '"' || c == '\\' || c == '$' || c == '`') {
            dst[j++] = '\\';
        }
        dst[j++] = c;
    }
    dst[j] = '\0';
}

static int parse_history(const char *json, ProblemStatus *status) {
    const char *hist = strstr(json, "\"history\"");
    if (!hist) {
        status->history_count = 0;
        return 0;
    }

    hist = strchr(hist, '[');
    if (!hist) {
        status->history_count = 0;
        return 0;
    }
    hist++;

    status->history_count = 0;
    while (*hist && *hist != ']') {
        hist = skip_ws(hist);
        if (*hist == ']') {
            break;
        }
        if (*hist != '{') {
            hist++;
            continue;
        }

        const char *obj_end = strchr(hist, '}');
        if (!obj_end) {
            break;
        }

        size_t obj_len = (size_t)(obj_end - hist + 1);
        char obj_buf[1024];
        if (obj_len >= sizeof(obj_buf)) {
            return -1;
        }
        memcpy(obj_buf, hist, obj_len);
        obj_buf[obj_len] = '\0';

        if (status->history_count >= MAX_HISTORY) {
            return -1;
        }

        HistoryEntry *entry = &status->history[status->history_count];
        if (parse_json_string(obj_buf, "date", entry->date, sizeof(entry->date)) != 0 ||
            parse_json_string(obj_buf, "result", entry->result, sizeof(entry->result)) != 0 ||
            parse_json_string(obj_buf, "memo", entry->memo, sizeof(entry->memo)) != 0) {
            return -1;
        }
        status->history_count++;
        hist = obj_end + 1;
        hist = skip_ws(hist);
        if (*hist == ',') {
            hist++;
        }
    }

    return 0;
}

static int load_status(const char *path, ProblemStatus *status) {
    char *json = read_file(path, NULL);
    if (!json) {
        return -1;
    }

    memset(status, 0, sizeof(*status));
    if (parse_json_string(json, "id", status->id, sizeof(status->id)) != 0 ||
        parse_json_string(json, "title", status->title, sizeof(status->title)) != 0 ||
        parse_json_string(json, "url", status->url, sizeof(status->url)) != 0 ||
        parse_json_string(json, "difficulty", status->difficulty, sizeof(status->difficulty)) != 0) {
        free(json);
        return -1;
    }

    long value = 0;
    if (parse_json_int(json, "points", &value) == 0) {
        status->points = (int)value;
    } else if (parse_json_int(json, "count", &value) == 0) {
        status->points = (int)value;
    } else {
        status->points = 0;
    }

    if (parse_json_int(json, "last_attempt", &value) == 0) {
        status->last_attempt = value;
    } else if (parse_json_int(json, "last_cleared", &value) == 0) {
        status->last_attempt = value;
    } else {
        status->last_attempt = 0;
    }

    if (parse_history(json, status) != 0) {
        free(json);
        return -1;
    }

    free(json);
    return 0;
}

static int serialize_status(const ProblemStatus *status, char *out, size_t out_size) {
    char esc_id[128], esc_title[512], esc_url[1024], esc_difficulty[64];
    json_escape(status->id, esc_id, sizeof(esc_id));
    json_escape(status->title, esc_title, sizeof(esc_title));
    json_escape(status->url, esc_url, sizeof(esc_url));
    json_escape(status->difficulty, esc_difficulty, sizeof(esc_difficulty));

    int written = snprintf(
        out,
        out_size,
        "{\n"
        "  \"id\": \"%s\",\n"
        "  \"title\": \"%s\",\n"
        "  \"url\": \"%s\",\n"
        "  \"difficulty\": \"%s\",\n"
        "  \"points\": %d,\n"
        "  \"last_attempt\": %ld,\n"
        "  \"history\": [\n",
        esc_id,
        esc_title,
        esc_url,
        esc_difficulty,
        status->points,
        status->last_attempt);

    if (written < 0 || (size_t)written >= out_size) {
        return -1;
    }

    size_t offset = (size_t)written;
    for (int i = 0; i < status->history_count; i++) {
        char esc_date[64], esc_result[32], esc_memo[1024];
        json_escape(status->history[i].date, esc_date, sizeof(esc_date));
        json_escape(status->history[i].result, esc_result, sizeof(esc_result));
        json_escape(status->history[i].memo, esc_memo, sizeof(esc_memo));

        written = snprintf(
            out + offset,
            out_size - offset,
            "    {\n"
            "      \"date\": \"%s\",\n"
            "      \"result\": \"%s\",\n"
            "      \"memo\": \"%s\"\n"
            "    }%s\n",
            esc_date,
            esc_result,
            esc_memo,
            (i + 1 < status->history_count) ? "," : "");

        if (written < 0 || (size_t)written >= out_size - offset) {
            return -1;
        }
        offset += (size_t)written;
    }

    written = snprintf(out + offset, out_size - offset, "  ]\n}\n");
    if (written < 0 || (size_t)written >= out_size - offset) {
        return -1;
    }

    return 0;
}

static int save_status(const char *path, const ProblemStatus *status) {
    char *buf = malloc(MAX_FILE_SIZE);
    if (!buf) {
        return -1;
    }

    if (serialize_status(status, buf, MAX_FILE_SIZE) != 0) {
        free(buf);
        return -1;
    }

    int rc = write_file(path, buf);
    free(buf);
    return rc;
}

static int append_notes(const char *id, const char *datetime, const char *result, const char *memo) {
    char path[PATH_MAX];
    snprintf(path, sizeof(path), "%s/src/%s/NOTES.md", repo_root, id);

    FILE *fp = fopen(path, "a");
    if (!fp) {
        fp = fopen(path, "w");
        if (!fp) {
            return -1;
        }
        fprintf(
            fp,
            "# %s\n\n"
            "## lct log\n\n",
            id);
    }

    fprintf(fp, "- %s [%s] %s\n", datetime, result, memo);
    fclose(fp);
    return 0;
}

static int build_summary(void) {
    char src_path[PATH_MAX];
    snprintf(src_path, sizeof(src_path), "%s/src", repo_root);

    DIR *dir = opendir(src_path);
    if (!dir) {
        return -1;
    }

    char *summary = malloc(MAX_FILE_SIZE);
    if (!summary) {
        closedir(dir);
        return -1;
    }

    long updated_at = (long)time(NULL);
    size_t offset = (size_t)snprintf(
        summary,
        MAX_FILE_SIZE,
        "{\n"
        "  \"updated_at\": %ld,\n"
        "  \"problems\": [\n",
        updated_at);

    int first = 1;
    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_name[0] == '.') {
            continue;
        }

        char problem_dir[PATH_MAX];
        snprintf(problem_dir, sizeof(problem_dir), "%s/%s", src_path, entry->d_name);
        if (!is_dir(problem_dir)) {
            continue;
        }

        char status_path[PATH_MAX];
        snprintf(status_path, sizeof(status_path), "%s/status.json", problem_dir);
        if (access(status_path, R_OK) != 0) {
            continue;
        }

        char *status_json = read_file(status_path, NULL);
        if (!status_json) {
            continue;
        }

        if (!first) {
            if (offset + 2 >= MAX_FILE_SIZE) {
                free(status_json);
                free(summary);
                closedir(dir);
                return -1;
            }
            summary[offset++] = ',';
            summary[offset++] = '\n';
            summary[offset] = '\0';
        }
        first = 0;

        size_t json_len = strlen(status_json);
        while (json_len > 0 && (status_json[json_len - 1] == '\n' || status_json[json_len - 1] == '\r')) {
            status_json[--json_len] = '\0';
        }

        if (offset + json_len + 16 >= MAX_FILE_SIZE) {
            free(status_json);
            free(summary);
            closedir(dir);
            return -1;
        }

        summary[offset++] = ' ';
        summary[offset++] = ' ';
        summary[offset++] = ' ';
        summary[offset++] = ' ';
        memcpy(summary + offset, status_json, json_len);
        offset += json_len;
        summary[offset] = '\0';
        free(status_json);
    }
    closedir(dir);

    if (offset + 16 >= MAX_FILE_SIZE) {
        free(summary);
        return -1;
    }

    snprintf(summary + offset, MAX_FILE_SIZE - offset, "\n  ]\n}\n");

    char summary_path[PATH_MAX];
    snprintf(summary_path, sizeof(summary_path), "%s/summary.json", repo_root);
    int rc = write_file(summary_path, summary);
    free(summary);
    if (rc != 0) {
        return -1;
    }

    char web_summary_path[PATH_MAX];
    snprintf(web_summary_path, sizeof(web_summary_path), "%s/web/public/summary.json", repo_root);
    char copy_cmd[PATH_MAX * 2];
    snprintf(copy_cmd, sizeof(copy_cmd), "cp \"%s\" \"%s\"", summary_path, web_summary_path);
    if (system(copy_cmd) != 0) {
        fprintf(stderr, "warning: failed to copy summary.json to web/public/\n");
    }

    return 0;
}

static int run_git_commit(const char *result, const char *id, const char *memo) {
    char escaped_memo[1024];
    shell_escape(memo, escaped_memo, sizeof(escaped_memo));

    char cmd[PATH_MAX + 1024];
    snprintf(cmd, sizeof(cmd), "cd \"%s\" && git add .", repo_root);
    if (system(cmd) != 0) {
        fprintf(stderr, "warning: git add failed\n");
    }

    snprintf(
        cmd,
        sizeof(cmd),
        "cd \"%s\" && git commit -m \"lct(%s): %s - %s\"",
        repo_root,
        result,
        id,
        escaped_memo);
    if (system(cmd) != 0) {
        fprintf(stderr, "warning: git commit failed (no changes or git error)\n");
    }

    return 0;
}

static void usage(const char *prog) {
    fprintf(stderr, "Usage:\n");
    fprintf(stderr, "  %s ok <id> \"<memo>\"\n", prog);
    fprintf(stderr, "  %s no <id> \"<memo>\"\n", prog);
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        usage(argv[0]);
        return 1;
    }

    const char *result = argv[1];
    const char *id = argv[2];
    const char *memo = argv[3];

    if (strcmp(result, "ok") != 0 && strcmp(result, "no") != 0) {
        fprintf(stderr, "error: result must be 'ok' or 'no'\n");
        usage(argv[0]);
        return 1;
    }

    if (find_repo_root() != 0) {
        fprintf(stderr, "error: could not find repository root (missing src/)\n");
        return 1;
    }

    char status_path[PATH_MAX];
    snprintf(status_path, sizeof(status_path), "%s/src/%s/status.json", repo_root, id);
    if (access(status_path, R_OK | W_OK) != 0) {
        fprintf(stderr, "error: status file not found or not writable: %s\n", status_path);
        return 1;
    }

    ProblemStatus status;
    if (load_status(status_path, &status) != 0) {
        fprintf(stderr, "error: failed to parse %s\n", status_path);
        return 1;
    }

    time_t now = time(NULL);
    struct tm *tm_info = localtime(&now);
    char date_str[32];
    char datetime_str[64];
    strftime(date_str, sizeof(date_str), "%Y-%m-%d", tm_info);
    strftime(datetime_str, sizeof(datetime_str), "%Y-%m-%d %H:%M:%S", tm_info);

    status.last_attempt = (long)now;
    if (strcmp(result, "ok") == 0) {
        status.points += 1;
    } else {
        status.points -= 1;
    }

    if (status.history_count >= MAX_HISTORY) {
        fprintf(stderr, "error: history limit reached\n");
        return 1;
    }

    HistoryEntry *entry = &status.history[status.history_count++];
    strncpy(entry->date, date_str, sizeof(entry->date) - 1);
    strncpy(entry->result, result, sizeof(entry->result) - 1);
    strncpy(entry->memo, memo, sizeof(entry->memo) - 1);

    if (save_status(status_path, &status) != 0) {
        fprintf(stderr, "error: failed to write %s\n", status_path);
        return 1;
    }

    if (append_notes(id, datetime_str, result, memo) != 0) {
        fprintf(stderr, "error: failed to append NOTES.md for %s\n", id);
        return 1;
    }

    if (build_summary() != 0) {
        fprintf(stderr, "error: failed to build summary.json\n");
        return 1;
    }

    run_git_commit(result, id, memo);

    printf(
        "updated %s: points=%d last_attempt=%ld result=%s\n",
        id,
        status.points,
        status.last_attempt,
        result);
    return 0;
}
