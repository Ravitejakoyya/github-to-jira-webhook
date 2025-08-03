from flask import Flask, request, jsonify
import os
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Jira Configuration
JIRA_DOMAIN = "ravitejakoyya.atlassian.net"
JIRA_API_URL = f"https://{JIRA_DOMAIN}/rest/api/3/issue"
EMAIL = "Ravitejakoyya651@gmail.com"
API_TOKEN = os.environ.get("JIRA_API_TOKEN")
PROJECT_KEY = "SCRUM"

# Create Jira Ticket
def create_jira_ticket(pr_data):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "fields": {
            "project": {
                "key": PROJECT_KEY
            },
            "summary": f"[AUTO] {pr_data['title']}",
            "description": pr_data.get("body", "No description provided."),
            "issuetype": {
                "name": "Task"
            }
        }
    }

    response = requests.post(
        JIRA_API_URL,
        headers=headers,
        json=payload,
        auth=HTTPBasicAuth(EMAIL, API_TOKEN)
    )

    print("🔍 Jira response code:", response.status_code)
    print("🔍 Jira response body:", response.text)

    return response.status_code == 201

# GitHub Webhook Endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("📬 GitHub webhook received")

    if "pull_request" in data:
        pr_data = {
            "title": data["pull_request"]["title"],
            "body": data["pull_request"]["body"]
        }
        success = create_jira_ticket(pr_data)
        if success:
            print("✅ Jira ticket created.")
        else:
            print("❌ Failed to create Jira ticket.")
    else:
        print("⚠️ Not a pull_request event")

    return jsonify({"status": "ok"}), 200

# Start Server
if __name__ == '__main__':
    app.run(port=5000)

#pushed to github
# Set the JIRA_API_TOKEN environment variable before running the app
# --- IGNORE ---
# --- IGNORE ---