import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def filter_jobs_with_ai(jobs):
    print("\n🧠 AI filtering jobs...\n")

    filtered_jobs = []

    for job in jobs:
        try:
            prompt = f"""
You are a job filter assistant for a fresher candidate in India.

Candidate Profile:
- Name: Vedant
- Level: Fresher (0-1 years experience)
- Preferred Roles: Full Stack Developer, AI Developer, Technical Support
- Preferred Locations: Nagpur, Pune, Remote
- Skills: Python, Basic AI knowledge, Web development basics

Job Details:
- Title: {job['title']}
- Company: {job['company']}
- Location: {job['location']}
- Experience: {job['experience']}

Answer these questions in EXACTLY this format:
RELEVANT: [YES / NO]
REASON: [One line why this is or isn't relevant]
APPLY: [YES / NO]
PRIORITY: [HIGH / MEDIUM / LOW]

Be strict:
- Only YES if job matches fresher level
- Only YES if location matches or is Remote
- Only YES if role matches candidate's skills
- NO for senior roles (VP, Lead, Manager, 5+ years)
"""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                max_tokens=150,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            result = response.choices[0].message.content.strip()

            relevant = "NO"
            reason = ""
            apply = "NO"
            priority = "LOW"

            for line in result.split('\n'):
                if line.startswith("RELEVANT:"):
                    relevant = line.replace("RELEVANT:", "").strip()
                elif line.startswith("REASON:"):
                    reason = line.replace("REASON:", "").strip()
                elif line.startswith("APPLY:"):
                    apply = line.replace("APPLY:", "").strip()
                elif line.startswith("PRIORITY:"):
                    priority = line.replace("PRIORITY:", "").strip()

            if relevant == "YES":
                job['reason'] = reason
                job['apply'] = apply
                job['priority'] = priority
                filtered_jobs.append(job)
                print(f"✅ RELEVANT: {job['title']} at {job['company']}")
                print(f"   Priority: {priority} | Reason: {reason}")
            else:
                print(f"❌ SKIPPED: {job['title']} — {reason}")

        except Exception as e:
            print(f"❌ Error filtering job: {e}")
            continue

    # Sort by priority
    priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    filtered_jobs.sort(key=lambda x: priority_order.get(x['priority'], 3))

    print(f"\n✅ Relevant jobs for Vedant: {len(filtered_jobs)}")
    return filtered_jobs


if __name__ == "__main__":
    # Test with sample jobs
    test_jobs = [
        {
            'title': 'Full Stack Developer',
            'company': 'Fireblaze AI School',
            'location': 'Nagpur, India',
            'experience': 'Fresher',
            'link': 'https://www.foundit.in'
        },
        {
            'title': 'Java Full Stack Developer - Vice President',
            'company': 'Some Bank',
            'location': 'Pune',
            'experience': '10+ Years',
            'link': 'https://www.foundit.in'
        },
        {
            'title': 'Technical Support Engineer',
            'company': 'TCS',
            'location': 'Pune',
            'experience': 'Fresher',
            'link': 'https://www.foundit.in'
        },
        {
            'title': 'AI Developer Intern',
            'company': 'StartupXYZ',
            'location': 'Remote',
            'experience': 'Fresher',
            'link': 'https://www.foundit.in'
        }
    ]

    results = filter_jobs_with_ai(test_jobs)

    print("\n--- Final Filtered Jobs ---")
    for i, job in enumerate(results):
        print(f"\n{i+1}. {job['title']} at {job['company']}")
        print(f"   📍 {job['location']} | 💼 {job['experience']}")
        print(f"   🎯 Priority: {job['priority']}")
        print(f"   💡 Reason: {job['reason']}")
        print(f"   🔗 {job['link']}")