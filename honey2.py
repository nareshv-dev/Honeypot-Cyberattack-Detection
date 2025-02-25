from flask import Flask, request, render_template
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# Log file setup
LOG_FILE = "honeypot_logs.csv"
COLUMNS = ["Timestamp", "IP Address", "Forwarded IP", "User-Agent", "Path", "Headers", "Search Query"]

# Ensure the log file is properly initialized
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=COLUMNS).to_csv(LOG_FILE, index=False)

# Function to log request details
def log_request(req, search_query=""):
    real_ip = req.headers.get("X-Forwarded-For", req.remote_addr)
    log_data = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "IP Address": req.remote_addr,
        "Forwarded IP": real_ip,
        "User-Agent": req.headers.get("User-Agent", "Unknown"),
        "Path": req.path,
        "Headers": str(req.headers),
        "Search Query": search_query
    }
    df = pd.DataFrame([log_data])
    
    # Append without corrupting the CSV format
    df.to_csv(LOG_FILE, mode='a', header=False, index=False)

@app.route('/')
def homepage():
    log_request(request)
    return render_template("index.html")

@app.route('/search')
def search():
    search_query = request.args.get("query", "Unknown")
    log_request(request, search_query)
    return f"<h3>Showing results for: {search_query}</h3>"

@app.route('/report')
def view_report():
    try:
        if os.path.exists(LOG_FILE):
            data = pd.read_csv(LOG_FILE, usecols=COLUMNS, on_bad_lines="skip")
            return data.to_html()
    except Exception as e:
        return f"Error loading logs: {str(e)}"
    return "No logs available."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
