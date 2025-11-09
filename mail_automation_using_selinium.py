from __future__ import print_function
import os.path
import base64
import pickle
from email.mime.text import MIMEText

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def gmail_send_message():
    creds = None
    print("📁 Current working directory:", os.getcwd())

    CREDENTIAL_PATH = r"C:\Users\prave\OneDrive\Desktop\60 Days Ai Challenge\Praveen\Selinium\credentials.json"
    if not os.path.exists(CREDENTIAL_PATH):
        print("\n❌ ERROR: credentials.json NOT FOUND at path:")
        print(CREDENTIAL_PATH)
        return

    if os.path.exists("token.pickle"):
        print("🔐 Using saved Gmail token...")
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔁 Refreshing token...")
            creds.refresh(Request())
        else:
            print("🌐 Opening Google login page...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIAL_PATH, SCOPES)
            creds = flow.run_local_server(port=8000, open_browser=True)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
            print("💾 Token saved — next time no login required.")

    service = build("gmail", "v1", credentials=creds)

    # ✅ Updated recipient here
    message = create_message(
        "bezhilarasi0005@gmail.com",
        "Python Gmail Test ✅",
        "Hello Ezhilaras,\n\nThis email was sent by your son Praveen using Python + Gmail API.\n\n— Automated Mail"
    )

    print("🚀 Sending email...")
    sent = service.users().messages().send(userId="me", body=message).execute()
    print(f"\n✅ Email sent successfully!\n📩 Message ID: {sent['id']}")

if __name__ == "__main__":
    gmail_send_message()
