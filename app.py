from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# --- BUSINESS LOGIC ENGINE ---
class LoanEngine:
    @staticmethod
    def calculate_compliance(debt, ebitda, threshold):
        ratio = round(debt / ebitda, 2) if ebitda > 0 else 0
        headroom = round(((threshold - ratio) / threshold) * 100, 1)
        
        # Predictive Status Logic
        if ratio > threshold: return ratio, "CRITICAL", "danger", headroom
        if headroom < 15: return ratio, "WATCHLIST", "warning", headroom
        return ratio, "COMPLIANT", "success", headroom

    @staticmethod
    def calculate_margin(base_bps, esg_met):
        # Programmatic ESG Ratchet: -5bps incentive
        adjustment = -5 if esg_met else 0
        return base_bps + adjustment

# --- PERSISTENT DIGITAL TWIN STATE ---
loan_state = {
    "deal_id": "LMA-2025-DELTA",
    "verified": False,
    "jurisdiction": "LMA",
    "covenant_threshold": 3.50,
    "base_margin": 225,
    "breach_start_date": None,
    "current_metrics": {"ratio": 0, "status": "Inactive"},
    "audit_log": []
}

@app.route('/')
def index(): return render_template('index.html')

@app.route('/workbench')
def workbench(): return render_template('workbench.html', loan=loan_state)

@app.route('/api/verify', methods=['POST'])
def verify():
    text = request.json.get('text', '').lower()
    # Semantic Anchor Check
    if "security" in text and "negative pledge" in text:
        loan_state["verified"] = True
        return jsonify({"success": True, "message": "LMA Standard Clause Verified"})
    return jsonify({"success": False, "message": "Verification Failed"})

@app.route('/api/monitor', methods=['POST'])
def monitor():
    data = request.json
    debt, ebitda = float(data['debt']), float(data['ebitda'])
    esg_met = data.get('esg_met', False)
    
    ratio, status, color, headroom = LoanEngine.calculate_compliance(debt, ebitda, loan_state["covenant_threshold"])
    final_margin = LoanEngine.calculate_margin(loan_state["base_margin"], esg_met)
    
    # Cure Period Logic
    if status == "CRITICAL":
        if not loan_state["breach_start_date"]:
            loan_state["breach_start_date"] = datetime.now()
        days_remaining = 10 - (datetime.now() - loan_state["breach_start_date"]).days
        status = f"CURE PERIOD ({max(0, days_remaining)}d left)"
    else:
        loan_state["breach_start_date"] = None

    loan_state["current_metrics"] = {"ratio": ratio, "status": status, "margin": final_margin}
    return jsonify({
        "ratio": ratio, "status": status, "color": color, 
        "headroom": headroom, "margin": final_margin
    })

@app.route('/api/export')
def export():
    return jsonify({
        "metadata": {"deal_id": loan_state["deal_id"], "ts": datetime.now().isoformat()},
        "legal_logic": {"covenant_max": loan_state["covenant_threshold"], "jurisdiction": "LMA"},
        "performance": loan_state["current_metrics"],
        "audit_trail": loan_state["audit_log"]
    })

if __name__ == '__main__':
    app.run(debug=True)
