from playwright.sync_api import sync_playwright
import csv
import os
import re

def clean_number(text):
    """Clean and convert number text to proper format"""
    if not text:
        return "0"
    # Remove any non-numeric characters except dots, commas, and minus
    cleaned = re.sub(r'[^\d,.-]', '', text)
    # Convert German/Turkish number format to standard
    cleaned = cleaned.replace('.', '').replace(',', '.')
    return cleaned

def handle_cookie_consent(page):
    """Handle cookie consent popup"""
    consent_selectors = [
        "button#onetrust-accept-btn-handler",
        "button.sp_choice_type_11",
        "button[title='Accept']",
        "button[title='Kabul']",
        "#sp_message_iframe_575846"
    ]
    
    for selector in consent_selectors:
        try:
            if page.locator(selector).is_visible(timeout=5000):
                print(f"Found consent button with selector: {selector}")
                if 'iframe' in selector:
                    frame = page.frame_locator(selector)
                    frame.locator("button[title='Accept']").click()
                else:
                    page.locator(selector).click()
                break
        except Exception as e:
            continue

def scrape_league_standings(season_id, league_code, league_name):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            )
            
            page = context.new_page()
            page.set_extra_http_headers({
                'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            })

            url = f"https://www.transfermarkt.com.tr/super-lig/spieltagtabelle/wettbewerb/{league_code}/saison_id/{season_id}"
            print(f"\nScraping league standings for {league_name} season {season_id}/{season_id+1}...")
            print(f"URL: {url}")
            
            page.goto(url)
            handle_cookie_consent(page)
            
            # Wait for the table to load
            table = page.wait_for_selector('table.items')
            if not table:
                raise Exception("Table not found")

            rows = page.locator('table.items > tbody > tr:not(.bg_blau_20)').all()
            if not rows:
                raise Exception("No rows found in table")

            print(f"Found {len(rows)} teams")
            data = []
            
            for row in rows:
                cells = row.locator('td').all()
                if len(cells) >= 10:  # Ensure we have enough cells
                    row_data = {
                        'Siralama': clean_number(cells[0].inner_text()),
                        'Takim': cells[2].inner_text().strip(),
                        'Mac': clean_number(cells[3].inner_text()),
                        'Galibiyet': clean_number(cells[4].inner_text()),
                        'Beraberlik': clean_number(cells[5].inner_text()),
                        'Maglubiyet': clean_number(cells[6].inner_text()),
                        'Attigi_Gol': clean_number(cells[7].inner_text().split(':')[0]),
                        'Yedigi_Gol': clean_number(cells[7].inner_text().split(':')[1]),
                        'Averaj': clean_number(cells[8].inner_text()),
                        'Puan': clean_number(cells[9].inner_text())
                    }
                    data.append(row_data)
                    print(f"Processed {row_data['Takim']}")

            if not data:
                raise Exception("No data was extracted from the table")

            # Create directory if it doesn't exist
            os.makedirs('data/league', exist_ok=True)
            
            # Save to CSV
            filename = f"data/league/{league_name}_{season_id}_{season_id+1}.csv"
            fieldnames = [
                'Siralama', 'Takim', 'Mac', 'Galibiyet', 'Beraberlik',
                'Maglubiyet', 'Attigi_Gol', 'Yedigi_Gol', 'Averaj', 'Puan'
            ]
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            print(f"\nData saved to {filename}")
            
            # Take screenshot
            screenshot_dir = 'screenshots/league'
            os.makedirs(screenshot_dir, exist_ok=True)
            page.screenshot(path=f"{screenshot_dir}/{league_name}_{season_id}_{season_id+1}.png")
            
            browser.close()
            return data
            
    except Exception as e:
        print(f"Error scraping league standings: {str(e)}")
        if 'page' in locals():
            try:
                page.screenshot(path=f"screenshots/league/error_{league_name}_{season_id}.png")
                print(f"Error screenshot saved as screenshots/league/error_{league_name}_{season_id}.png")
            except:
                pass
        return None

def main():
    leagues = [
        {"code": "TS1", "name": "chance-liga"},
        {"code": "L1", "name": "bundesliga"},
        {"code": "BE1", "name": "jupiler-pro-league"},
        {"code": "FR1", "name": "ligue-1"},
        {"code": "NL1", "name": "eredivisie"},
        {"code": "GB1", "name": "premier-league"},
        {"code": "ES1", "name": "laliga"},
        {"code": "IT1", "name": "serie-a"},
        {"code": "PO1", "name": "liga-portugal"},
        {"code": "TR1", "name": "super-lig"}
    ]
    
    seasons = [2024, 2023, 2022, 2021, 2020]
    
    for league in leagues:
        print(f"\nProcessing league: {league['name']}")
        for season_id in seasons:
            print(f"\nProcessing season {season_id}/{season_id+1}")
            success = scrape_league_standings(season_id, league['code'], league['name'])
            if not success:
                print(f"Failed to scrape {league['name']} season {season_id}/{season_id+1}")

if __name__ == "__main__":
    main() 