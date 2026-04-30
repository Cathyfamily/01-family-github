#!/bin/bash
cd "$(dirname "$0")"
SCRIPT_DIR="$( pwd )"
PROJECT_ROOT="$( dirname "$SCRIPT_DIR" )"

echo "========================================"
echo "🧠 正在讀取專案記錄簿..."
echo "========================================"

# 1. 顯示 README 中的最後一次動作摘要
echo "📌 最後一次動作摘要："
grep -E "## 📌 最後一次動作摘要|Last Action" -A 1 "$PROJECT_ROOT/README.md" | tail -n 1
echo ""

# 2. 顯示 LOG.md 中最近的 3 筆記錄 (大約取最後 15 行)
echo "📜 最近開發紀錄："
grep -E "^## [0-9]{4}-" "$PROJECT_ROOT/memory/LOG.md" -A 2 | tail -n 15
echo ""

echo "🖥️ 正在開啟視覺化儀表板..."
open "$PROJECT_ROOT/memory/notes.html"

echo "========================================"
echo "✅ 紀錄讀取完畢，您可以繼續開發了！"
echo "========================================"
