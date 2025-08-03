from flask import Flask, request, jsonify
import os

app = Flask(__name__)

JIRA_DOMAIN = "ravitejakoyya.atlassian.net"
JIRA_API_URL = f"https://{JIRA_DOMAIN}/rest/api/3/issue"
EMAIL = "Ravitejakoyya651@gmail.com"
API_TOKEN = os.environ.get("JIRA_API_TOKEN")  # ✅ Fetch from environment variable
PROJECT_KEY = "SCRUM"

from requests.auth import HTTPBasicAuth
import requests
import json 

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("✅ Webhook received:", data)
    return jsonify({"message": "Webhook received"}), 200

if __name__ == '__main__':
    app.run(port=5000)

#Everything below this line is commented out for clarity
# # GitHub Actions Workflow Example
# # This is a sample GitHub Actions workflow that runs the webhook script   

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
# def create_jira_ticket(summary, description):
#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/json"
#     }

#     payload = json.dumps({
#         "fields": {
#             "project": {"key": PROJECT_KEY},
#             "summary": summary,
#             "description": description,
#             "issuetype": {"name": "Task"}
#         }
#     })

#     auth = HTTPBasicAuth(EMAIL, API_TOKEN)
#     response = requests.post(JIRA_API_URL, data=payload, headers=headers, auth=auth)

#     if response.status_code == 201:
#         print("✅ Jira ticket created successfully.")
#         return response.json()
#     else:
#         print("❌ Jira ticket creation failed:", response.status_code, response.text)
#         return None

import requests

def create_jira_ticket(pr_data):
    url = "https://ravitejakoyya.atlassian.net/rest/api/3/issue"
    auth = (EMAIL, API_TOKEN)
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
            "description": pr_data.get("body", "No description."),
            "issuetype": {
                "name": "Task"
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers, auth=auth)
    print("Jira Response:", response.status_code, response.text)

    return response.status_code == 201

print("🔍 Jira response code:", response.status_code)
print("🔍 Jira response body:", response.text)


# === GITHUB WEBHOOK HANDLER ===
# @app.route('/webhook', methods=['POST'])
# def github_webhook():
#     data = request.json
#     print("📩 GitHub Webhook Received")

#     # Handle Pull Request creation
#     if data.get('action') == 'opened' and 'pull_request' in data:
#         pr = data['pull_request']
#         title = pr['title']
#         url = pr['html_url']
#         description = f"A new Pull Request was opened:\n\n{url}"

#         create_jira_ticket(summary=title, description=description)

#     return jsonify({'status': 'received'}), 200

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
    return jsonify({"status": "ok"}), 200


# === START SERVER ===
if __name__ == '__main__':
    app.run(port=5000)
