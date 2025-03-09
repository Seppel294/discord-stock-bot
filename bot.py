import requests
import time
import os

# Discord Webhook URL aus GitHub Secrets laden
discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

# Alpha Vantage API-Key aus GitHub Secrets (neu hinzugefügt!)
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

# Portfolio mit neuen Aktien (WKN durch Ticker ersetzt)
portfolio = {
    "Rheinmetall": {"ticker": "RHM.DE", "kaufpreis": 65},
    "Palantir": {"ticker": "PLTR", "kaufpreis": 35},
    "BigBear.ai": {"ticker": "BBAI", "kaufpreis": 5},
    "MicroStrategy": {"ticker": "MSTR", "kaufpreis": 1000},
    "C3.ai": {"ticker": "AI", "kaufpreis": 25}
}

# Verlustgrenze für Warnungen
verlustgrenze = -50  # Ab -50 € Warnung und Entscheidung

# API-URL für Aktienkurse von Alpha Vantage
api_url = "https://www.alphavantage.co/query"

def log(message):
    """ Schreibt Nachrichten in die Konsole und sendet sie an Discord """
    print(message)
    send_discord_alert(f"📝 LOG: {message}")

def get_stock_price(ticker):
    """ Holt den aktuellen Aktienkurs von Alpha Vantage """
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": ticker,
        "interval": "60min",
        "apikey": alpha_vantage_api_key
    }
    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        if "Time Series (60min)" in data:
            latest_key = list(data["Time Series (60min)"].keys())[0]
            return float(data["Time Series (60min)"][latest_key]["1. open"])
        else:
            log(f"⚠️ Fehler beim Abrufen von {ticker}: {data}")
            return 0
    except Exception as e:
        log(f"❌ API-Fehler: {str(e)}")
        return 0

def check_portfolio():
    """ Überprüft das Portfolio & sendet Warnungen """
    for stock, data in portfolio.items():
        current_price = get_stock_price(data["ticker"])
        if current_price:
            percent_change = ((current_price - data["kaufpreis"]) / data["kaufpreis"]) * 100
            log(f"📊 {stock}: {current_price} € ({percent_change:.2f}%)")
            if percent_change <= verlustgrenze:
                send_discord_alert(f"⚠️ {stock} hat die Verlustgrenze erreicht! {percent_change:.2f}% | Empfehlung: {get_recommendation(stock)}")

def get_recommendation(stock):
    """ Gibt eine Empfehlung basierend auf dem Preis ab """
    return "Verkaufen!" if stock == "Rheinmetall" and get_stock_price("RHM.DE") < (portfolio["Rheinmetall"]["kaufpreis"] * 0.85) else "Halten"

def send_discord_alert(message):
    """ Sendet eine Nachricht an Discord """
    try:
        payload = {"content": message}
        response = requests.post(discord_webhook_url, json=payload)
        if response.status_code != 204:
            log(f"⚠️ Webhook-Fehler: {response.status_code}")
    except Exception as e:
        log(f"❌ Discord-Fehler: {str(e)}")

# News & Politik-Analyse
def fetch_news():
    headlines = ["Bundesregierung plant neue Rüstungsausgaben", "KI-Sektor wächst weiter: Palantir gewinnt neuen Regierungsauftrag"]
    send_discord_alert(f"📰 Tägliche Marktnews: {headlines}")

if __name__ == "__main__":
    log("✅ Bot läuft! Ich überwache jetzt den Markt für dich.")
    
    while True:
        log("🔄 Starte Marktcheck")
        check_portfolio()
        fetch_news()
        log("⏳ Warten auf den nächsten Check...")
        time.sleep(3600)  # Alle 60 Minuten prüfen
