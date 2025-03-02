# Transfermarkt Data Scraping Project
Bu proje, Transfermarkt websitesinden çeşitli futbol verilerini çekmek için kullanılan Python scriptlerini içerir.

## Özellikler

- UEFA ülke katsayıları verilerini çekme
- Lig puan durumu verilerini çekme
- Transfer bilançosu verilerini çekme
- Tüm veriler CSV formatında kaydedilir
- Her veri çekimi için screenshot alınır

## Desteklenen Ligler

- Chance Liga (Çek Cumhuriyeti)
- Bundesliga (Almanya)
- Jupiler Pro League (Belçika)
- Ligue 1 (Fransa)
- Eredivisie (Hollanda)
- Premier League (İngiltere)
- LaLiga (İspanya)
- Serie A (İtalya)
- Liga Portugal (Portekiz)
- Süper Lig (Türkiye)

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım

UEFA katsayıları için:
```bash
python scrape_uefa_coefficients.py
```

Lig puan durumları için:
```bash
python scrape_league_standings.py
```

Transfer bilançoları için:
```bash
python scrape_single_balance.py
```

## Dosya Yapısı

```
.
├── data/
│   ├── league/        # Lig puan durumu verileri
│   ├── transfer/      # Transfer bilançosu verileri
│   └── uefa/          # UEFA katsayı verileri
├── screenshots/
│   ├── league/        # Lig puan durumu screenshot'ları
│   ├── transfer/      # Transfer bilançosu screenshot'ları
│   └── uefa/          # UEFA katsayı screenshot'ları
├── scrape_league_standings.py
├── scrape_single_balance.py
├── scrape_uefa_coefficients.py
├── requirements.txt
└── README.md
```

## Notlar

- Tüm veriler 2020/21'den 2024/25'e kadar olan sezonları kapsar
- Veriler Türkçe olarak çekilir
- Her script headless modda çalışır
- Hata durumunda screenshot alınır 
