# PythonAnywhere 手動佈署教學 (FamilyHQ)

這份文件將引導您如何將專案打包並佈署到 PythonAnywhere。

---

## 步驟 1：本機打包
1.  執行 `進度更新.command` 或 `./scripts/進度更新.command`。
2.  這會在專案根目錄產生一個 `01-family.zip`。

## 步驟 2：上傳與解壓縮
1.  登入 [PythonAnywhere](https://www.pythonanywhere.com/)。
2.  點擊右上角的 **"Files"**。
3.  在 **"Upload a file"** 區塊，選擇您電腦中的 `01-family.zip` 並上傳。
4.  點擊右上角的 **"Consoles"**，開啟一個 **"Bash"** 控制台。
5.  在控制台輸入以下指令來解壓縮：
    ```bash
    unzip -o 01-family.zip -d 01-family
    ```
    *注意：使用 `-o` 參數會自動覆蓋舊檔案，這是同步更新的關鍵。*

---

## 步驟 3：建立虛擬環境 (僅首次佈署需要)
如果您已經建立過 `family-venv`，可以跳過此步。
1.  在 Bash 控制台中執行：
    ```bash
    mkvirtualenv --python=/usr/bin/python3.10 family-venv
    pip install -r ~/01-family/src/requirements.txt
    ```

---

## 步驟 4：設定 Web App
1.  點擊右上角的 **"Web"** 標籤。
2.  **首次佈署**：點擊 "Add a new web app" -> Manual configuration -> Python 3.10。
3.  **路徑設定** (請將 `你的帳號` 替換為實際名稱)：
    *   **Source code:** `/home/你的帳號/01-family/src`
    *   **Working directory:** `/home/你的帳號/01-family/src`
    *   **Virtualenv:** `/home/你的帳號/.virtualenvs/family-venv`

---

## 步驟 5：設定 WSGI 檔案 (最關鍵)
1.  在 Web 頁面點擊 **"WSGI configuration file"** 連結。
2.  刪除內容並貼上以下代碼：
```python
import sys
import os

path = '/home/你的帳號/01-family/src'
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)
from app import app as application
```
3.  點擊 **"Save"**。

---

## 步驟 6：重新啟動 (同步更新必做)
1.  回到 **"Web"** 標籤頁面。
2.  點擊綠色的 **"Reload [yourdomain]"** 按鈕。
3.  開啟網站，輸入密碼 `09150915` 即可。

---

## 💡 如何進行同步更新？
1.  在本機執行「進度更新」產生新的 `01-family.zip`。
2.  上傳到 PythonAnywhere 的 Files 頁面。
3.  在 Bash 執行 `unzip -o 01-family.zip -d 01-family`。
4.  在 Web 頁面點擊 **"Reload"**。
