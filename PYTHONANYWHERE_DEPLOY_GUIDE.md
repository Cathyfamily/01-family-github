# PythonAnywhere 手動佈署教學 (FamilyHQ)

這份文件將引導您如何將 `family_app.zip` 上傳並佈署到 PythonAnywhere。

---

## 步驟 1：上傳與解壓縮

1.  登入 [PythonAnywhere](https://www.pythonanywhere.com/)。
2.  點擊右上角的 **"Files"**。
3.  在 **"Upload a file"** 區塊，選擇您電腦中的 `family_app.zip` 並上傳。
4.  點擊右上角的 **"Consoles"**，開啟一個 **"Bash"** 控制台。
5.  在控制台輸入以下指令來解壓縮（假設您上傳到根目錄）：
    ```bash
    unzip family_app.zip -d my_family_app
    ```
    *這會建立一個 `my_family_app` 資料夾並將內容解壓進去。*

---

## 步驟 2：建立虛擬環境與安裝套件

在同一個 Bash 控制台中，執行以下指令：

1.  **建立虛擬環境** (建議使用 Python 3.10 或更高版本)：
    ```bash
    mkvirtualenv --python=/usr/bin/python3.10 family-venv
    ```
2.  **安裝必要套件**：
    ```bash
    cd ~/my_family_app
    pip install -r src/requirements.txt
    ```

---

## 步驟 3：設定 Web App

1.  回首頁，點擊右上角的 **"Web"** 標籤。
2.  點擊 **"Add a new web app"**。
    *   Domain name: 選擇您的預設網域 (例如 `yourusername.pythonanywhere.com`)。
    *   Select a Python Web framework: 選擇 **"Manual configuration"** (這很重要，不要選 Flask)。
    *   Select a Python version: 選擇 **"Python 3.10"**。
3.  **進入 Web App 設定頁面後，修改以下欄位：**
    *   **Source code:** `/home/你的帳號/my_family_app/src`
    *   **Working directory:** `/home/你的帳號/my_family_app/src`
    *   **Virtualenv:** `/home/你的帳號/.virtualenvs/family-venv`

---

## 步驟 4：設定 WSGI 檔案 (最關鍵的一步)

1.  在 Web 頁面的 "Code" 區塊，找到 **"WSGI configuration file"** 的連結並點擊進去。
2.  刪除裡面的所有內容，並貼上以下代碼：

```python
import sys
import os

# 指向你的 src 資料夾
path = '/home/你的帳號/my_family_app/src'
if path not in sys.path:
    sys.path.append(path)

# 設定環境變數 (如果需要)
os.chdir(path)

from app import app as application
```

3.  點擊上方的 **"Save"**。

---

## 步驟 5：重新啟動並測試

1.  回到 **"Web"** 標籤頁面。
2.  點擊綠色的 **"Reload [yourdomain]"** 按鈕。
3.  開啟您的網站網址。
4.  您應該會看到登入頁面，請輸入密碼 `09150915` 即可進入。

---

## 疑難排解

*   如果出現 "Internal Server Error"，請查看 Web 頁面下方的 **"Error log"**。
*   確保 `src/database.db` 在 PythonAnywhere 上有寫入權限 (通常預設即可)。
*   如果有修改代碼，每次修改後都必須在 Web 頁面點擊 **"Reload"**。
