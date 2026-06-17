# my-leetcode

NeetCode 150 を軸にした LeetCode 周回・進捗管理リポジトリです。  
C++ と CLI ツールだけで完結し、Web ダッシュボードは Vercel へのデプロイ専用です。

## 目的

- NeetCode 150 を繰り返し解き、アルゴリズム実装の速度と型を身につける
- 解法・計算量・つまずきポイントを `NOTES.md` に蓄積する
- `lct` CLI で進捗を記録し、Vercel 上のダッシュボードで可視化する

## プロジェクト構成

```
my-leetcode/
├── src/           # 問題フォルダ（nc001〜nc150）
├── cli/           # lct CLI のソース（C）
├── lct            # 進捗記録 CLI（ルートから実行）
├── web/           # ダッシュボード（Vercel デプロイ専用）
├── summary.json   # 全問題の進捗サマリー（lct が生成）
└── Makefile       # C++ 解答のコンパイル・実行
```

### 問題フォルダ（`src/ncXXX/`）

```
src/
  nc001/
    sol1.cpp       # 解答コード
    NOTES.md       # 解法メモ
    status.json    # 進捗メタデータ
```

## クイックスタート

### 1. C++ 解答の実行

```bash
make 001/sol1   # src/nc001/sol1.cpp をコンパイル・実行
```

`find` で ID を含むディレクトリを自動検索し、実行後にバイナリを削除します。

### 2. 進捗の記録（lct）

```bash
cd cli && make          # 初回のみ: ルートに lct をビルド

./lct ok 001 "O(N)で解けた"
./lct no 001 "セグフォした"
```

`001` と入力するだけで `nc001` を自動特定します（`nc001` の明示指定も可）。  
リポジトリルートからそのまま実行できます。

`lct` は以下を自動で行います。

- `src/ncXXX/status.json` の更新（`points` / `last_attempt` / `history`）
- `src/ncXXX/NOTES.md` へのログ追記
- ルート `summary.json` の再生成
- `web/public/summary.json` への同期
- `git add .` と `git commit`

### 3. lct のビルド

```bash
cd cli && make
```

## points とタイルの色

| points | 意味 |
|--------|------|
| ≥ 3 | マスター（ゴールド） |
| 2 | 安定して解ける |
| 1 | 一度は解けた |
| 0 | 未着手 |
| -1 | 直近で失敗 |
| ≤ -2 | 要復習 |

## ツール一覧

| ツール | 説明 |
|--------|------|
| `lct` | 進捗記録 CLI（`./lct ok 001 "memo"`） |
| `Makefile` | `make 001/sol1` で C++ 実行 |
| `web/` | Vercel 公開用ダッシュボード |

## Vercel デプロイ

ローカルでの `npm run dev` は行いません。`lct` で進捗を更新したあと、Vercel がビルド・公開します。

### Vercel 設定

| 項目 | 値 |
|------|-----|
| Root Directory | `web` |
| Build Command | `npm run build` |
| Output Directory | `dist` |

### フロー

1. 問題を解く → `make 001/sol1`
2. 進捗を記録 → `./lct ok 001 "メモ"`
3. `lct` が `summary.json` と `web/public/summary.json` を更新し git commit
4. Vercel が自動デプロイ → ダッシュボードに反映

`prebuild` 時にルートの `summary.json` が `web/public/` へコピーされます。  
Vercel の Root Directory を `web` に設定している場合、リポジトリ全体が clone されるため `../summary.json` が参照できます。
