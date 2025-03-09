name: Run Discord Stock Bot

on:
  schedule:
    - cron: '*/60 * * * *'  # Alle 60 Minuten ausführen
  workflow_dispatch:  # Manuelles Starten möglich

jobs:
  run-bot:
    runs-on: ubuntu-latest
    steps:
      - name: Repository klonen
        uses: actions/checkout@v4

      - name: Python installieren
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Abhängigkeiten installieren
        run: pip install requests

      - name: Bot ausführen
        env:
          DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
        run: python bot.py
