#!/usr/bin/env bash
# scripts/check-structure.sh
# 規約遵守チェックスクリプト（個人情報・日付・URL等のリーク検証およびGit管理設定確認）

set -e

TARGET_DIRS=("02-knowledge" "03-output" "00-rules" ".agents")
ERRORS_FOUND=0

echo "🔍 構造・サニタイズ・Git設定のチェックを開始します..."

# --------------------------------------------------
# A. Git管理・ignore設定チェック
# --------------------------------------------------

# 1. 01-private/ の追跡ファイルチェック (.gitkeep 以外は追跡禁止)
PRIVATE_TRACKED=$(git ls-files 01-private/ | grep -v '\.gitkeep$' || true)
if [ -n "$PRIVATE_TRACKED" ]; then
  echo -e "\n❌ 01-private/ 内に .gitkeep 以外の追跡対象ファイルが存在します:"
  echo "$PRIVATE_TRACKED"
  ERRORS_FOUND=$((ERRORS_FOUND + 1))
fi

# 2. 01-private/ の ignore 設定チェック
if ! git check-ignore -q 01-private/dummy_check_file 2>/dev/null; then
  echo -e "\n❌ 01-private/ が .gitignore に設定されていません。"
  ERRORS_FOUND=$((ERRORS_FOUND + 1))
fi

# 3. 03-output/ 配下の日付形式ディレクトリの ignore 設定チェック
# 例: 03-output/2026-09-17 または 03-output/20260917
DATE_DIR_CHECK=$(find 03-output/ -type d -regextype posix-extended -regex '.*/[0-9]{4}[-/]?[0-9]{2}[-/]?[0-9]{2}$' 2>/dev/null || true)
if [ -n "$DATE_DIR_CHECK" ]; then
  while IFS= read -r dir; do
    if ! git check-ignore -q "$dir" 2>/dev/null; then
      echo -e "\n❌ 03-output 内の日付ディレクトリが ignore 設定されていません: $dir"
      ERRORS_FOUND=$((ERRORS_FOUND + 1))
    fi
  done <<< "$DATE_DIR_CHECK"
fi

# 4. 99-trash/ の追跡対象チェック (.gitkeep またはフォルダ自体が追跡されていること)
TRASH_TRACKED=$(git ls-files 99-trash/ || true)
if [ -z "$TRASH_TRACKED" ]; then
  echo -e "\n❌ 99-trash/ (または 99-trash/.gitkeep) が Git の追跡対象になっていません。"
  ERRORS_FOUND=$((ERRORS_FOUND + 1))
fi

# --------------------------------------------------
# B. サニタイズ（リーク情報）チェック
# --------------------------------------------------

DATE_PATTERN='([12][0-9]{3}[-/年][01]?[0-9][-/月][0-3]?[0-9]日?)'
NAME_PATTERN='([一-龠ぁ-んァ-ヶ]+(氏|さん|様|君|ちゃん)|(Mr\.|Ms\.|Dr\.)\s+[A-Z][a-z]+)'
URL_PATTERN='(https?://[a-zA-Z0-9.\-_~:/?#\[\]@!$&'\''()*+,;=]+)'
COMBINED_PATTERN="${DATE_PATTERN}|${NAME_PATTERN}|${URL_PATTERN}"

for dir in "${TARGET_DIRS[@]}"; do
  if [ -d "$dir" ]; then
    MATCHES=$(grep -E -n -r --binary-files=without-match "$COMBINED_PATTERN" "$dir" || true)

    if [ -n "$MATCHES" ]; then
      echo -e "\n❌ 未サニタイズ（日付/人名/URL）を検出しました: $dir"
      echo "$MATCHES"
      ERRORS_FOUND=$((ERRORS_FOUND + 1))
    fi
  fi
done

# --------------------------------------------------
# C. 最終結果判定
# --------------------------------------------------

if [ $ERRORS_FOUND -gt 0 ]; then
  echo -e "\n💥 チェック不合格: 修正してからコミットしてください。"
  exit 1
else
  echo -e "\n✅ チェック合格: すべての検証をパスしました。"
  exit 0
fi