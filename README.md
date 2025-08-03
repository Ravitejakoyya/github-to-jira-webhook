# github-to-jira-webhook

🚀 Automated Jira Ticket Creation from GitHub Using Python
✨ Build an end-to-end integration with GitHub, Flask & Jira
📌 Goal
Create a Jira task automatically whenever a Pull Request is opened on a GitHub repository using a simple Python Flask webhook.

This is a great way to streamline DevOps workflows, enhance project visibility, and reduce manual Jira entry.

🧰 Tools Used
🐍 Python (Flask) — lightweight server to receive GitHub events
🔁 GitHub Webhooks — trigger the event
🧾 Jira Cloud REST API — create tickets programmatically
🌐 Localtunnel — expose your app or deploy it online
✅ Prerequisites
Tool Description Jira Cloud Account Sign up at atlassian.com GitHub Repo To trigger events from Python 3.8+ Install it from python.org pip For Python packages (Optional) Git To push code to GitHub

🔁 Overview of the Process
Set up Jira: generate API token & get project key
Build a Flask app that handles GitHub webhooks
Run it locally
Expose it to the internet (with localtunnel)
Set up GitHub webhook
Trigger by opening a pull request

🧩 Step 1: Jira Setup
🔐 1.1 Generate Jira API Token
Go to: https://id.atlassian.com/manage/api-tokens
Click Create API token
Name it and copy the token (you won’t see it again)
🔒 Save the token securely.

<img width="1850" height="805" alt="image" src="https://github.com/user-attachments/assets/12055df2-6656-401d-9059-b51a3550ead3" />


🧾 1.2 Get Your Jira Project Key
Go to your Jira dashboard
Click into any project
Look at an issue ID like SCRUM-23 → Project Key is SCRUM

<img width="1860" height="742" alt="image" src="https://github.com/user-attachments/assets/49f1d032-8114-43c8-98b7-55424517912f" />


🧩 Step 2: Create Flask Webhook App
🧪 2.1 Set up Python project
mkdir github-to-jira
cd github-to-jira
python -m venv venv
venv\Scripts\activate     # Windows
# OR
venv\Scripts\activate.bat
# OR
source venv/bin/activate  # macOS/Linux

📦 2.2 Install dependencies
pip install Flask requests python-dotenv

📁 2.3 Project files
requirements.txt
Flask
requests
python-dotenv

#webhook.py

https://github.com/Ravitejakoyya/github-to-jira-webhook/blob/main/webhook.py

from flask import Flask, request, jsonify
import os, requests
from requests.auth import HTTPBasicAuth
app = Flask(__name__)
# Your Jira config
JIRA_DOMAIN = "your-domain.atlassian.net"
EMAIL = "you@example.com"
API_TOKEN = os.environ.get("JIRA_API_TOKEN")
PROJECT_KEY = "SCRUM"
JIRA_API_URL = f"https://{JIRA_DOMAIN}/rest/api/3/issue"
# Function to create a Jira issue
def create_jira_ticket(pr_data):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "fields": {
            "project": {"key": PROJECT_KEY},
            "summary": f"[AUTO] {pr_data['title']}",
            "description": pr_data.get("body", "No description provided."),
            "issuetype": {"name": "Task"}
        }
    }
    response = requests.post(JIRA_API_URL, json=payload, headers=headers, auth=HTTPBasicAuth(EMAIL, API_TOKEN))
    print("🔍 Jira response code:", response.status_code)
    print("🔍 Jira response body:", response.text)
    return response.status_code == 201
    
# Webhook endpoint
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
        print("✅ Jira ticket created." if success else "❌ Failed to create Jira ticket.")
    else:
        print("⚠️ Not a pull_request event")
    return jsonify({"status": "ok"}), 200
    
# Start the Flask server
if __name__ == '__main__':
    app.run(port=5000)

<img width="1919" height="1021" alt="image" src="https://github.com/user-attachments/assets/f28a321b-554a-4a72-a30f-e3a63961ff12" />


🧩 Step 3: Run the Flask Server
Set your Jira token in your environment:

