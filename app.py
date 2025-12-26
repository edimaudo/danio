from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

loan_state = {
    "deal_id": "STP-2025-DELTA",
    "verified": False,
    "covenant_threshold": 3.50,
    "current_metrics": {"ratio": 0, "status": "Pending Verification"}
}

@app.route('/')
def index(): return render_template('index.html')

@app.route('/workbench')
def workbench(): return render_template('workbench.html', loan=loan_state)

@app.route('/api/verify', methods=['POST'])
def verify():
    text = request.json.get('text', '').lower()
    # Verification against Institutional Negative Pledge Standards
    if "security" in text and "negative pledge" in text:
        loan_state["verified"] = True
        return jsonify({"success": True, "message": "Institutional Standard Verified"})
    return jsonify({"success": False, "message": "Standard Anchors Missing: Verification Failed"})

@app.route('/api/monitor', methods=['POST'])
def monitor():
    data = request.json
    debt, ebitda = float(data['debt']), float(data['ebitda'])
    ratio = round(debt / ebitda, 2) if ebitda > 0 else 0
    headroom = round(((3.5 - ratio) / 3.5) * 100, 1)
    
    status, color = "COMPLIANT", "success"
    if ratio > 3.5: status, color = "CRITICAL BREACH", "danger"
    elif headroom < 15: status, color = "WATCHLIST", "warning"

    return jsonify({"ratio": ratio, "status": status, "color": color, "headroom": headroom})
