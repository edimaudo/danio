document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const ingestionStage = document.getElementById('ingestion-stage');
    const workstationView = document.getElementById('workstation-view');
    const progressBar = document.getElementById('upload-progress');

    // SLO Output Fields
    const fields = {
        class: document.getElementById('f-class'),
        law: document.getElementById('f-law'),
        margin: document.getElementById('f-margin'),
        ccy: document.getElementById('f-ccy'),
        maturity: document.getElementById('f-maturity'),
        covenant: document.getElementById('f-covenant'),
        json: document.getElementById('json-output')
    };

    dropZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });

    async function handleFileUpload(file) {
        // Show progress UI
        progressBar.style.display = 'block';
        dropZone.style.opacity = '0.5';
        dropZone.style.pointerEvents = 'none';

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Normalization failed');

            const slo = await response.json();
            
            // Populate Structured View
            fields.class.value = slo.instrument_intelligence.facility_type;
            fields.law.value = slo.instrument_intelligence.governing_law;
            fields.margin.value = slo.economic_terms.margin_bps;
            fields.ccy.value = slo.instrument_intelligence.currency;
            fields.maturity.value = slo.economic_terms.maturity_date;
            fields.covenant.value = slo.covenants.leverage_ceiling;

            // Populate Raw JSON
            fields.json.textContent = JSON.stringify(slo, null, 4);

            // Transition UI
            ingestionStage.style.display = 'none';
            workstationView.style.display = 'block';

        } catch (error) {
            console.error(error);
            alert("Error: Institutional extraction failed. Please ensure the PDF is not encrypted.");
            location.reload();
        }
    }

    // Drag and Drop support
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--danio-indigo)';
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.style.borderColor = 'var(--danio-border)';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (file && file.type === 'application/pdf') {
            handleFileUpload(file);
        }
    });
});
