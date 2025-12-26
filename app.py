from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# --- UPGRADED BUSINESS LOGIC ENGINE ---
class LoanEngine:
    @staticmethod
    def calculate_metrics(debt, ebitda, threshold):
        ratio = round(debt / ebitda, 2) if ebitda > 0 else 0
        headroom = round(((threshold - ratio) / threshold) * 100, 1)
        
        status, color = "COMPLIANT", "success"
        if ratio > threshold:
            status, color = "CRITICAL", "danger"
        elif headroom < 15:
            status, color = "WATCHLIST", "warning"
            
        return ratio, status, color, headroom

# --- ENHANCED INSTITUTIONAL STATE ---
loan_state = {
    "deal_id": "LMA-2025-DELTA",
    "verified": False,
    "jurisdiction": "LMA",
    "base_margin_bps": 225,
    "covenant_threshold": 3.50,
    "current_metrics": {"debt": 0, "ebitda": 0, "ratio": 0},
    "audit_log": []
}

@app.route('/')
def index(): return render_template('index.html')

@app.route('/workbench')
def workbench(): return render_template('workbench.html', loan=loan_state)

@app.route('/api/monitor', methods=['POST'])
def monitor():
    data = request.json
    debt = float(data['debt'])
    ebitda = float(data['ebitda'])
    
    ratio, status, color, headroom = LoanEngine.calculate_metrics(
        debt, ebitda, loan_state["covenant_threshold"]
    )
    
    # Update the "Live" state of the Digital Twin
    loan_state["current_metrics"] = {"debt": debt, "ebitda": ebitda, "ratio": ratio}
    loan_state["audit_log"].insert(0, f"{datetime.now().strftime('%H:%M:%S')} - Performance Updated: {ratio}x")
    
    return jsonify({
        "ratio": ratio, "status": status, "color": color, "headroom": headroom
    })

@app.route('/api/export', methods=['GET'])
def export_golden_record():
    """Generates the machine-readable Digital Twin Snapshot"""
    snapshot = {
        "metadata": {
            "version": "1.0",
            "timestamp": datetime.now().isoformat(),
            "deal_id": loan_state["deal_id"]
        },
        "legal_framework": {
            "jurisdiction": loan_state["jurisdiction"],
            "covenants": [{"type": "leverage", "limit": loan_state["covenant_threshold"]}]
        },
        "financial_state": loan_state["current_metrics"],
        "audit_trail": loan_state["audit_log"][:10]
    }
    return jsonify(snapshot)

if __name__ == '__main__':
    app.run(debug=True)
