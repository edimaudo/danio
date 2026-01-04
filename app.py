import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

# Synthetic portfolio data
MOCK_PORTFOLIO = [
    {"id": "SLO-9921", "name": "Project Apollo - Senior Secured", "type": "Term Loan B", "margin": "350bps", "status": "Normalized", "date": "2024-05-10"},
    {"id": "SLO-8842", "name": "Starlight Corp - RCF 2024", "type": "Revolver", "margin": "275bps", "status": "Normalized", "date": "2024-05-12"},
    {"id": "SLO-7731", "name": "Horizon Infrastructure - Bridge", "type": "Bridge Loan", "margin": "450bps", "status": "Verification Pending", "date": "2024-05-14"},
    {"id": "SLO-6610", "name": "Apex Manufacturing - Term Loan", "type": "Term Loan A", "margin": "325bps", "status": "Normalized", "date": "2024-05-15"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/workstation')
def workstation():
    """Portfolio dashboard showing previously scanned documents."""
    return render_template('app.html', records=MOCK_PORTFOLIO)

@app.route('/reader')
def reader():
    """Dedicated view for processing and analyzing a single document."""
    return render_template('reader.html')

@app.route('/analyze', methods=['POST'])
def analyze_document():
    # Simulated extraction of a Standardized Loan Object (SLO)
    slo_data = {
        "metadata": {"normalization_version": "1.0.4", "confidence_score": 0.96},
        "instrument_intelligence": {
            "facility_type": "Term Loan B",
            "governing_law": "New York",
            "currency": "USD"
        },
        "economic_terms": {
            "margin_bps": 375,
            "floor_pct": 1.00,
            "maturity_date": "2030-06-15"
        },
        "covenants": {
            "leverage_ceiling": "4.25x",
            "interest_coverage": "2.50x",
            "status": "In-Compliance"
        }
    }
    return jsonify(slo_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
