from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore


# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)

# Allow frontend to connect with backend
CORS(app)


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

    # Local computer: database.json
    elif os.path.exists("database.json"):
        cred = credentials.Certificate("database.json")

        firebase_admin.initialize_app(cred)

        db = firestore.client()

        print("Firebase connected using database.json.")

    else:
        print("Firebase credentials not found. Running without Firebase.")

except Exception as error:
    print("Firebase connection error:", error)
    db = None


# ==========================================
# LANGUAGE DETECTION
# ==========================================

def detect_language(message):

    # Tamil Unicode characters
    tamil_pattern = re.compile(r'[\u0B80-\u0BFF]')

    if tamil_pattern.search(message):
        return "tamil"

    # Common Tanglish words
    tanglish_words = [
        "ena",
        "enna",
        "sollu",
        "kudu",
        "venum",
        "epdi",
        "eppadi",
        "pathi",
        "theriyuma",
        "iruku",
        "irukku",
        "illa",
        "pannu",
        "padikanum",
        "padikka",
        "oda",
        "ku",
        "la",
        "ah",
        "thaan",
        "thana",
        "enaku",
        "ungaluku",
        "kekura",
        "kekuren"
    ]

    message_lower = message.lower()

    for word in tanglish_words:

        if word in message_lower.split():
            return "tanglish"

    # Default
    return "english"


# ==========================================
# TNPSC QUESTION ANSWERS
# ==========================================

