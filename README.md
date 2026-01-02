# danio | Institutional Loan Standardizer

danio is a digital infrastructure solution built to address the Digital Loans. It bridges the gap between unstructured legal prose and machine-readable credit data, facilitating efficiency, transparency, and interoperability across the loan market.

The syndicated loan market is hindered by "dark data" trapped within 300-page PDF agreements. Manual data extraction is slow, prone to error, and prevents real-time portfolio analysis. danio provides an institutional-grade workstation that allows credit risk professionals and traders to extract a Standardized Loan Object (SLO) from these documents instantly. By normalizing complex covenants and business terms, danio turns a static document into a dynamic digital asset.

## Key Features

- **Automated Ingestion**: In-memory PDF stream processing ensures secure document handling. No sensitive document data is stored locally, adhering to institutional privacy standards.
- **Standardized Loan Object (SLO)**: A proprietary schema that maps varied legal phrasing—such as "Margin," "Spread," or "Applicable Rate"—to a unified digital format.
- **Dual-View Workstation**: A professional interface featuring a Structured Form View for human verification alongside a Raw JSON Output for direct system interoperability.
- **Instrument Intelligence**: Heuristic logic designed to differentiate between Revolving Credit Facilities (RCF), Term Loans, and Bridge Loans, adjusting extraction priorities accordingly.

## Implementation
- **Backend**: Flask (Python) with PyPDF2 for secure, in-memory document "shredding."
- **Frontend**: Native JavaScript and CSS Grid, ensuring a lightweight, secure, and responsive institutional experience.

## Project Structure
```
danio/
├── app.py              
├── requirements.txt    
├── README.md           
├── static/
│   ├── style.css       
│   └── script.js       
└── templates/
    ├── index.html      
    └── app.html       
```

## Installation and Deployment
### Environmental Setup
```
pip install -r requirements.txt
```
### Application Launch
```
python app.py
```


