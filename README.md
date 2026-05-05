# 🔐 Phishing Website Detector (Real-Time)

A machine learning-based web application that detects phishing websites using URL analysis and real-time prediction.

---

## 🚀 Features

- Real-time phishing detection (live typing)
- Machine Learning model (Random Forest)
- URL feature extraction (6 features)
- Risk scoring system (0–100)
- Trusted domain intelligence
- Domain-type awareness (.gov, .edu, .de)
- Interactive UI (Flask + HTML)

---

## 🧠 How It Works

1. User enters a URL
2. Features are extracted:
   - URL length
   - Special characters
   - IP address presence
   - Number of dots
   - HTTPS usage
   - Suspicious keywords
3. ML model predicts:
   - Phishing or Legitimate
4. Risk score is calculated
5. Trusted domains override false positives
6. Results shown in real-time

---

## 🛠 Tech Stack

- Python
- Flask
- Scikit-learn
- HTML/CSS/JavaScript

---

## 📊 Example Output

- Result: PHISHING
- Confidence: 87%
- Risk Score: 72/100
- Risk Level: HIGH ⚠️

---

## 📸 Screenshots

(Add images in screenshots folder)

---

## ⚠️ Disclaimer

This project is a prototype and demonstrates phishing detection concepts using machine learning. It is not a production-level security system.

---

## 👨‍💻 Author

Your Name
