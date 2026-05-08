import os
import shutil
import datetime
import json
import subprocess

# 設定路徑
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, 'src')
MEMORY_DIR = os.path.join(BASE_DIR, 'memory')
CHECKPOINTS_DIR = os.path.join(MEMORY_DIR, 'checkpoints')
DATA_JS = os.path.join(MEMORY_DIR, 'data.js')
LOG_MD = os.path.join(MEMORY_DIR, 'LOG.md')
README_MD = os.path.join(BASE_DIR, 'README.md')
ROOT_ZIP = os.path.join(BASE_DIR, '01-family.zip')

def run_command(cmd, cwd=BASE_DIR):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"指令執行錯誤: {cmd}")
        print(result.stderr)
        return False
    return True

def create_root_zip():
    print("正在打包專案 (01-family.zip)...")
    # 建立一個臨時資料夾來打包，避免把 zip 自己也包進去
    temp_dir = os.path.join(BASE_DIR, 'temp_package')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # 複製需要的檔案
    shutil.copytree(SRC_DIR, os.path.join(temp_dir, 'src'))
    shutil.copytree(MEMORY_DIR, os.path.join(temp_dir, 'memory'))
    shutil.copy(os.path.join(BASE_DIR, 'README.md'), temp_dir)
    shutil.copy(os.path.join(BASE_DIR, 'PYTHONANYWHERE_DEPLOY_GUIDE.md'), temp_dir)
    
    # 打包
    if os.path.exists(ROOT_ZIP):
        os.remove(ROOT_ZIP)
    shutil.make_archive(ROOT_ZIP.replace('.zip', ''), 'zip', temp_dir)
    
    # 清理
    shutil.rmtree(temp_dir)
    print(f"✅ 打包完成: {ROOT_ZIP}")

def create_checkpoint_zip(timestamp):
    print("正在建立備份快照...")
    zip_name = f"checkpoint_{timestamp}"
    zip_path = os.path.join(CHECKPOINTS_DIR, zip_name)
    shutil.make_archive(zip_path, 'zip', SRC_DIR)
    return f"{zip_name}.zip"

def update_logs(description, details, zip_file, timestamp_str):
    print("正在更新記憶日誌...")
    if os.path.exists(DATA_JS):
        with open(DATA_JS, 'r', encoding='utf-8') as f:
            content = f.read()
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
    
    with open(DATA_JS, 'w', encoding='utf-8') as f:
        f.write(f"window.memoryData = {json.dumps(data, ensure_ascii=False, indent=2)};")
        
    with open(LOG_MD, 'a', encoding='utf-8') as f:
        f.write(f"\n## {timestamp_str}\n")
        f.write(f"*   **摘要**: {description}\n")
        f.write(f"*   **詳情**: {details}\n")
        f.write(f"*   **備份**: {zip_file}\n")
        
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
    description = input("請輸入這次修改的簡短描述: ") or "更新專案內容"
    details = input("請輸入詳細說明 (可留空): ") or ""
    
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    timestamp_file = now.strftime("%Y%m%d_%H%M%S")
    
    # 1. 建立 ZIP 備份 (Snapshot)
    zip_file = create_checkpoint_zip(timestamp_file)
    
    # 2. 建立供 PythonAnywhere 使用的總打包
    create_root_zip()
    
    # 3. 更新日誌
    update_logs(description, details, zip_file, timestamp_str)
    
    # 4. Git 同步
    print("正在推送到 GitHub...")
    if run_command("git add .") and \
       run_command(f'git commit -m "Checkpoint: {description}"') and \
       run_command("git push"):
        print("\n✨ 進度更新完成！")
        print(f"📦 已產出佈署包: {ROOT_ZIP}")
        print("📝 已更新紀錄並同步至 GitHub。")
    else:
        print("\n❌ Git 推送失敗，請檢查網路或 Git 設定。")

if __name__ == "__main__":
    main()
