import os
import shutil
import datetime
import json
import subprocess

# 設定路徑 (現在腳本在 scripts/ 底下，所以要往上一層找根目錄)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, 'src')
MEMORY_DIR = os.path.join(BASE_DIR, 'memory')
CHECKPOINTS_DIR = os.path.join(MEMORY_DIR, 'checkpoints')
DATA_JS = os.path.join(MEMORY_DIR, 'data.js')
LOG_MD = os.path.join(MEMORY_DIR, 'LOG.md')
README_MD = os.path.join(BASE_DIR, 'README.md')

def run_command(cmd, cwd=BASE_DIR):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"指令執行錯誤: {cmd}")
        print(result.stderr)
        return False
    return True

def create_checkpoint_zip(timestamp):
    print("正在建立備份快照...")
    zip_name = f"checkpoint_{timestamp}"
    zip_path = os.path.join(CHECKPOINTS_DIR, zip_name)
    shutil.make_archive(zip_path, 'zip', SRC_DIR)
    return f"{zip_name}.zip"

def update_logs(description, details, zip_file, timestamp_str):
    print("正在更新記憶日誌...")
    # 讀取現有的 data.js
    if os.path.exists(DATA_JS):
        with open(DATA_JS, 'r', encoding='utf-8') as f:
            content = f.read()
            # 提取 JSON 部分
            start = content.find('[')
            end = content.rfind(']') + 1
            try:
                data = json.loads(content[start:end])
            except:
                data = []
    else:
        data = []
    
    data.append({
        "timestamp": timestamp_str,
        "description": description,
        "details": details,
        "checkpoint_file": zip_file
    })
    
    # 寫回 data.js (JS 格式)
    with open(DATA_JS, 'w', encoding='utf-8') as f:
        f.write(f"window.memoryData = {json.dumps(data, ensure_ascii=False, indent=2)};")
        
    # 更新 Markdown
    with open(LOG_MD, 'a', encoding='utf-8') as f:
        f.write(f"\n## {timestamp_str}\n")
        f.write(f"*   **摘要**: {description}\n")
        f.write(f"*   **詳情**: {details}\n")
        f.write(f"*   **備份**: {zip_file}\n")
        
    # 更新 README.md 的最後動作摘要
    if os.path.exists(README_MD):
        with open(README_MD, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        skip = False
        for line in lines:
            if "## 📌 最後一次動作摘要" in line:
                new_lines.append(line)
                new_lines.append(f"> **{timestamp_str}**: {description}\n")
                skip = True
            elif skip and line.startswith(">"):
                continue
            else:
                skip = False
                new_lines.append(line)
                
        with open(README_MD, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

def main():
    print("=== Ai 進度更新系統 ===")
    description = input("請輸入這次修改的簡短描述 (例如: 修正登入邏輯): ")
    details = input("請輸入詳細說明 (可留空): ") or ""
    
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    timestamp_file = now.strftime("%Y%m%d_%H%M%S")
    
    # 1. 建立 ZIP 備份
    zip_file = create_checkpoint_zip(timestamp_file)
    
    # 2. 更新日誌
    update_logs(description, details, zip_file, timestamp_str)
    
    # 3. Git 同步
    print("正在推送到 GitHub...")
    if run_command("git add .") and \
       run_command(f'git commit -m "Checkpoint: {description}"') and \
       run_command("git push"):
        print("\n✨ 進度更新完成！您可以執行「專案記錄簿」查看。")
    else:
        print("\n❌ Git 推送失敗，請檢查網路或 Git 設定。")

if __name__ == "__main__":
    main()
