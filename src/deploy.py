import os
import requests

USERNAME = 'Cathyfamily'
TOKEN = '1f990874775a217546087f86f661c02f637d0c02'
BASE_URL = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/'
TARGET_DIR = '/home/Cathyfamily/family'

def upload_file(local_path, remote_path):
    url = f"{BASE_URL}files/path{remote_path}"
    with open(local_path, 'rb') as f:
        files = {'content': f}
        response = requests.post(
            url,
            files=files,
            headers={'Authorization': f'Token {TOKEN}'}
        )
    if response.status_code in [200, 201]:
        print(f"✅ 成功上傳: {local_path} -> {remote_path}")
    else:
        print(f"❌ 上傳失敗 {local_path}: {response.status_code} - {response.content}")

def deploy():
    # 要上傳的檔案與資料夾 (排除資料庫與虛擬環境)
    files_to_upload = [
        'app.py',
        'models.py',
        'requirements.txt',
    ]
    dirs_to_upload = ['templates', 'static']

    print(f"🚀 開始將專案部署至 PythonAnywhere ({USERNAME})...")

    # 上傳根目錄檔案
    for file in files_to_upload:
        if os.path.exists(file):
            remote_path = f"{TARGET_DIR}/{file}"
            upload_file(file, remote_path)

    # 上傳資料夾內的檔案
    for dir_name in dirs_to_upload:
        for root, _, files in os.walk(dir_name):
            for file in files:
                if file.endswith('.DS_Store') or file.endswith('.pyc'):
                    continue
                local_path = os.path.join(root, file)
                remote_path = f"{TARGET_DIR}/{local_path}"
                upload_file(local_path, remote_path)

    print("\n🎉 檔案上傳完成！")
    print("請進入 PythonAnywhere Web 介面點擊綠色的 'Reload' 按鈕以套用更新。")

if __name__ == '__main__':
    # 確保有安裝 requests
    try:
        import requests
    except ImportError:
        print("請先執行 `pip install requests` 或安裝虛擬環境中的 requirements.txt")
        exit(1)
        
    deploy()
