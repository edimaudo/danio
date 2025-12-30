const zone = document.getElementById('drop-zone');
const input = document.getElementById('file-input');

zone.onclick = () => input.click();

input.onchange = async (e) => {
    const file = e.target.files[0];
    if(!file) return;

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/api/process', { method: 'POST', body: formData });
    const res = await response.json();
    
    if(res.success) {
        document.getElementById('slo-form').style.display = 'block';
        document.getElementById('f-type').value = res.data.instrument_details.type;
        document.getElementById('f-margin').value = res.data.financial_covenants.margin_bps + "%";
        document.getElementById('f-lev').value = res.data.financial_covenants.leverage_ceiling + "x";
        document.getElementById('f-law').value = res.data.instrument_details.governing_law;
        document.getElementById('raw-slo').innerText = JSON.stringify(res.data, null, 2);
    }
};
