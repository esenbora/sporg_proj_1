from playwright.sync_api import sync_playwright
import csv
import time
import os
import re

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

def clean_number(text):
    """Clean and convert number text to proper format"""
    if not text:
        return "0"
    # Remove any non-numeric characters except dots, commas, and minus
    cleaned = re.sub(r'[^\d,.-]', '', text)
    # Convert German/Turkish number format to standard
    cleaned = cleaned.replace('.', '').replace(',', '.')
    return cleaned

def scrape_transfer_balance(season_id, league_code, league_name):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Changed to headless for faster execution
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            )
            
            page = context.new_page()
            page.set_extra_http_headers({
                'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            })
            
            url = f"https://www.transfermarkt.com.tr/{league_name}/transfers/wettbewerb/{league_code}/plus/?saison_id={season_id}&s_w=&leihe=1&intern=0&intern=1"
            print(f"\nScraping transfer balance data for {league_name} season {season_id}/{season_id+1}...")
            print(f"URL: {url}")
            
            page.goto(url)
            handle_cookie_consent(page)
            
            # Wait for the transfer balance section
            page.wait_for_selector('div.large-8.columns')
            
            balance_data = {}
            
            # Extract transfer counts using specific selectors
            departures = page.locator('div.large-8.columns div.headline:has-text("Gidenler:")').inner_text()
            arrivals = page.locator('div.large-8.columns div.headline:has-text("Gelenler:")').inner_text()
            
            balance_data['Giden_Sayisi'] = re.search(r'Gidenler:\s*(\d+)', departures).group(1) if departures else "0"
            balance_data['Gelen_Sayisi'] = re.search(r'Gelenler:\s*(\d+)', arrivals).group(1) if arrivals else "0"
            
            # Extract financial data using specific text patterns
            financial_data = page.locator('div.large-8.columns div.text').all_inner_texts()
            
            patterns = {
                'Transfer_Geliri': r'Transfer gelir:\s*([\d,.€\s-]+)',
                'Kulup_Basina_Gelir': r'Kulüp başına gelir:\s*([\d,.€\s-]+)',
                'Oyuncu_Basina_Gelir': r'Oyuncu başına gelir:\s*([\d,.€\s-]+)',
                'Transfer_Gideri': r'Transfer giderleri:\s*([\d,.€\s-]+)',
                'Kulup_Basina_Gider': r'Kulüp başına giderler:\s*([\d,.€\s-]+)',
                'Oyuncu_Basina_Gider': r'Oyuncu başına giderler:\s*([\d,.€\s-]+)',
                'Toplam_Bilanco': r'Toplam bilanço:\s*([\d,.€\s-]+)',
                'Kulup_Basina_Bilanco': r'Kulüp başına bilanço:\s*([\d,.€\s-]+)',
                'Oyuncu_Basina_Bilanco': r'Oyuncu başına bilanço:\s*([\d,.€\s-]+)'
            }
            
            for text in financial_data:
                for key, pattern in patterns.items():
                    match = re.search(pattern, text)
                    if match:
                        value = match.group(1).strip()
                        balance_data[key] = clean_number(value)
            
            # Print extracted data
            print("\nTransfer Bilançosu:")
            for key, value in balance_data.items():
                print(f"{key}: {value}")
            
            if not balance_data:
                raise Exception("No data was extracted from the table")

            # Create directory if it doesn't exist
            os.makedirs('data/transfer', exist_ok=True)
            
            # Save to CSV
            filename = f"data/transfer/{league_name}_{season_id}_{season_id+1}.csv"
            fieldnames = [
                'Giden_Sayisi', 'Gelen_Sayisi',
                'Transfer_Geliri', 'Kulup_Basina_Gelir', 'Oyuncu_Basina_Gelir',
                'Transfer_Gideri', 'Kulup_Basina_Gider', 'Oyuncu_Basina_Gider',
                'Toplam_Bilanco', 'Kulup_Basina_Bilanco', 'Oyuncu_Basina_Bilanco'
            ]
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(balance_data)
            
            print(f"\nData saved to {filename}")
            
            # Take screenshot
            screenshot_dir = 'screenshots/transfer'
            os.makedirs(screenshot_dir, exist_ok=True)
            page.screenshot(path=f"{screenshot_dir}/{league_name}_{season_id}_{season_id+1}.png")
            
            browser.close()
            return True
            
    except Exception as e:
        print(f"Error scraping transfer balance: {str(e)}")
        if 'page' in locals():
            try:
                page.screenshot(path=f"screenshots/transfer/error_{league_name}_{season_id}.png")
                print(f"Error screenshot saved as screenshots/transfer/error_{league_name}_{season_id}.png")
            except:
                pass
        return False

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
            success = scrape_transfer_balance(season_id, league['code'], league['name'])
            if not success:
                print(f"Failed to scrape {league['name']} season {season_id}/{season_id+1}")

if __name__ == "__main__":
    main() 