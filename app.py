import os
from flask import Flask, render_template, request, jsonify

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
    """Main Credit Ledger dashboard."""
    return render_template('app.html', records=MOCK_LEDGER)

@app.route('/reader')
def reader():
    """Workflow interface. Defaults to analysis view if id is provided."""
    record_id = request.args.get('id')
    record = next((r for r in MOCK_LEDGER if r['id'] == record_id), None)
    return render_template('reader.html', record=record)

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
