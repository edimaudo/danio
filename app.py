from flask import Flask, render_template, request, jsonify
import PyPDF2
import io
import re

app = Flask(__name__)

def extract_slo_logic(text):
    """
    Standardization Engine: Maps varied legal prose to a 
    Standardized Loan Object (SLO).
    """
    text_clean = text.lower()
    
    # 1. Product Type Identification
    if "revolving" in text_clean: p_type = "Revolving Credit Facility (RCF)"
    elif "bridge" in text_clean: p_type = "Bridge Loan"
    else: p_type = "Term Loan (Facility A/B)"

    # 2. Key Term Extraction (Heuristic Anchors)
    margin = re.search(r"margin of ([\d\.]+) per cent", text_clean)
    leverage = re.search(r"leverage (?:not to exceed|maximum of) ([\d\.]+):1", text_clean)
    
    return {
        "product_type": p_type,
        "jurisdiction": "English Law (LMA)" if "england" in text_clean else "NY Law (LSTA)",
        "margin": margin.group(1) + "%" if margin else "3.25% (Standard)",
        "leverage_cap": leverage.group(1) + "x" if leverage else "3.50x (Default)",
        "status": "Digitized"
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/app')
def workstation():
    return render_template('app.html')

@app.route('/api/ingest', methods=['POST'])
def ingest():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file"}), 400
    
    file = request.files['file']
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = ""
        # Extract first 15 pages for metadata efficiency
        for i in range(min(15, len(reader.pages))):
            text += reader.pages[i].extract_text()
            
        data = extract_slo_logic(text)
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
