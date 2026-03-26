import sys
import time
import schedule
from datetime import datetime

print("🚀 AGENT STARTING...", flush=True)

from job_fetcher import fetch_jobs
from ai_filter import filter_jobs_with_ai
from whatsapp_sender import send_job_alerts

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
        print("✅ Done!", flush=True)

    except Exception as e:
        print(f"❌ ERROR: {e}", flush=True)
        import traceback
        traceback.print_exc()
        print("⚠️ Agent will retry at next scheduled time", flush=True)

def heartbeat():
    print(f"💓 Agent alive at {datetime.now().strftime('%H:%M %d-%m-%Y')}", flush=True)

if __name__ == "__main__":
    print("✅ Agent loaded successfully", flush=True)
    print("⏰ Scheduled to run daily at 9AM IST", flush=True)

    # Schedule daily at 9AM IST
    schedule.every().day.at("09:00").do(run_agent)

    # Heartbeat every 30 mins so Railway knows agent is alive
    schedule.every(30).minutes.do(heartbeat)

    # Run once immediately on start
    run_agent()

    print("\n⏳ Waiting for next scheduled run...", flush=True)

    # Keep running forever — never exit
    while True:
        try:
            schedule.run_pending()
            time.sleep(30)
        except Exception as e:
            print(f"⚠️ Loop error: {e} — continuing...", flush=True)
            time.sleep(30)
            continue