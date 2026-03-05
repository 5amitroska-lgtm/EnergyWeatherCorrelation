# EnergyWeather Correlation

Projekt analyzuje vzťah medzi hodinovými cenami elektriny v Česku a priemernou dennou teplotou krajiny. Dáta sa získavajú automaticky z verejných API, ukladajú do lokálnej SQLite databázy a následne sa vizualizujú a porovnávajú.

---

## 🔍 Ciele projektu
- Získať hodinové ceny elektriny pre Česko (EUR/MWh).
- Získať priemernú dennú teplotu krajiny.
- Ukladať dáta do SQLite databázy.
- Porovnávať vývoj cien elektriny s teplotou.
- Vytvoriť základ pre ďalšiu analýzu alebo vizualizáciu.

---


---

## 🌐 Použité API

### 1. Ceny elektriny – Energy-Charts API
- Endpoint: `https://api.energy-charts.info/price`
- Parametre: `country=CZE`, `start=YYYY-MM-DD`, `end=YYYY-MM-DD`
- Výstup:  
  - `unix_seconds[]` – časové značky  
  - `price[]` – ceny v EUR/MWh  

### 2. Teplota – Open-Meteo API
- Endpoint: `https://api.open-meteo.com/v1/climate`
- Výstup: priemerná denná teplota pre danú krajinu

---

## 🗃️ Databáza

Použitá je **SQLite**, pretože:
- nevyžaduje server,
- je ideálna pre malé a demo projekty,
- je súčasťou Pythonu.

### Štruktúra tabuľky `api_data`

| stĺpec     | typ     | popis |
|------------|---------|-------|
| id         | INTEGER | Primárny kľúč |
| timestamp  | TEXT    | ISO časová značka |
| value      | REAL    | Cena elektriny alebo teplota |

---

## ⚙️ Inštalácia

### 1. Klonovanie projektu

git clone https://github.com/username/EnergyWeather-Correlation.git (github.com in Bing)
cd EnergyWeather-Correlation

### 3. Inštalácia balíkov

pip install -r requirements.txt

---

## 📥 Zber dát

### Spustenie skriptu na získanie cien elektriny

python app/database/read_data.py


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

## 🧪 Plánovanie automatického zberu dát

### Windows Task Scheduler
- Trigger: Daily
- Action: `python app/database/fetch_data.py`

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