def get_answer(message, language):

    message_lower = message.lower()


    # ======================================
    # CAPITAL OF INDIA
    # ======================================

    if (
        "capital of india" in message_lower
        or "india capital" in message_lower
        or "இந்தியாவின் தலைநகரம்" in message
    ):

        if language == "tamil":

            return "இந்தியாவின் தலைநகரம் புதுடெல்லி."

        elif language == "tanglish":

            return "India oda capital New Delhi."

        else:

            return "The capital of India is New Delhi."


    # ======================================
    # ARTICLE 21
    # ======================================

    if "article 21" in message_lower:

        if language == "tamil":

            return (
                "இந்திய அரசியலமைப்பின் Article 21 "
                "வாழ்வதற்கும் தனிப்பட்ட சுதந்திரத்திற்கும் "
                "உரிமை வழங்குகிறது."
            )

        elif language == "tanglish":

            return (
                "Article 21 na Right to Life and Personal Liberty. "
                "Simple ah sonna, ovvoru person kum life and "
                "personal freedom oda right iruku."
            )

        else:

            return (
                "Article 21 of the Indian Constitution guarantees "
                "the Right to Life and Personal Liberty."
            )


    # ======================================
    # TNPSC GROUP 4
    # ======================================

    if "group 4" in message_lower:

        if language == "tamil":

            return (
                "TNPSC Group 4 தேர்வுக்கு தமிழ், பொது அறிவு, "
                "அரசியலமைப்பு, வரலாறு, புவியியல் மற்றும் "
                "அடிப்படை கணிதம் போன்ற பாடங்களை படிக்க வேண்டும்."
            )

        elif language == "tanglish":

            return (
                "TNPSC Group 4 prepare panna Tamil, General Knowledge, "
                "History, Geography, Polity and Aptitude topics "
                "padikanum. Namma practice questions um pannalam!"
            )

        else:

            return (
                "For TNPSC Group 4 preparation, you should study "
                "Tamil, General Knowledge, History, Geography, "
                "Polity and Aptitude."
            )


    # ======================================
    # INDIAN CONSTITUTION
    # ======================================

    if (
        "constitution" in message_lower
        or "அரசியலமைப்பு" in message
        or "constitution pathi" in message_lower
    ):

        if language == "tamil":

            return (
                "இந்திய அரசியலமைப்பு இந்தியாவின் அடிப்படை சட்டமாகும். "
                "இது குடிமக்களின் உரிமைகள் மற்றும் அரசாங்கத்தின் "
                "அமைப்பை விளக்குகிறது."
            )

        elif language == "tanglish":

            return (
                "Indian Constitution na India oda basic law. "
                "Ithu citizens oda rights, duties matrum government "
                "epdi work pannanum nu explain pannuthu."
            )

        else:

            return (
                "The Indian Constitution is the supreme law of India. "
                "It explains the structure of government and the "
                "rights and duties of citizens."
            )


    # ======================================
    # TAMIL NADU HISTORY
    # ======================================

    if (
        "tamil nadu history" in message_lower
        or "தமிழ்நாடு வரலாறு" in message
        or "history pathi" in message_lower
    ):

        if language == "tamil":

            return (
                "தமிழ்நாட்டின் வரலாறு சேர, சோழ மற்றும் பாண்டிய "
                "அரசர்களுடன் தொடர்புடையது. குறிப்பாக சோழர்கள் "
                "சிறந்த நிர்வாகம் மற்றும் கோவில் கட்டிடக்கலைக்கு "
                "புகழ்பெற்றவர்கள்."
            )

        elif language == "tanglish":

            return (
                "Tamil Nadu history la Chera, Chola and Pandya "
                "kingdoms romba important. Chola kings avanga "
                "administration and temple architecture ku famous."
            )

        else:

            return (
                "Tamil Nadu has a rich history associated with the "
                "Chera, Chola and Pandya kingdoms. The Cholas are "
                "especially known for administration and temple "
                "architecture."
            )


    # ======================================
    # APTITUDE QUESTION
    # ======================================

    if (
        "aptitude" in message_lower
        or "math question" in message_lower
        or "கணிதம்" in message
    ):

        if language == "tamil":

            return (
                "பயிற்சி கேள்வி:\n\n"
                "ஒரு எண்ணின் 25% = 50 என்றால், அந்த எண் என்ன?\n\n"
                "பதில்: 200.\n\n"
                "விளக்கம்: 50 × 100 / 25 = 200."
            )

        elif language == "tanglish":

            return (
                "Practice Question 👇\n\n"
                "Oru number oda 25% = 50 na, "
                "antha number enna?\n\n"
                "Answer: 200.\n\n"
                "Explanation: 50 × 100 / 25 = 200."
            )

        else:

            return (
                "Practice Question 👇\n\n"
                "If 25% of a number is 50, what is the number?\n\n"
                "Answer: 200.\n\n"
                "Explanation: 50 × 100 / 25 = 200."
            )


    # ======================================
    # GENERAL KNOWLEDGE
    # ======================================

    if (
        "general knowledge" in message_lower
        or "gk" in message_lower
        or "பொது அறிவு" in message
    ):

        if language == "tamil":

            return (
                "பொது அறிவு பயிற்சி கேள்வி:\n\n"
                "இந்தியாவின் தேசிய விலங்கு எது?\n\n"
                "பதில்: புலி."
            )

        elif language == "tanglish":

            return (
                "GK Practice Question 👇\n\n"
                "India oda National Animal enna?\n\n"
                "Answer: Puli (Tiger)."
            )

        else:

            return (
                "GK Practice Question 👇\n\n"
                "What is the national animal of India?\n\n"
                "Answer: Tiger."
            )


    # ======================================
    # DEFAULT RESPONSE
    # ======================================

    if language == "tamil":

        return (
            "உங்கள் கேள்வியை புரிந்துகொண்டேன். "
            "TNPSC தொடர்பான கேள்விகளை கேட்கலாம். "
            "வரலாறு, அரசியலமைப்பு, புவியியல், "
            "பொது அறிவு மற்றும் கணிதம் போன்றவற்றில் "
            "நான் உதவ முடியும்."
        )

    elif language == "tanglish":

        return (
            "Ungaloda question purinjuthu 👍🏻 "
            "TNPSC related questions kekalam. "
            "History, Polity, Geography, GK and Aptitude "
            "topics la naan help panren!"
        )

    else:

        return (
            "I understand your question. You can ask me "
            "TNPSC-related questions about History, Polity, "
            "Geography, General Knowledge and Aptitude."
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

        message = data.get("message", "").strip()

        selected_language = data.get(
            "language",
            "auto"
        )


        # ==================================
        # EMPTY MESSAGE CHECK
        # ==================================

        if not message:

            return jsonify({
                "success": False,
                "reply": "Please enter a question."
            })


        # ==================================
        # LANGUAGE DETECTION
        # ==================================

        if selected_language == "auto":

            language = detect_language(message)

        else:

            language = selected_language


        # ==================================
        # GET ANSWER
        # ==================================

        answer = get_answer(
            message,
            language
        )


        # ==================================
        # SAVE CHAT TO FIREBASE
        # ==================================

        if db is not None:

            try:

                db.collection("chat_history").add({

                    "question": message,

                    "answer": answer,

                    "language": language

                })

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

        print("Error:", error)

        return jsonify({

            "success": False,

            "reply": "Something went wrong. Please try again."

        })


# ==========================================
# HOME ROUTE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health")
def health():

    return jsonify({

        "status": "ok",

        "firebase": db is not None

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