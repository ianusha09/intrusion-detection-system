"""
============================================================
  send.py — Alert Module
  Fill in your Twilio credentials below to enable SMS.
============================================================

SETUP:
  1. Sign up free at https://twilio.com
  2. Get Account SID, Auth Token, and a Twilio phone number
  3. Fill in the 4 variables below
  4. pip install twilio
"""

import datetime

# ── Fill these in ──
ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
AUTH_TOKEN  = "YOUR_TWILIO_AUTH_TOKEN"
FROM_PHONE  = "YOUR_TWILIO_PHONE_NUMBER"   # e.g. "+12345678901"
TO_PHONE    = "YOUR_PERSONAL_NUMBER"       # e.g. "+919876543210"

def sendSms():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_body = (
        f"INTRUSION ALERT!\n"
        f"Person detected in restricted zone.\n"
        f"Time: {timestamp}"
    )

    print("-" * 45)
    print(f"[ALERT LOG] {timestamp} — Intrusion detected!")
    print("-" * 45)

    if "YOUR_" in ACCOUNT_SID:
        print("[WARNING] Twilio not configured. SMS skipped.")
        return

    try:
        from twilio.rest import Client
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            body=message_body,
            from_=FROM_PHONE,
            to=TO_PHONE
        )
        print(f"[SMS SENT] SID: {message.sid}")
    except ImportError:
        print("[ERROR] Run: pip install twilio")
    except Exception as e:
        print(f"[ERROR] SMS failed: {e}")