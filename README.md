# AI-Prescription-Checker
The AI Prescription Checker is a Flask-based intelligent healthcare assistant that uses Google Gemini AI to analyze medical prescriptions and reports. It extracts structured medical information and helps users better understand their medication details in a simple and clear format.
# 🧠 AI Prescription Checker – Gemini Powered Medical Analyzer

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black.svg)
![Gemini AI](https://img.shields.io/badge/Google-Gemini%20AI-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📌 Overview

The **AI Prescription Checker** is a Flask-based intelligent medical assistant that uses **Google Gemini AI** to analyze prescriptions and medical reports.

It extracts structured medical information and helps users understand their medication in a simple, clear, and safe way.

> ⚠️ This project is for **educational and research purposes only** and is not a substitute for professional medical advice.

---

## 🚀 Features

- 📄 Upload prescription or medical report images
- 💊 Extracts:
  - Medicine names
  - Dosage information
  - Frequency & timing
- ⚠️ Basic drug interaction checker
- 🧠 AI-powered medical text understanding (Gemini AI)
- 🔁 Retry system for API failures (503 / quota issues)
- 🛡️ Smart fallback handling for stability
- 📊 Converts unstructured text into structured JSON output

---

## ⚙️ How It Works

1. User uploads a prescription image or report  
2. File is temporarily stored on server  
3. Google Gemini AI analyzes the content  
4. AI extracts medical information in structured format  
5. System checks for possible drug interactions  
6. Results are displayed in a clean UI  

---

## 🛠️ Tech Stack

- Python 🐍  
- Flask 🌐  
- Google Gemini API 🤖  
- JSON Processing 📊  
- HTML/CSS (Frontend) 🎨  

---

## 📂 Project Structure
ai-prescription-checker/
│
├── app.py
├── templates/
│ └── index.html
└── README.md
