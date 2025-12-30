const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');

dropZone.onclick = () => fileInput.click();

fileInput.onchange = (e) => handleUpload(e.target.files[0]);

async function handleUpload(file) {
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/api/ingest', { method: 'POST', body: formData });
    const result = await response.json();
    
    if(result.success) {
        document.getElementById('form-view').style.display = 'block';
        document.getElementById('f-type').value = result.data.product_type;
        document.getElementById('f-margin').value = result.data.margin;
        document.getElementById('f-lev').value = result.data.leverage_cap;
        document.getElementById('f-law').value = result.data.jurisdiction;
        document.getElementById('json-preview').innerText = JSON.stringify(result.data, null, 2);
    }
}
