const NC_ID_PATTERN = /^nc\d{3}$/

export function normalizeProblems(raw) {
  if (!Array.isArray(raw)) {
    return []
  }

  return raw
    .filter((problem) => problem && typeof problem === 'object' && NC_ID_PATTERN.test(String(problem.id ?? '')))
    .map((problem) => ({
      id: String(problem.id),
      title: String(problem.title ?? ''),
      url: String(problem.url ?? ''),
      points: Number(problem.points ?? 0),
      last_attempt:
        problem.last_attempt == null || problem.last_attempt === ''
          ? null
          : Number(problem.last_attempt),
    }))
    .sort((a, b) => a.id.localeCompare(b.id, undefined, { numeric: true }))
    .slice(0, 150)
}

export function parseSummary(data) {
  if (!data || typeof data !== 'object') {
    throw new Error('summary.json の形式が不正です')
  }

  const problems = normalizeProblems(data.problems)
  if (problems.length === 0) {
    throw new Error(
      'summary.json に nc001〜nc150 の問題データがありません。lct を実行するか summary.json を再生成してください。',
    )
  }

  return {
    updatedAt:
      data.updated_at == null || data.updated_at === ''
        ? null
        : Number(data.updated_at),
    problems,
  }
}

export async function fetchSummary() {
  const url = `${import.meta.env.BASE_URL}summary.json`
  const res = await fetch(url, { cache: 'no-store' })

  if (!res.ok) {
    throw new Error(`summary.json の読み込みに失敗しました (HTTP ${res.status})`)
  }

  let data
  try {
    data = await res.json()
  } catch {
    throw new Error('summary.json の JSON パースに失敗しました')
  }

  return parseSummary(data)
}
