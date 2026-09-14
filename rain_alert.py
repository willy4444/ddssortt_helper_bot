import os
import requests
from datetime import datetime

# =========================
# 1. Telegram 設定
# =========================

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# =========================
# 2. 天氣地點設定
# =========================

# 桃園市座標
LATITUDE = 24.9936
LONGITUDE = 121.3010

# =========================
# 3. 取得 Open-Meteo 天氣資料
# =========================

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "daily": "precipitation_probability_max",
    "timezone": "Asia/Taipei",
    "forecast_days": 1
}

response = requests.get(url, params=params)
data = response.json()

# =========================
# 4. 取得今天最高降雨機率
# =========================

rain_probability = data["daily"]["precipitation_probability_max"][0]

today = datetime.now().strftime("%Y-%m-%d")

print(f"日期：{today}")
print(f"今天最高降雨機率：{rain_probability}%")

# =========================
# 5. 判斷是否超過 60%
# =========================

if rain_probability > 60:

    message = (
        f"☔ 今天是 {today}\n"
        f"最高降雨機率：{rain_probability}%\n"
        f"記得帶傘喔！"
    )

    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    telegram_data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    telegram_response = requests.post(
        telegram_url,
        data=telegram_data
    )

    print("已傳送 Telegram 通知！")
    print(telegram_response.json())

else:

    print("今天降雨機率沒有超過 60%，不用傳送通知。")
