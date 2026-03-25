from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import urllib.parse
import os

def create_driver():
    import os
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--no-zygote')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    chrome_bin = os.getenv("CHROME_BIN", "/usr/bin/chromium")
    chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")

    options.binary_location = chrome_bin
    service = Service(chromedriver_path)

    driver = webdriver.Chrome(service=service, options=options)
    return driver

def build_search_link(title, location):
    query = urllib.parse.quote(title)
    loc = urllib.parse.quote(location)
    return f"https://www.foundit.in/srp/results?query={query}&locations={loc}&experienceRanges=0~1"

def fetch_foundit_jobs():
    all_jobs = []

    search_queries = [
        ("full+stack+developer", "nagpur"),
        ("full+stack+developer", "pune"),
        ("full+stack+developer", "remote"),
        ("technical+support", "nagpur"),
        ("technical+support", "pune"),
        ("technical+support", "remote"),
        ("python+developer", "pune"),
        ("python+developer", "nagpur"),
        ("ai+developer", "pune"),
        ("ai+developer", "remote"),
    ]

    print("🔧 Creating Chrome driver...", flush=True)
    try:
        driver = create_driver()
        print("✅ Chrome driver created successfully!", flush=True)
    except Exception as e:
        print(f"❌ Chrome driver failed: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return []

    try:
        for role, location in search_queries:
            try:
                url = f"https://www.foundit.in/srp/results?query={role}&locations={location}&experienceRanges=0~1"
                print(f"🔍 Searching: {role.replace('+', ' ')} in {location}", flush=True)

                driver.get(url)
                time.sleep(4)

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "cardContainer"))
                )

                cards = driver.find_elements(By.CLASS_NAME, "cardContainer")
                print(f"   Found {len(cards)} jobs", flush=True)

                for card in cards[:8]:
                    try:
                        # Title
                        try:
                            title = card.find_element(
                                By.ID, "jobCardTitle"
                            ).text.strip()
                        except:
                            title = "N/A"

                        # Company
                        try:
                            company = card.find_element(
                                By.CLASS_NAME, "companyName"
                            ).text.strip()
                        except:
                            company = "N/A"

                        # Location
                        try:
                            loc = card.find_element(
                                By.CSS_SELECTOR, ".details.location"
                            ).text.strip()
                        except:
                            loc = location

                        # Experience
                        try:
                            exp = card.find_element(
                                By.CLASS_NAME, "details"
                            ).text.strip()
                        except:
                            exp = "Fresher"

                        # Build unique search link
                        link = build_search_link(title, location)

                        if title != "N/A":
                            all_jobs.append({
                                'title': title,
                                'company': company,
                                'location': loc,
                                'experience': exp,
                                'link': link,
                                'source': 'Foundit',
                                'fetched_at': str(datetime.now())
                            })

                    except Exception as e:
                        continue

            except Exception as e:
                print(f"❌ Error searching {role} in {location}: {e}", flush=True)
                continue

    finally:
        driver.quit()
        print("🔧 Chrome driver closed", flush=True)

    # Remove duplicates
    seen = set()
    unique_jobs = []
    for job in all_jobs:
        key = job['title'] + job['company']
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    print(f"\n✅ Total unique jobs found: {len(unique_jobs)}", flush=True)
    return unique_jobs


if __name__ == "__main__":
    print("🔍 Fetching fresher jobs from Foundit...\n", flush=True)
    jobs = fetch_foundit_jobs()

    print("\n--- Jobs Found ---")
    for i, job in enumerate(jobs[:10]):
        print(f"\n{i+1}. {job['title']}")
        print(f"   🏢 Company:    {job['company']}")
        print(f"   📍 Location:   {job['location']}")
        print(f"   💼 Experience: {job['experience']}")
        print(f"   🔗 Link:       {job['link']}")