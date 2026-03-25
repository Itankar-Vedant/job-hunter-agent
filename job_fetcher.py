import requests
from datetime import datetime

def fetch_foundit_jobs():
    all_jobs = []

    searches = [
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

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Referer": "https://www.foundit.in/",
        "Origin": "https://www.foundit.in",
    }

    for role, location in searches:
        try:
            print(f"🔍 Searching: {role} in {location}", flush=True)

            url = "https://www.foundit.in/middleware/jobsearch/search"
            params = {
                "query": role,
                "locations": location,
                "experienceRanges": "0~1",
                "limit": 10,
                "offset": 0,
                "sort": 1
            }

            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=15
            )

            print(f"   Status: {response.status_code}", flush=True)

            if response.status_code == 200:
                try:
                    data = response.json()
                    jobs = data.get('jobDetails', []) or data.get('jobs', []) or data.get('results', [])
                    print(f"   Found {len(jobs)} jobs", flush=True)

                    for job in jobs[:8]:
                        title = job.get('title', '') or job.get('jobTitle', '')
                        company = job.get('companyName', '') or job.get('company', '')
                        loc = job.get('location', '') or location
                        job_id = job.get('jobId', '') or job.get('id', '')
                        link = f"https://www.foundit.in/srp/results?query={role.replace(' ', '+')}&locations={location}"

                        if title:
                            all_jobs.append({
                                'title': title,
                                'company': company,
                                'location': loc,
                                'experience': 'Fresher',
                                'link': link,
                                'source': 'Foundit',
                                'fetched_at': str(datetime.now())
                            })
                except Exception as e:
                    print(f"   ❌ Parse error: {e}", flush=True)
                    print(f"   Response: {response.text[:200]}", flush=True)
            else:
                print(f"   ❌ Failed: {response.text[:200]}", flush=True)

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
    jobs = fetch_foundit_jobs()

    for i, job in enumerate(jobs[:10]):
        print(f"\n{i+1}. {job['title']}")
        print(f"   🏢 {job['company']}")
        print(f"   📍 {job['location']}")
        print(f"   🔗 {job['link']}")