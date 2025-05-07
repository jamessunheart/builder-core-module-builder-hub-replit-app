from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Service registry (can later be externalized)
services = {
    "telegram_alert_bot": "https://your-telegram-bot.repl.co"
}

@app.route("/health")
def health():
    return {"status": "Builder Hub is online"}

@app.route("/route/<service>", methods=["POST"])
def route(service):
    if service not in services:
        return {"error": f"Service '{service}' not registered."}, 404

    payload = request.json
    try:
        res = requests.post(services[service], json=payload)
        return res.json(), res.status_code
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    services[data["name"]] = data["url"]
    return {"status": "Service registered", "service": data["name"]}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)  # Replit default port