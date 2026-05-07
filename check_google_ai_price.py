import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import time

# ================= 設定區塊 =================

# 1. 監控的網址 (Google One AI Premium / Gemini Advanced 頁面)
URL = "https://one.google.com/explore-plan/gemini-advanced"

# 2. 觸發通知的關鍵字 (網頁中出現這些字時會發通知)
TARGET_KEYWORDS = ["特價", "優惠", "折扣", "sale", "discount", "offer", "promotional"]

# 3. 寄件者 Email 設定 (必須使用支援 SMTP 的信箱，建議用 Gmail)
SENDER_EMAIL = "ysf.fcu@gmail.com"  # 請替換為用來寄信的 Gmail
# 注意：Google 現在不允許使用一般密碼登入 SMTP，您必須去 Google 帳號設定產生一組「應用程式密碼」
SENDER_PASSWORD = "請在此輸入您的應用程式密碼" 

# 4. 收件者 Email (您要求通知的信箱)
RECEIVER_EMAIL = "ysf.fcu@gmail.com"

# ============================================

def check_price():
    print(f"[{datetime.datetime.now()}] 正在檢查 Google AI Pro 價格...")
    # 模擬瀏覽器標頭，避免被當作機器人阻擋
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
        html_content = response.text.lower()
        
        # 檢查是否有任何關鍵字出現在網頁原始碼中
        found_keywords = [kw for kw in TARGET_KEYWORDS if kw in html_content]
        
        if found_keywords:
            print(f"🎉 發現疑似特價資訊！觸發關鍵字: {', '.join(found_keywords)}")
            send_email(f"系統在 Google One 網頁中偵測到以下特價關鍵字：{', '.join(found_keywords)}。\n請盡快前往確認：{URL}")
        else:
            print("目前網頁上沒有發現特價關鍵字。")
            
    except Exception as e:
        print(f"❌ 檢查網頁時發生錯誤: {e}")

def send_email(message_body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = "【通知】Google AI Pro 可能有特價活動！"
    
    msg.attach(MIMEText(message_body, 'plain', 'utf-8'))
    
    try:
        # 連接 Gmail 的 SMTP 伺服器
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # 登入信箱
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        # 寄送郵件
        server.send_message(msg)
        server.quit()
        print("✅ 通知信件已成功發送！")
    except Exception as e:
        print(f"❌ 發送 Email 時發生錯誤: {e}")
        print("請確認您的「應用程式密碼」是否設定正確，或是 SMTP 服務是否被阻擋。")

if __name__ == "__main__":
    check_price()
