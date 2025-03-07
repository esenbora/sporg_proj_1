# SPORG
=======
# Transfermarkt Data Scraping Project
This project contains Python scripts used to scrape various football data from Transfermarkt and FBREF websites.

## Özellikler

- Liglerin belli sezonlarinda oynayan takimlari cekme
- Belli sezonlardaki lig takimlarin kadro verileri
- Tüm veriler CSV formatında kaydedilir
- Ayni zamanda json formatinda da kaydedilir

## Competitions

- Bundesliga (Germany)
- Ligue 1 (France)
- Premier League (England)
- LaLiga (Spain)
- Serie A (Italy)

## Setup

```bash
pip install -r requirements.txt
```

## Usage

For teams in the season:
  League Team Scraper.ipynb

For teams squad information:
  Team Squad Info Scraper.ipynb

## Directory Structure

```
.
├── data/
│   ├── league-fixture/           # info about every game in a comp's season
│   ├── squad-information/        # info about each team's squad
│   └── teams-in-the-season/      # teams that participated during a season
├── .gitignore
├── FBREF Scraper.py
├── League Team Scraper.ipynb
├── Team Squad Info Scraper.ipynb
├── requirements.txt
└── README.md
```

## Notes

- Data covers seasons from 2020/21 to 2024/25
- Data is scraped in English
