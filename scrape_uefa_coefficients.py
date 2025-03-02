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

def scrape_uefa_coefficients():
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

            url = "https://www.transfermarkt.com.tr/uefa/5jahreswertung/statistik/stat/saison_id/2024/plus/1"
            print(f"Scraping UEFA coefficients data...")
            print(f"URL: {url}")
            
            page.goto(url)
            handle_cookie_consent(page)
            
            # Wait for the table to load
            table = page.wait_for_selector('table.items')
            if not table:
                raise Exception("Table not found")

            rows = page.locator('table.items > tbody > tr').all()
            if not rows:
                raise Exception("No rows found in table")

            print(f"Found {len(rows)} rows")
            data = []
            
            for row in rows:
                cells = row.locator('td').all()
                if len(cells) >= 14:  # Ensure we have enough cells
                    row_data = {
                        'Siralama': clean_number(cells[0].inner_text()),
                        'Onceki_Siralama': clean_number(cells[1].inner_text()),
                        'Ulke': cells[2].inner_text().strip(),
                        'Toplam': clean_number(cells[3].inner_text()),
                        'Sampiyonlar_Ligi': clean_number(cells[4].inner_text()),
                        'Avrupa_Ligi': clean_number(cells[5].inner_text()),
                        'Konferans_Ligi': clean_number(cells[6].inner_text()),
                        'Devam_Edenler': clean_number(cells[7].inner_text()),
                        '20_21': clean_number(cells[8].inner_text()),
                        '21_22': clean_number(cells[9].inner_text()),
                        '22_23': clean_number(cells[10].inner_text()),
                        '23_24': clean_number(cells[11].inner_text()),
                        '24_25': clean_number(cells[12].inner_text()),
                        'Toplam_Puan': clean_number(cells[13].inner_text())
                    }
                    data.append(row_data)
                    print(f"Processed {row_data['Ulke']}")

            if not data:
                raise Exception("No data was extracted from the table")

            # Create directory if it doesn't exist
            os.makedirs('data/uefa', exist_ok=True)
            
            # Save to CSV
            filename = "data/uefa/uefa_coefficients.csv"
            fieldnames = [
                'Siralama', 'Onceki_Siralama', 'Ulke', 'Toplam',
                'Sampiyonlar_Ligi', 'Avrupa_Ligi', 'Konferans_Ligi',
                'Devam_Edenler', '20_21', '21_22', '22_23', '23_24',
                '24_25', 'Toplam_Puan'
            ]
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            print(f"\nData saved to {filename}")
            
            # Take screenshot
            screenshot_dir = 'screenshots/uefa'
            os.makedirs(screenshot_dir, exist_ok=True)
            page.screenshot(path=f"{screenshot_dir}/uefa_coefficients.png")
            
            browser.close()
            return data
            
    except Exception as e:
        print(f"Error scraping UEFA coefficients: {str(e)}")
        if 'page' in locals():
            try:
                page.screenshot(path="screenshots/uefa/error_uefa.png")
                print("Error screenshot saved as screenshots/uefa/error_uefa.png")
            except:
                pass
        return None

if __name__ == "__main__":
    data = scrape_uefa_coefficients()
    if data:
        print("\nSuccessfully scraped UEFA coefficients data")
    else:
        print("\nFailed to scrape UEFA coefficients data") 