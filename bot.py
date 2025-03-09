import requests
import time
import os

# Discord Webhook URL aus GitHub Secrets laden
discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

# Portfolio mit neuen Aktien
portfolio = {
    "Rheinmetall": {"wkn": "703000", "kaufpreis": 65},
    "Palantir": {"wkn": "A2QA4J", "kaufpreis": 35},
    "BigBear.ai": {"wkn": "A3D92B", "kaufpreis": 5},
    "MicroStrategy": {"wkn": "722713", "kaufpreis": 1000},
    "C3.ai": {"wkn": "A2QJVE", "kaufpreis": 25}
}

# Verlustgrenze für Warnungen
verlustgrenze = -50  # Ab -50 € Warnung und Entscheidung

# API-URL für Aktienpreise (Platzhalter)
api_url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols="

def log(message):
    """ Schreibt Nachrichten in die Konsole und sendet sie an Discord """
    print(message)
    send_discord_alert(f"📝 LOG: {message}")

def get_stock_price(wkn):
    """ Holt den aktuellen Aktienkurs """
    try:
        response = requests.get(f"{api_url}{wkn}")
        if response.status_code == 200:
            return response.json()["quoteResponse"]["result"][0]["regularMarketPrice"]
        else:
            log(f"⚠️ Fehler beim Abrufen von {wkn}: {response.status_code}")
            return 0
    except Exception as e:
        log(f"❌ API-Fehler: {str(e)}")
        return 0

def check_portfolio():
    """ Überprüft das Portfolio & sendet Warnungen """
    for stock, data in portfolio.items():
        current_price = get_stock_price(data["wkn"])
        if current_price:
            percent_change = ((current_price - data["kaufpreis"]) / data["kaufpreis"]) * 100
            log(f"📊 {stock}: {current_price} € ({percent_change:.2f}%)")
            if percent_change <= verlustgrenze:
                send_discord_alert(f"⚠️ {stock} hat die Verlustgrenze erreicht! {percent_change:.2f}% | Empfehlung: {get_recommendation(stock)}")

def get_recommendation(stock):
    """ Gibt eine Empfehlung basierend auf dem Preis ab """
    return "Verkaufen!" if stock == "Rheinmetall" and get_stock_price("703000") < (portfolio["Rheinmetall"]["kaufpreis"] * 0.85) else "Halten"

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
    
    # Debug: Test ob die Schleife durchläuft
    for i in range(3):  # Anstatt Endlosschleife erstmal nur 3 Durchläufe zum Testen
        log(f"🔄 Starte Marktcheck Durchgang {i+1}")
        check_portfolio()
        fetch_news()
        log("⏳ Warten auf den nächsten Check...")
        time.sleep(5)  # Kürzere Wartezeit zum Debuggen
    log("✅ Testlauf abgeschlossen. Falls alles gut lief, können wir die Endlosschleife aktivieren.")
