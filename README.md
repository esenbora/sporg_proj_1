# SPORG
=======
# Transfermarkt Data Scraping Project
Bu proje, Transfermarkt websitesinden çeşitli futbol verilerini çekmek için kullanılan Python scriptlerini içerir.

## Özellikler

- Liglerin belli sezonlarinda oynayan takimlari cekme
- Belli sezonlardaki lig takimlarin kadro verileri
- Tüm veriler CSV formatında kaydedilir
- Ayni zamanda json formatinda da kaydedilir

## Desteklenen Ligler

- Bundesliga (Almanya)
- Ligue 1 (Fransa)
- Premier League (İngiltere)
- LaLiga (İspanya)
- Serie A (İtalya)

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım

Sezondaki takımlar için:
  League Team Scraper.ipynb


Takımların kadro bilgileri için:
  Team Squad Info Scraper.ipynb

## Dosya Yapısı

```
.
├── data/
│   ├── squad information/        # Takım kadro bilgileri
│   └── teams in the season/      # Ligdeki takımlar
├── screenshots/
│   ├── league/        # Lig puan durumu screenshot'ları
│   ├── transfer/      # Transfer bilançosu screenshot'ları
│   └── uefa/          # UEFA katsayı screenshot'ları
├── venv
├── .ipynb_checkpoints
├── League Team Scraper.ipynb
├── Team Squad Info Scraper.ipynb
├── requirements.txt
└── README.md
```

## Notlar

- Tüm veriler 2020/21'den 2024/25'e kadar olan sezonları kapsar
- Veriler İngizice olarak çekilir
