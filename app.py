from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import os
import json
import re

import firebase_admin
from firebase_admin import credentials, firestore

import google.generativeai as genai


# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)
CORS(app)


# ==========================================
# GEMINI AI CONFIGURATION
# ==========================================

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        print("Gemini API configured successfully.")
    except Exception as error:
        print("Gemini configuration error:", error)
else:
    print("WARNING: GEMINI_API_KEY not found.")


# ==========================================
# FIREBASE CONNECTION
# ==========================================

db = None

try:

    # Render Environment Variable
    firebase_credentials = os.environ.get("FIREBASE_CREDENTIALS")

    if firebase_credentials:

        firebase_config = json.loads(firebase_credentials)

        cred = credentials.Certificate(firebase_config)

        firebase_admin.initialize_app(cred)

        db = firestore.client()

        print("Firebase connected successfully.")

    # Local computer
    elif os.path.exists("database.json"):

        cred = credentials.Certificate("database.json")

        firebase_admin.initialize_app(cred)

        db = firestore.client()

        print("Firebase connected using database.json.")

    else:

        print("Firebase credentials not found.")
        print("Running without Firebase.")

except Exception as error:

    print("Firebase connection error:", error)

    db = None


# ==========================================
# LANGUAGE DETECTION
# ==========================================

def detect_language(message):

    # Tamil Unicode
    tamil_pattern = re.compile(r'[\u0B80-\u0BFF]')

    if tamil_pattern.search(message):
        return "tamil"


    # Tanglish words
    tanglish_words = [

        "ena",
        "enna",
        "sollu",
        "sollunga",
        "kudu",
        "kudunga",
        "venum",
        "epdi",
        "eppadi",
        "pathi",
        "theriyuma",
        "iruku",
        "irukku",
        "illa",
        "pannu",
        "pannunga",
        "padikanum",
        "padikka",
        "padipu",
        "oda",
        "ku",
        "la",
        "ah",
        "thaan",
        "thana",
        "enaku",
        "ungaluku",
        "kekura",
        "kekuren",
        "sollu",
        "exam",
        "question",
        "answer",
        "history",
        "math",
        "gk"
    ]

    message_lower = message.lower()

    words = message_lower.split()

    for word in tanglish_words:

        if word in words:
            return "tanglish"

    return "english"


# ==========================================
# GEMINI ANSWER FUNCTION
# ==========================================

def get_answer(message, language):

    if not GEMINI_API_KEY:

        return (
            "Gemini API key is not configured. "
            "Please add GEMINI_API_KEY in Render Environment Variables."
        )


    # ======================================
    # LANGUAGE INSTRUCTION
    # ======================================

    if language == "tamil":

        language_instruction = """
Answer completely in Tamil script.
Use simple Tamil that a TNPSC student can easily understand.
Avoid unnecessary English words.
"""

    elif language == "tanglish":

        language_instruction = """
Answer completely in Tanglish.
Use Tamil words written using English letters.
Do NOT use Tamil Unicode script.
Keep the explanation simple and natural.
"""

    else:

        language_instruction = """
Answer completely in English.
Use simple English suitable for a TNPSC student.
"""


    # ======================================
    # TNPSC SYSTEM PROMPT
    # ======================================

    prompt = f"""
You are TNPSC Study AI, an educational assistant
designed specifically for TNPSC examination preparation.

The student can ask questions about:

- TNPSC
- Group 1
- Group 2
- Group 2A
- Group 4
- History
- Indian History
- Tamil Nadu History
- Indian Polity
- Indian Constitution
- Geography
- Economics
- General Science
- General Knowledge
- Current Affairs
- Aptitude
- Mathematics
- Tamil
- English
- Government schemes
- Important personalities
- Important dates
- Previous year style questions
- Practice questions

{language_instruction}

IMPORTANT RULES:

1. Answer the student's actual question directly.
2. Do not give a generic response.
3. Explain concepts in a student-friendly way.
4. For factual questions, give the correct answer first.
5. For aptitude or mathematics questions, show the calculation step by step.
6. If the student asks for a practice question, give one TNPSC-level question and answer.
7. If the student asks for multiple questions, provide multiple questions.
8. If appropriate, use headings and bullet points.
9. Keep answers reasonably concise unless the student asks for a detailed answer.
10. Do not say that you are unable to answer just because the question is not one of a fixed list.
11. If the question is related to TNPSC preparation, answer it as a TNPSC study assistant.
12. If the student asks in Tanglish, respond in Tanglish.
13. If the student asks in Tamil script, respond in Tamil script.
14. If the student asks in English, respond in English.

Student question:

{message}
"""


    try:

        # Gemini Flash model
        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        response = model.generate_content(prompt)

        if response and response.text:

            return response.text.strip()

        return "Sorry, I could not generate an answer. Please try again."

    except Exception as error:

        print("Gemini Error:", error)

        return (
            "Sorry, Gemini AI response failed. "
            "Please check the Gemini API key and try again."
        )


# ==========================================
# CHAT API
# ==========================================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "reply": "Invalid request."
            })


        message = data.get(
            "message",
            ""
        ).strip()


        selected_language = data.get(
            "language",
            "auto"
        )


        # ==================================
        # EMPTY MESSAGE
        # ==================================

        if not message:

            return jsonify({
                "success": False,
                "reply": "Please enter a question."
            })


        # ==================================
        # LANGUAGE
        # ==================================

        if selected_language == "auto":

            language = detect_language(message)

        else:

            language = selected_language


        # ==================================
        # GEMINI ANSWER
        # ==================================

        answer = get_answer(
            message,
            language
        )


        # ==================================
        # SAVE TO FIREBASE
        # ==================================

        if db is not None:

            try:

                db.collection(
                    "chat_history"
                ).add({

                    "question": message,

                    "answer": answer,

                    "language": language

                })

                print("Chat saved to Firebase.")

            except Exception as firebase_error:

                print(
                    "Firebase save error:",
                    firebase_error
                )


        # ==================================
        # SEND RESPONSE
        # ==================================

        return jsonify({

            "success": True,

            "language": language,

            "reply": answer

        })


    except Exception as error:

        print(
            "Chat API Error:",
            error
        )

        return jsonify({

            "success": False,

            "reply": "Something went wrong. Please try again."

        })


# ==========================================
# HOME ROUTE
# ==========================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health")
def health():

    return jsonify({

        "status": "ok",

        "firebase": db is not None,

        "gemini": GEMINI_API_KEY is not None

    })


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(

        host="0.0.0.0",

        port=port,

        debug=False

    )