import os
from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Institutional Credit Ledger Data
MOCK_LEDGER = [
    {
        "id": "SLO-8829", 
        "name": "Global Tech Acquisitions", 
        "type": "Term Loan B", 
        "margin": "S+350", 
        "law": "New York", 
        "maturity": "2030-06-15",
        "leverage_covenant": "4.50x",
        "compliance": "Compliant",
        "last_verified": "2024-05-10"
    },
    {
        "id": "SLO-7712", 
        "name": "Oceanic Wind Portfolio", 
        "type": "RCF", 
        "margin": "S+275", 
        "law": "English", 
        "maturity": "2028-12-01",
        "leverage_covenant": "3.25x",
        "compliance": "Compliant",
        "last_verified": "2024-05-12"
    },
    {
        "id": "SLO-9901", 
        "name": "Starlight Real Estate", 
        "type": "Bridge Loan", 
        "margin": "S+450", 
        "law": "New York", 
        "maturity": "2025-03-20",
        "leverage_covenant": "N/A",
        "compliance": "Pending Review",
        "last_verified": "N/A"
    },
    {
        "id": "SLO-5542", 
        "name": "Industrial Logistics", 
        "type": "Term Loan A", 
        "margin": "S+325", 
        "law": "Delaware", 
        "maturity": "2029-09-30",
        "leverage_covenant": "4.00x",
        "compliance": "Compliant",
        "last_verified": "2024-05-14"
    },
    {
        "id": "SLO-4410", 
        "name": "Apex Manufacturing", 
        "type": "Term Loan B", 
        "margin": "S+400", 
        "law": "New York", 
        "maturity": "2031-11-15",
        "leverage_covenant": "5.25x",
        "compliance": "Breach Alert",
        "last_verified": "2024-05-15"
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/workstation')
def workstation():
    """Main Credit Ledger dashboard with dynamic metrics."""
    # 1. Calculation for Portfolio Facilities: Total count of records
    total_facilities = len(MOCK_LEDGER)
    
    # 2. Calculation for Data Health: % of compliant facilities
    compliant_count = len([r for r in MOCK_LEDGER if r['compliance'] == 'Compliant'])
    data_health = round((compliant_count / total_facilities) * 100, 1) if total_facilities > 0 else 0
    
    return render_template(
        'app.html', 
        records=MOCK_LEDGER, 
        total_facilities=total_facilities, 
        data_health=data_health
    )

@app.route('/reader')
def reader():
    """Workflow interface. Generates dynamic data if no ID provided (New Agreement)."""
    record_id = request.args.get('id')
    record = next((r for r in MOCK_LEDGER if r['id'] == record_id), None)
    
    # Generate random data for the "OCR" simulation if it's a new agreement
    if not record:
        companies = ["Vanguard Systems", "Apex Global", "Titan Infrastructure", "Horizon Logistics"]
        margins = ["S+300", "S+325", "S+400", "S+275"]
        laws = ["New York", "English Law", "Delaware"]
        
        record = {
            "id": f"SLO-{random.randint(1000, 9999)}",
            "name": random.choice(companies),
            "type": "Term Loan B",
            "margin": random.choice(margins),
            "law": random.choice(laws),
            "maturity": f"203{random.randint(0,2)}-12-31",
            "leverage_covenant": f"{random.uniform(3.5, 5.0):.2f}x",
            "compliance": "Compliant"
        }
    
    return render_template('reader.html', record=record, is_new=(not record_id))

@app.route('/commit', methods=['POST'])
def commit():
    """Adds the newly harmonized record to the ledger."""
    data = request.json
    data['last_verified'] = datetime.now().strftime("%Y-%m-%d")
    MOCK_LEDGER.insert(0, data)
    return jsonify({"status": "success"})

@app.route('/analyze', methods=['POST'])
def analyze():
    """Simulated high-fidelity extraction for the standardization process."""
    return jsonify({
        "instrument": "Term Loan B",
        "jurisdiction": "New York",
        "margin_grid": "S+375 (Step-downs at 3.0x)",
        "maturity": "2030-06-15",
        "financial_covenants": "Max Net Leverage 4.50x",
        "status": "Harmonized"
    })

@app.route('/documentation')
def documentation():
    """Serves the institutional documentation and framework guide."""
    return render_template('documentation.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
