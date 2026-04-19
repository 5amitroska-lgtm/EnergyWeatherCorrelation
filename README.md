# EnergyWeather Correlation

Projekt analyzuje vzťah medzi hodinovými cenami elektriny v Europe podla krajiny a priemernou dennou teplotou krajiny. Dáta sa získavajú automaticky z verejných API, ukladajú do lokálnej SQLite databázy a následne sa vizualizujú a porovnávajú.

---

## 🔍 Ciele projektu
- Získať hodinové ceny elektriny pre Europu (EUR/MWh).
- Získať priemernú dennú teplotu krajiny a pocasie.
- Ukladať dáta do SQLite databázy.
- Porovnávať vývoj cien elektriny s pocasim.
- Vytvoriť základ pre ďalšiu analýzu alebo vizualizáciu.

---


---

## 🌐 Použité API

### 1. Ceny elektriny – Energy-Charts API
- Endpoint: `https://api.energy-charts.info/price`
- Parametre: `country=CZE`, `start=YYYY-MM-DD`, `end=YYYY-MM-DD`
- Výstup:  
  - `unix_seconds[]` – časové značky  
  - `vaule[]` – ceny v EUR/MWh  
  - `zone[]` – zona v Europe

### 2. Teplota – Open-Meteo API
- Endpoint: `https://api.open-meteo.com/v1/climate`
- Výstup:
  - `unix_seconds[]` – časové značky  
  - `vaule[]` – hodnota 
  - `zone[]` – zona v Europe
  - `source[]` – typ hodnoty pocasia
    - ej.:
      -  CZE	CZE_temperature 
      - CZE	CZE_cloudcover      
      - CZE	CZE_precipitation
      - CZE	CZE_weathercode 
      - CZE	CZE_weather_text


---

## 🗃️ Databáza

Použitá je **SQLite**, pretože:
- nevyžaduje server,
- je ideálna pre malé a demo projekty,
- je súčasťou Pythonu.

---

## ⚙️ Inštalácia

### 1. Klonovanie projektu

git clone https://github.com/username/EnergyWeather-Correlation.git (github.com in Bing)
cd EnergyWeather-Correlation

### 3. Inštalácia balíkov

pip install -r requirements.txt

---

## 📥 Zber dát

### Spustenie skriptu na zber dat a nasledne vykreslenie grafov podla Zony

run main

pre otvorenie Swaggeru: 
- uvicorn app.main:app --reload
- http://127.0.0.1:8000/docs
  



---

## 📊 Analýza

Skript `compare.py` porovnáva:
- hodinové ceny elektriny,
- priemernú dennú teplotu,
- koreláciu medzi nimi.

Výstupom môže byť:
- tabuľka,
- graf,
- korelačný koeficient.

---

## 📄 Licencia
MIT License

---

## 👤 Autor
Petra Mitroova
Slovenska republika 
2026

🚀 Future Work
🔧 Rozšírenie dátových zdrojov
Integrácia ďalších meteorologických premenných (vietor, oblačnosť, zrážky, slnečný svit) pre presnejšie modelovanie.

Pridanie dát o spotrebe elektriny, výrobe z obnoviteľných zdrojov a cezhraničných tokov.

Podpora viacerých krajín EÚ pre porovnanie regionálnych rozdielov.

📈 Pokročilá analýza a modelovanie
Výpočet korelačných koeficientov pre rôzne časové obdobia (hodiny, dni, sezóny).

Vytvorenie prediktívneho modelu (napr. regresia, LSTM) na odhad budúcich cien elektriny na základe počasia.

Detekcia anomálií v cenách (extrémne výkyvy, negatívne ceny).

🖥️ Vizualizácie a dashboard
Interaktívny dashboard (Streamlit alebo Dash) s grafmi cien, teplôt a korelácií.

Heatmapy zobrazujúce vzťah medzi hodinou dňa, teplotou a cenou.

Export grafov do PNG/HTML pre prezentácie.

🗄️ Vylepšenie dátovej infraštruktúry
Prechod zo SQLite na PostgreSQL pre robustnejšie spracovanie dát.

Automatické čistenie a validácia dát pri ukladaní.

Pravidelné archivovanie starších dát.

🔄 Automatizácia a prevádzka
Plná automatizácia ETL pipeline (napr. pomocou cron/Task Scheduler).

Dockerizácia projektu pre jednoduché nasadenie.

Monitoring chýb a logovanie API odpovedí.

🌍 Kontextové obohatenie
Pridanie informácií o cenách emisných povoleniek (ETS), ktoré ovplyvňujú cenu elektriny.

Porovnanie s cenami plynu a ropy.



