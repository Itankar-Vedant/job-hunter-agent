
import sys
print("🚀 AGENT STARTING...", flush=True)
sys.stdout.flush()

import schedule
import time
from job_fetcher import fetch_jobs
from ai_filter import filter_jobs_with_ai
from whatsapp_sender import send_job_alerts
from datetime import datetime


def run_agent():
    print(f"\n🤖 Agent running at {datetime.now().strftime('%H:%M %d-%m-%Y')}", flush=True)
    print("=" * 50, flush=True)

    try:
        print("📡 Step 1: Fetching jobs...", flush=True)
        jobs = fetch_jobs()
        print(f"✅ Fetched {len(jobs)} jobs", flush=True)

        if not jobs:
            print("❌ No jobs fetched.", flush=True)
            return

        print("🧠 Step 2: AI filtering...", flush=True)
        filtered_jobs = filter_jobs_with_ai(jobs)
        print(f"✅ Filtered to {len(filtered_jobs)} relevant jobs", flush=True)

        print("📱 Step 3: Sending WhatsApp...", flush=True)
        send_job_alerts(filtered_jobs)
        print("✅ WhatsApp sent!", flush=True)

    except Exception as e:
        print(f"❌ ERROR: {e}", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("✅ Agent file loaded successfully", flush=True)
    print("⏰ Scheduling daily at 9AM...", flush=True)

    run_agent()

    schedule.every().day.at("11:00").do(run_agent)

    while True:
        schedule.run_pending()
        time.sleep(60)