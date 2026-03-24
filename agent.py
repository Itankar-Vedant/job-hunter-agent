import schedule
import time
from job_fetcher import fetch_foundit_jobs
from ai_filter import filter_jobs_with_ai
from whatsapp_sender import send_job_alerts
from datetime import datetime

def run_agent():
    print(f"\n🤖 Job Hunter Agent Started at {datetime.now().strftime('%H:%M %d-%m-%Y')}")
    print("=" * 50)

    # Step 1 — Fetch jobs
    print("\n📡 Step 1: Fetching jobs from Foundit...")
    jobs = fetch_foundit_jobs()

    if not jobs:
        print("❌ No jobs fetched. Will retry next time.")
        return

    # Step 2 — Filter with AI
    print("\n🧠 Step 2: AI filtering relevant jobs...")
    filtered_jobs = filter_jobs_with_ai(jobs)

    if not filtered_jobs:
        print("❌ No relevant jobs found after filtering.")
        send_job_alerts([])
        return

    # Step 3 — Send WhatsApp alerts
    print("\n📱 Step 3: Sending WhatsApp alerts...")
    send_job_alerts(filtered_jobs)

    print(f"\n✅ Agent completed at {datetime.now().strftime('%H:%M %d-%m-%Y')}")
    print(f"📊 Summary: Fetched {len(jobs)} jobs → Filtered to {len(filtered_jobs)} relevant jobs → Sent to WhatsApp")
    print("=" * 50)


if __name__ == "__main__":
    print("🚀 Job Hunter Agent Launched!")
    print("⏰ Will run every morning at 9:00 AM automatically")
    print("Press Ctrl+C to stop\n")

    # Run immediately on start
    run_agent()

    # Then run every day at 9AM
    schedule.every().day.at("09:00").do(run_agent)

    while True:
        schedule.run_pending()
        time.sleep(60)