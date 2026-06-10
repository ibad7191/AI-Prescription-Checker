from flask import Flask, render_template, request, jsonify
from google import genai
import os, json, random

app = Flask(__name__)

# 🔹 Gemini API Key

client = genai.Client(api_key="PUT_YOUR_API_KEY_HERE")


# -------------------------------
# 1️⃣ Extract text from image (Prescription Reader)
# -------------------------------
def extract_text_gemini(image_path):
    try:
        file = client.files.upload(file=image_path)
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[file, "Extract medicine names, doses, and frequency in JSON format."]
        )
        if response and hasattr(response, "text") and response.text.strip():
            return response.text.strip()
        else:
            return ""
    except Exception as e:
        print("❌ Gemini error:", e)
        return ""


# -------------------------------
# 2️⃣ Convert Gemini output to JSON
# -------------------------------
def parse_prescription_text(raw_text):
    try:
        return json.loads(raw_text)
    except Exception:
        try:
            resp = client.models.generate_content(
                model="gemini-2.5-flash-exp",
                contents=f"Fix this malformed JSON: {raw_text}"
            )
            return json.loads(resp.text)
        except Exception:
            return [{"name": "Unknown", "dose": "", "frequency": ""}]


# -------------------------------
# 3️⃣ Medicine Interaction Checker
# -------------------------------
def check_interactions(med_list):
    dangerous_pairs = [
        ("aspirin", "ibuprofen"),
        ("paracetamol", "ibuprofen"),
        ("amoxicillin", "metronidazole")
    ]

    meds_lower = [m.get("name", "").lower() for m in med_list if isinstance(m, dict)]
    results = []

    for a in meds_lower:
        for b in meds_lower:
            if a and b and a != b and ((a, b) in dangerous_pairs or (b, a) in dangerous_pairs):
                results.append(f"⚠️ {a.title()} and {b.title()} should not be taken together!")

    if not results:
        results.append("✅ No major interactions found.")

    timing_tips = [
        "Take after meal with a glass of water.",
        "Avoid on empty stomach.",
        "Keep 4-hour gap between painkillers.",
        "Avoid dairy with antibiotics."
    ]

    return {"interactions": results, "tip": random.choice(timing_tips)}


# -------------------------------
# 4️⃣ Chatbot for Patients
# -------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please type something to ask."})

    try:
        prompt = f"""
        You are a helpful medical assistant. The patient said: "{user_message}".
        Reply in simple, clear language (health advice only, no prescriptions).
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash-exp",
            contents=prompt
        )
        reply = response.text.strip() if hasattr(response, "text") else "Sorry, I couldn't understand that."
        return jsonify({"response": reply})
    except Exception as e:
        print("Chat error:", e)
        return jsonify({"response": "⚠️ Gemini service is currently unavailable. Try again later."})


# -------------------------------
# 5️⃣ Home & Analyze Routes
# -------------------------------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", meds=None)


@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("prescription")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    save_path = file.filename
    file.save(save_path)

    raw_text = extract_text_gemini(save_path)
    if not raw_text.strip():
        return render_template(
            "index.html",
            raw_text="⚠️ Gemini API temporary unavailable or returned empty response.",
            meds=[],
            results={"interactions": [], "tip": ""},
            image_path=save_path
        )

    meds = parse_prescription_text(raw_text)
    results = check_interactions(meds)

    return render_template(
        "index.html",
        raw_text=raw_text,
        meds=meds,
        results=results,
        image_path=save_path
    )


# -------------------------------
# 6️⃣ Run App
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)




