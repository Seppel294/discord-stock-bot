import requests
import time
import os

# Discord Webhook URL aus den GitHub Secrets laden
discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

# Neue Portfolio-Zusammensetzung (Rheinmetall 65 %, Palantir 35 %)
portfolio = {
    "Rheinmetall": {"wkn": "703000", "kaufpreis": 65},
    "Palantir": {"wkn": "A2QA4J", "kaufpreis": 35}
}

# Verlustgrenze für Warnungen
verlustgrenze = -50  # Ab -50 € Warnung und Handlungsempfehlung

# API-URL für Aktienpreise (Platzhalter)
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
            if percent_change <= verlustgrenze:
                send_discord_alert(f"⚠️ {stock} hat die Verlustgrenze erreicht! {percent_change:.2f}% | Empfehlung: {get_recommendation(stock)}")

def get_recommendation(stock):
    return "Verkaufen!" if stock == "Rheinmetall" and get_stock_price("703000") < (portfolio["Rheinmetall"]["kaufpreis"] * 0.85) else "Halten"

def send_discord_alert(message):
    payload = {"content": message}
    requests.post(discord_webhook_url, json=payload)

# News & Politik-Analyse
def fetch_news():
    headlines = ["Bundesregierung plant neue Rüstungsausgaben", "KI-Sektor wächst weiter: Palantir gewinnt neuen Regierungsauftrag"]
    send_discord_alert(f"📰 Tägliche Marktnews: {headlines}")

if __name__ == "__main__":
    send_discord_alert("✅ Bot läuft! Ich überwache jetzt den Markt für dich.")
    while True:
        check_portfolio()
        fetch_news()
        time.sleep(3600)  # Alle 60 Minuten prüfen
