import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB limit

@app.route('/')
def index():
    """Renders the institutional landing page."""
    return render_template('index.html')

@app.route('/workstation')
def workstation():
    """Renders the dual-view analysis workstation."""
    return render_template('app.html')

@app.route('/analyze', methods=['POST'])
def analyze_document():
    """
    Simulates institutional-grade extraction.
    In a production environment, this would utilize the in-memory 
    PDF stream to extract the Standardized Loan Object (SLO).
    """
    if 'file' not in request.files:
        return jsonify({"error": "No document provided"}), 400
    
    file = request.files['file']
    
    # Mock Standardized Loan Object (SLO) based on heuristic intelligence
    slo_data = {
        "metadata": {
            "normalization_version": "1.0.4",
            "timestamp": "2024-05-20T14:30:00Z",
            "confidence_score": 0.98
        },
        "instrument_intelligence": {
            "facility_type": "Term Loan B",
            "governing_law": "New York",
            "currency": "USD"
        },
        "economic_terms": {
            "margin_bps": 350,
            "floor_pct": 0.75,
            "maturity_date": "2029-12-31"
        },
        "covenants": {
            "leverage_ceiling": "4.50x",
            "interest_coverage": "2.00x",
            "status": "In-Compliance"
        }
    }
    
    return jsonify(slo_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
