import requests
from datetime import datetime

def fetch_jobs():
    all_jobs = []

    searches = [
        ("full-stack-developer", "nagpur"),
        ("full-stack-developer", "pune"),
        ("technical-support", "nagpur"),
        ("technical-support", "pune"),
        ("python-developer", "pune"),
        ("ai-developer", "pune"),
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://internshala.com/",
        "X-Requested-With": "XMLHttpRequest",
    }

    for role, location in searches:
        try:
            print(f"🔍 Searching: {role} in {location}", flush=True)

            url = f"https://internshala.com/jobs/{role}-jobs-in-{location}"

            response = requests.get(url, headers=headers, timeout=15)
            print(f"   Status: {response.status_code}", flush=True)

            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                job_cards = soup.find_all('div', class_='individual_internship') or \
                            soup.find_all('div', class_='job-internship-card') or \
                            soup.find_all('a', class_='job-title-href')

                print(f"   Found {len(job_cards)} jobs", flush=True)

                for card in job_cards[:8]:
                    try:
                        title = card.find('h3') or card.find('h2') or \
                                card.find('div', class_='job-title') or \
                                card.find('p', class_='job-internship-name')
                        company = card.find('p', class_='company-name') or \
                                  card.find('div', class_='company-name') or \
                                  card.find('a', class_='link_display_like_text')
                        link_tag = card.find('a', href=True)

                        title_text = title.text.strip() if title else "N/A"
                        company_text = company.text.strip() if company else "N/A"
                        link = "https://internshala.com" + link_tag['href'] \
                               if link_tag and link_tag['href'].startswith('/') \
                               else link_tag['href'] if link_tag else url

                        if title_text != "N/A":
                            all_jobs.append({
                                'title': title_text,
                                'company': company_text,
                                'location': location.capitalize(),
                                'experience': 'Fresher',
                                'link': link,
                                'source': 'Internshala',
                                'fetched_at': str(datetime.now())
                            })
                    except:
                        continue

        except Exception as e:
            print(f"❌ Error: {e}", flush=True)
            continue

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
    print("🔍 Fetching jobs...\n")
    jobs = fetch_jobs()

    for i, job in enumerate(jobs[:10]):
        print(f"\n{i+1}. {job['title']}")
        print(f"   🏢 {job['company']}")
        print(f"   📍 {job['location']}")
        print(f"   🔗 {job['link']}")