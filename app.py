from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# --- INSTITUTIONAL ENGINE ---
loan_state = {
    "verified": False,
    "threshold": 3.50,
    "base_margin": 225, # bps
    "breach_timestamp": None
}

@app.route('/')
def index(): return render_template('index.html')

@app.route('/workbench')
def workbench(): return render_template('workbench.html')

@app.route('/api/verify', methods=['POST'])
def verify():
    text = request.json.get('text', '').lower()
    # Semantic logic for Institutional Standards
    if "security" in text and "negative pledge" in text:
        loan_state["verified"] = True
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route('/api/monitor', methods=['POST'])
def monitor():
    data = request.json
    debt = float(data.get('debt', 0))
    ebitda = float(data.get('ebitda', 1))
    esg_met = data.get('esg_met', False)
    
    ratio = round(debt / ebitda, 2)
    
    # 1. Calculate ESG Margin Ratchet (-5bps if target met)
    current_margin = loan_state["base_margin"] - (5 if esg_met else 0)
    
    # 2. Compliance Logic & Headroom
    headroom = round(((loan_state["threshold"] - ratio) / loan_state["threshold"]) * 100, 1)
    
    status = "COMPLIANT"
    color = "success"
    
    if ratio > loan_state["threshold"]:
        status = "BREACH"
        color = "danger"
        # 3. Cure Period Logic (Simplified)
        status = "CURE PERIOD (10D)"
    elif headroom < 15:
        status = "WATCHLIST"
        color = "warning"

    return jsonify({
        "ratio": f"{ratio}x",
        "status": status,
        "color": color,
        "margin": f"{current_margin} bps",
        "headroom": f"{headroom}%"
    })
