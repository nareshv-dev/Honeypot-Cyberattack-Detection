from flask import Flask, request, render_template_string
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# Log file setup
LOG_FILE = "honeypot_logs.csv"
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=["Timestamp", "IP Address", "Forwarded IP", "User-Agent", "Path", "Headers"]).to_csv(LOG_FILE, index=False)

# Fake webpage template
FAKE_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Login</title>
</head>
<body>
    <h2>Unauthorized Access Prohibited</h2>
    <p>If you are not authorized, please exit.</p>
</body>
</html>
"""

# Function to log request details
def log_request(req):
    real_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    log_data = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "IP Address": request.remote_addr,
        "Forwarded IP": real_ip,
        "User-Agent": request.headers.get("User-Agent", "Unknown"),
        "Path": request.path,
        "Headers": str(request.headers)
    }
    df = pd.DataFrame([log_data])
    df.to_csv(LOG_FILE, mode='a', header=False, index=False)

@app.route('/')
def honeypot():
    log_request(request)
    return render_template_string(FAKE_PAGE)

@app.route('/report')
def view_report():
    if os.path.exists(LOG_FILE):
        data = pd.read_csv(LOG_FILE)
        return data.to_html()
    return "No logs available."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
