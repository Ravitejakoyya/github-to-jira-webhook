from flask import Flask, request, jsonify
import os

app = Flask(__name__)

JIRA_DOMAIN = "ravitejakoyya.atlassian.net"
JIRA_API_URL = f"https://{JIRA_DOMAIN}/rest/api/3/issue"
EMAIL = "Ravitejakoyya651@gmail.com"
API_TOKEN = os.environ.get("JIRA_API_TOKEN")  # ✅ Fetch from environment variable
PROJECT_KEY = "SCRUM"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("✅ Webhook received:", data)
    return jsonify({"message": "Webhook received"}), 200

if __name__ == '__main__':
    app.run(port=5000)


# from flask import Flask, request, jsonify
# from requests.auth import HTTPBasicAuth
# import requests
# import json
# import os

# app = Flask(__name__)

# env:
#   JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}

# steps:
#   - name: Run Webhook Script
#     run: python webhook.py
#     env:
#       JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}


# # === JIRA CONFIG ===
# JIRA_DOMAIN = "ravitejakoyya.atlassian.net"
# JIRA_API_URL = f"https://{JIRA_DOMAIN}/rest/api/3/issue"
# EMAIL = "Ravitejakoyya651@gmail.com"
# API_TOKEN = os.environ.get("JIRA_API_TOKEN")
# PROJECT_KEY = "SCRUM"

# === JIRA TICKET CREATOR ===
def create_jira_ticket(summary, description):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "fields": {
            "project": {"key": PROJECT_KEY},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Task"}
        }
    })

    auth = HTTPBasicAuth(EMAIL, API_TOKEN)
    response = requests.post(JIRA_API_URL, data=payload, headers=headers, auth=auth)

    if response.status_code == 201:
        print("✅ Jira ticket created successfully.")
        return response.json()
    else:
        print("❌ Jira ticket creation failed:", response.status_code, response.text)
        return None

# === GITHUB WEBHOOK HANDLER ===
@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.json
    print("📩 GitHub Webhook Received")

    # Handle Pull Request creation
    if data.get('action') == 'opened' and 'pull_request' in data:
        pr = data['pull_request']
        title = pr['title']
        url = pr['html_url']
        description = f"A new Pull Request was opened:\n\n{url}"

        create_jira_ticket(summary=title, description=description)

    return jsonify({'status': 'received'}), 200

# === START SERVER ===
if __name__ == '__main__':
    app.run(port=5000)
