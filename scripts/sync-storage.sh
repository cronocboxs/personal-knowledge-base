#!/usr/bin/env bash
# scripts/sync-storage.sh
# 06-storage/ の大容量バイナリを Google Drive へ追記転送（上書き・削除なし）

set -e

# 設定
LOCAL_DIR="./06-storage"
RCLONE_REMOTE="gdrive:pkm-storage" # rclone config で設定したリモート名:フォルダ名

echo "🚀 Google Drive への転送を開始します: ${LOCAL_DIR} -> ${RCLONE_REMOTE}"

# rclone copy 実行
# --ignore-existing : 既存ファイルを絶対上書きしない
# -P                : 進捗状況を表示
rclone copy "${LOCAL_DIR}" "${RCLONE_REMOTE}" \
  --ignore-existing \
  -P

echo "✅ 転送完了（上書き・削除なしの追記同期が成功しました）"