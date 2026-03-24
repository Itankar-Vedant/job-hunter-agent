import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def send_job_alerts(jobs):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_WHATSAPP_FROM")
    to_number = os.getenv("TWILIO_WHATSAPP_TO")

    client = Client(account_sid, auth_token)

    if not jobs:
        message = "🤖 *Job Hunter Agent*\n\nNo new relevant jobs found today. Will check again soon!"
        client.messages.create(
            from_=from_number,
            body=message,
            to=to_number
        )
        print("✅ Sent no jobs message")
        return

    # Send header message
    header = f"🤖 *Good Morning Vedant!*\n\n🎯 Found *{len(jobs)} relevant jobs* for you today!\n\n"
    client.messages.create(
        from_=from_number,
        body=header,
        to=to_number
    )

    # Send each job as separate message
    for i, job in enumerate(jobs[:10]):
        priority_emoji = "🔴" if job['priority'] == "HIGH" else "🟡" if job['priority'] == "MEDIUM" else "🟢"

        message = f"""{priority_emoji} *Job {i+1}*

📌 *{job['title']}*
🏢 {job['company']}
📍 {job['location']}
💼 {job['experience']}
🎯 Priority: {job['priority']}
💡 {job['reason']}

🔗 Apply: {job['link']}"""

        client.messages.create(
            from_=from_number,
            body=message,
            to=to_number
        )
        print(f"✅ Sent alert for: {job['title']} at {job['company']}")

    # Send footer
    footer = "━━━━━━━━━━━━━━━\n💪 Go get it Vedant! Apply today!\n🤖 Your Job Hunter Agent"
    client.messages.create(
        from_=from_number,
        body=footer,
        to=to_number
    )

    print(f"\n✅ All {len(jobs[:10])} job alerts sent to WhatsApp!")


if __name__ == "__main__":
    test_jobs = [
        {
            'title': 'Full Stack Developer',
            'company': 'Fireblaze AI School',
            'location': 'Nagpur, India',
            'experience': 'Fresher',
            'priority': 'HIGH',
            'reason': 'Perfect fresher role matching your skills in Nagpur',
            'link': 'https://www.foundit.in'
        },
        {
            'title': 'Technical Support Engineer',
            'company': 'TCS',
            'location': 'Pune',
            'experience': 'Fresher',
            'priority': 'HIGH',
            'reason': 'Top company, fresher role, matches location',
            'link': 'https://www.foundit.in'
        }
    ]

    print("Testing WhatsApp sender...\n")
    send_job_alerts(test_jobs)