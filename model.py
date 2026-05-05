import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
data = pd.read_csv('phishing_dataset.csv')

# Feature extraction
def extract_features(url):
    features = []

    features.append(len(url))
    features.append(sum([1 for c in url if c in ['@', '?', '-', '=', '.', '_', '~', '%', '&']]))

    ip = re.findall(r'\d+\.\d+\.\d+\.\d+', url)
    features.append(1 if ip else 0)

    features.append(url.count('.'))
    features.append(1 if "https" in url else 0)

    keywords = ['login', 'secure', 'verify', 'update', 'bank', 'account']
    features.append(int(any(w in url.lower() for w in keywords)))

    return features

# Dataset conversion
X = [extract_features(url) for url in data['url']]
y = data['label']

# Train model
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))

joblib.dump(model, "phishing_model.pkl")

# ---------- SAFE TEST FUNCTION ----------
def predict_url(url):
    features = extract_features(url)

    prediction = model.predict([features])[0]
    probability = model.predict_proba([features])[0]

    confidence = max(probability) * 100

    label = "PHISHING" if prediction == 1 else "LEGITIMATE"

    # ---------------- Risk Score ----------------
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

    risk_score = max(0, min(100, int(risk_score)))

    # ---------------- Output ----------------
    print("\n==============================")
    print("URL:", url)
    print("Result:", label)
    print("Confidence:", round(confidence, 2), "%")
    print("Risk Score:", risk_score, "/100")
    print("==============================\n")

# ---------- RUN TESTS (ONLY HERE) ----------
if __name__ == "__main__":
    predict_url("http://secure-login-facebook.com")
    predict_url("https://google.com")