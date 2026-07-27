# FinanceHub

FinanceHub is a Flask-based personal finance web app for tracking income, expenses, and financial summaries. It includes user authentication, a transaction dashboard, export options, and finance calculators.

## Features
- User registration and login
- Add, edit, and delete transactions
- Dashboard with balance, income, expense, and charts
- CSV and PDF export
- GST, EMI, SIP, and profit-loss calculators
- Dark/light theme toggle

## Tech Stack
- Python 3
- Flask
- SQLite
- HTML, CSS, JavaScript
- ReportLab for PDF generation

## Installation
1. Open the project folder.
2. Create and activate a virtual environment:
   - Windows PowerShell:
     - `py -m venv venv`
     - `./venv/Scripts/Activate.ps1`
3. Install dependencies:
   - `pip install -r requirements.txt`

## Run the App
From the project root, run:
- `python app.py`

Then open:
- `http://127.0.0.1:5000/`

## Notes
- The app uses a local SQLite database file named `finance.db`.
- New users can register from the Register page and then log in.
- If you want to reset the database, delete `finance.db` and restart the app.
