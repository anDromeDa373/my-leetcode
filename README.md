# my-leetcode

LeetCode 周回によるアルゴリズム体力の強化を目的とした個人演習リポジトリです。

## 目的

- 定番問題を繰り返し解き、実装速度と思考の型を身につける
- 解法・計算量・思考プロセスを記録し、面接対策に再利用できる形で蓄積する
- ターミナルでの移動を最優先し、`ex0001` のような短いフォルダ名で問題を管理する

## ディレクトリ構成

```
src/
  ex0001/
    solutions.cpp   # 解答コード
    NOTES.md        # 面接対策用メモ
    status.json     # 進捗管理用メタデータ
```

## ロードマップ

### Phase 1: 問題集の管理（現在）

- 問題ごとに `src/exNNNN/` フォルダを追加
- `solutions.cpp` / `NOTES.md` / `status.json` のテンプレートを揃える
- 周回回数や最終クリア日時を `status.json` に記録

### Phase 2: progress-tracker の開発（予定）

- 全問題の `status.json` を集約し、グリッド（表）で進捗を可視化
- 難易度・周回回数・最終クリア日時などを一覧表示
- 未着手・要復習・オールグリーン達成状況を一目で把握できる管理ツールを同一リポジトリ内に構築

## 使い方（暫定）

```bash
cd src/ex0001
# solutions.cpp を編集して解答
# NOTES.md に解法メモを記録
# クリア後、status.json の count / last_cleared を更新
```
