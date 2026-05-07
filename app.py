from flask import Flask, request, render_template, jsonify, session, redirect, url_for
import numpy as np
import pickle
import json
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = "credit_card_secret_key_2024"

# ─── Simple file-based user store ───────────────────────────────────────────
USERS_FILE = "credit_card_app/users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# ─── Load model ─────────────────────────────────────────────────────────────
try:
    model = pickle.load(open("credit_card_app/best_rf_model.pkl", "rb"))
except FileNotFoundError:
    model = None  # Allow UI to run without model for demo

# ─── Auth decorator ──────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

# ─── Routes ──────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("predict_page"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        action   = data.get("action")
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        users = load_users()

        if action == "login":
            if username in users and users[username]["password"] == password:
                session["username"] = username
                session["email"]    = users[username].get("email", "")
                return jsonify({"success": True})
            return jsonify({"success": False, "message": "Invalid credentials"})

        elif action == "register":
            email = data.get("email", "").strip()
            if username in users:
                return jsonify({"success": False, "message": "Username already exists"})
            if not username or not password:
                return jsonify({"success": False, "message": "Username and password required"})
            users[username] = {"password": password, "email": email}
            save_users(users)
            session["username"] = username
            session["email"]    = email
            return jsonify({"success": True})

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/predict-page")
@login_required
def predict_page():
    return render_template("index.html", username=session.get("username"))

@app.route("/predict", methods=["POST"])
@login_required
def predict():
    try:
        features = [
            float(request.form["LIMIT_BAL"]),
            float(request.form["AGE"]),
            float(request.form["PAY_0"]),
            float(request.form["PAY_1"]),
            float(request.form["PAY_2"]),
            float(request.form["PAY_3"]),
            float(request.form["PAY_4"]),
            float(request.form["PAY_5"]),
            float(request.form["BILL_AMT1"]),
            float(request.form["BILL_AMT2"]),
            float(request.form["BILL_AMT3"]),
            float(request.form["BILL_AMT4"]),
            float(request.form["BILL_AMT5"]),
            float(request.form["BILL_AMT6"]),
            float(request.form["PAY_AMT1"]),
            float(request.form["PAY_AMT2"]),
            float(request.form["PAY_AMT3"]),
            float(request.form["PAY_AMT4"]),
            float(request.form["PAY_AMT5"]),
            float(request.form["PAY_AMT6"]),
        ]

        final_features = np.array([features])

        if model is None:
            # Demo mode — random result
            import random
            prediction = random.randint(0, 1)
            prob = round(random.uniform(0.1, 0.95), 4)
        else:
            prediction = int(model.predict(final_features)[0])
            prob = float(model.predict_proba(final_features)[0][1])

        # Store in session for dashboard
        session["last_prediction"] = prediction
        session["last_prob"]       = prob
        session["last_inputs"]     = {k: request.form[k] for k in request.form}

        return jsonify({"prediction": prediction, "prob": prob})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/dashboard")
@login_required
def dashboard():
    prediction = session.get("last_prediction", None)
    prob       = session.get("last_prob", None)
    inputs     = session.get("last_inputs", {})
    return render_template(
        "result.html",
        username=session.get("username"),
        prediction=prediction,
        prob=prob,
        inputs=inputs,
    )

if __name__ == "__main__":
    app.run(debug=True)
