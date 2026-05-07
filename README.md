# CreditGuard — Credit Card Default Prediction App

## Project Structure
```
credit_card_app/
├── app.py                  ← Flask backend (main file)
├── requirements.txt        ← Python dependencies
├── users.json              ← Auto-created on first registration
├── best_rf_model.pkl       ← Your trained model (place here)
└── templates/
    ├── login.html          ← Page 1: Login / Register
    ├── index.html          ← Page 2: Prediction Input Form
    └── result.html         ← Page 3: Dashboard / Results
```

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Place your trained model in the same folder
cp path/to/best_rf_model.pkl .

# 3. Run the app
python app.py
```

Then open: http://127.0.0.1:5000

## Features

- **Login / Register** — User accounts saved in `users.json`
- **Session-based auth** — Every route requires login; logout clears session
- **Prediction Form** — 14 input fields organised into 3 sections:
  - Account Info (LIMIT_BAL, AGE)
  - Monthly Bill Statements (BILL_AMT1–6)
  - Monthly Payment History (PAY_AMT1–6)
- **Dashboard** — Animated probability bar, bill vs payment chart, input summary table
- **Demo mode** — If `best_rf_model.pkl` is missing, random predictions are used (for UI testing)

## Model Input Order (14 features)
LIMIT_BAL, AGE, BILL_AMT1, BILL_AMT2, BILL_AMT3, BILL_AMT4, BILL_AMT5, BILL_AMT6,
PAY_AMT1, PAY_AMT2, PAY_AMT3, PAY_AMT4, PAY_AMT5, PAY_AMT6
