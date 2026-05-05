from flask import Flask, request, render_template, jsonify
import joblib
import re
from urllib.parse import urlparse

app = Flask(__name__)

# Load trained model
model = joblib.load("phishing_model.pkl")

# ---------------- Feature Extraction ----------------
def extract_features(url):
    features = []

    # 1. URL length
    features.append(len(url))

    # 2. Special characters
    features.append(sum([c in ['@', '?', '-', '=', '.', '_', '~', '%', '&'] for c in url]))

    # 3. IP address presence
    ip = re.findall(r'\d+\.\d+\.\d+\.\d+', url)
    features.append(1 if ip else 0)

    # 4. Dot count
    features.append(url.count('.'))

    # 5. HTTPS check
    features.append(1 if "https" in url else 0)

    # 6. Suspicious keywords
    keywords = ['login', 'secure', 'verify', 'update', 'bank', 'account']
    features.append(int(any(word in url.lower() for word in keywords)))

    return features

# ---------------- Home Page ----------------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# ---------------- Prediction API ----------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"})

    features = extract_features(url)

    prediction = model.predict([features])[0]
    probability = model.predict_proba([features])[0]

    confidence = round(max(probability) * 100, 2)

    # ---------------- Risk Scoring ----------------
    risk_score = 0

    if prediction == 1:
        risk_score += confidence * 0.6
    else:
        risk_score += (100 - confidence) * 0.2

    if "http://" in url:
        risk_score += 15

    if "login" in url.lower():
        risk_score += 10

    if url.count('.') > 3:
        risk_score += 10

    if any(char.isdigit() for char in url):
        risk_score += 5

    risk_score = int(max(0, min(100, risk_score)))

    # ---------------- Consistency Fix ----------------
    if prediction == 1 and risk_score < 60:
        risk_score = 65  # phishing should be high risk

    if prediction == 0 and risk_score > 60:
        risk_score = 40  # legit should stay low risk

    # ---------------- Trusted Domains ----------------
    trusted_domains = [
        "google.com",
        "youtube.com",
        "github.com",
        "wikipedia.org",
        "amazon.in",
        "microsoft.com",
        "apple.com",
        "linkedin.com",
        "epicgames.com",
        "daad.de"
    ]

    domain = urlparse(url).netloc.lower()

    # Trusted override
    if any(trusted in domain for trusted in trusted_domains):
        result = "LEGITIMATE"
        risk_score = int(risk_score * 0.3)
    else:
        result = "PHISHING" if prediction == 1 else "LEGITIMATE"

    # ---------------- Domain Type Intelligence ----------------
    if domain.endswith(".gov") or domain.endswith(".edu") or domain.endswith(".de"):
        risk_score = int(risk_score * 0.5)

    return jsonify({
        "result": result,
        "confidence": confidence,
        "risk": risk_score
    })

# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run(debug=True)