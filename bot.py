import requests
import os
import time

discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

portfolio = {
    "Nvidia": {"wkn": "918422", "kaufpreis": 250},
    "Rheinmetall": {"wkn": "703000", "kaufpreis": 250},
    "Palantir": {"wkn": "A2QA4J", "kaufpreis": 250}
}

api_url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols="

def get_stock_price(wkn):
    response = requests.get(f"{api_url}{wkn}")
    if response.status_code == 200:
        try:
            return response.json()["quoteResponse"]["result"][0]["regularMarketPrice"]
        except (KeyError, IndexError):
            return 0
    return 0

def check_portfolio():
    for stock, data in portfolio.items():
        current_price = get_stock_price(data["wkn"])
        if current_price:
            percent_change = ((current_price - data["kaufpreis"]) / data["kaufpreis"]) * 100
            if percent_change <= -10:
                message = f"⚠️ Achtung! {stock} ist um {percent_change:.2f}% gefallen! Überprüfe dein Investment!"
                send_discord_alert(message)

def send_discord_alert(message):
    payload = {"content": message}
    requests.post(discord_webhook_url, json=payload)

send_discord_alert("✅ Test: Dein GitHub-Bot läuft jetzt!")
check_portfolio()