# Windows PowerShell
$env:JIRA_API_TOKEN = "your_jira_api_token"
# OR macOS/Linux
export JIRA_API_TOKEN="your_jira_api_token"
Atlassian account — To create a API Token

<img width="1865" height="535" alt="image" src="https://github.com/user-attachments/assets/52dcebfa-4e57-42dd-96af-1f0dcab6040e" />

Run it:

python webhook.py
Your server will be live at http://localhost:5000

🧩 Step 4: Expose Your Local Server
Install & Run LocalTunnel to Expose Server

If you face any issues while installing the LocalTunnel Follow this one:
1.Open POWERSHELL with admin

powershell — RUN AS adminstrator

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

2. Come to vs code and run the below command
npx localtunnel — port 5000

You’ll get a URL like:

```
https://abcd1234.ngrok.io
```

Keep this terminal open — it’s your public URL.

🛰 Option: LocalTunnel (No install needed if you have npm)
npm install -g localtunnel
lt --port 5000 --subdomain githubtojira
This gives you a public URL like:

https://githubtojira.loca.lt/webhook

🧩 Step 5: Connect GitHub Webhook
Open your GitHub repo → Settings → Webhooks
Click Add Webhook
Set:
Payload URL: https://githubtojira.loca.lt/webhook
Content type: application/json
Event type: Only “Pull requests”
Click Save

<img width="1831" height="905" alt="image" src="https://github.com/user-attachments/assets/d1f26262-891f-425d-a295-701e0a9163dd" />


🧩 Step 6: Test It 🎉
Create a new branch:
git checkout -b feature-test
git push origin feature-test
Go to GitHub → Open a new pull request
In the Flask terminal, you should see:
📬 GitHub webhook received
🔍 Jira response code: 201
✅ Jira ticket created.

<img width="1415" height="507" alt="image" src="https://github.com/user-attachments/assets/f5d77bd6-714b-48d7-81fa-d3688ad4e0d6" />


Go to Jira → You’ll see the new task created 🎯

<img width="1854" height="772" alt="image" src="https://github.com/user-attachments/assets/7be44bc1-d476-4a99-bd2e-6a06413ae70b" />


⚙️ How It Works — Step by Step
This integration connects your GitHub development workflow directly with Jira, allowing automatic ticket creation whenever a Pull Request is opened. Here’s how the system works behind the scenes:

When a developer opens a pull request on GitHub, a webhook event is triggered. GitHub sends a POST request containing pull request metadata — like title, description, and author — to your Flask server’s /webhook endpoint.

Your Flask application, acting as a lightweight webhook receiver, captures this incoming data. It parses the payload and checks if the event type is indeed a pull request. If it is, the Flask server extracts the relevant information (PR title and body) and prepares it for Jira.

Then comes the core part: your Flask app makes an authenticated API call to Jira. Using basic auth (email and API token), it sends a structured request to Jira’s REST API with the necessary fields — such as the project key, issue summary, description, and issue type (e.g., Task).

If everything is configured correctly, Jira processes this request and creates a new task under your specified project. Meanwhile, your Flask server logs a confirmation message like “✅ Jira ticket created.” All of this happens automatically, without any manual input.

This seamless bridge ensures that every pull request made on GitHub has a corresponding task in Jira, keeping your project tracking accurate and your workflow streamlined.

✅ You’re Done!
You now have:
✔ A webhook server in Flask
✔ A secure GitHub → Jira automation
✔ One less manual task to worry about

🧠 Want to Go Further?
Create Jira tickets for other GitHub events (commits, issues)
Auto-update Jira status when PR is merged
Send PR comments to Jira
Add Slack or email notifications
🙌 Final Thoughts
This automation saves time, improves traceability, and integrates your dev workflow seamlessly with project management.

🔗 Let’s Connect
If you found this helpful:

⭐️ Follow me on LinkedIn — https://www.linkedin.com/in/koyya-raviteja/
⭐️ Follow me on GitHub — https://github.com/Ravitejakoyya/
⭐️ Follow me on Medium - https://medium.com/@ravitejakoyya651/

💬 Drop your questions or improvements in the comments
Happy Automating! ⚙️🧠💡

