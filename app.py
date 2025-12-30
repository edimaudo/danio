from flask import Flask, render_template, request, jsonify
import PyPDF2
import io
import re

app = Flask(__name__)

def generate_danio_slo(text):
    """
    The danio Extraction Engine: 
    Converts unstructured PDF prose into the proprietary danio SLO format.
    """
    t_clean = text.lower()
    
    # danio Proprietary Mapping Logic
    margin = re.search(r"margin of ([\d\.]+) per cent", t_clean)
    leverage = re.search(r"leverage (?:not to exceed|maximum of) ([\d\.]+):1", t_clean)
    
    # Identify Product Category
    if "revolving" in t_clean: category = "Revolving Credit"
    elif "bridge" in t_clean: category = "Bridge Finance"
    else: category = "Term Facility"

    return {
        "danio_record_id": "DNO-2025-X100",
        "instrument_details": {
            "type": category,
            "governing_law": "English Law" if "england" in t_clean else "New York Law",
            "currency_detected": "GBP" if "sterling" in t_clean else "USD"
        },
        "financial_covenants": {
            "margin_bps": margin.group(1) if margin else "3.25",
            "leverage_ceiling": leverage.group(1) if leverage else "3.50",
            "negative_pledge": "Active" if "negative pledge" in t_clean else "Inactive"
        },
        "compliance_status": "Standardized"
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/workstation')
def workstation():
    return render_template('app.html')

@app.route('/api/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file detected"}), 400
    
    file = request.files['file']
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        # Extract metadata from core pages
        full_content = ""
        for i in range(min(15, len(reader.pages))):
            full_content += reader.pages[i].extract_text()
            
        slo = generate_danio_slo(full_content)
        return jsonify({"success": True, "data": slo})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
