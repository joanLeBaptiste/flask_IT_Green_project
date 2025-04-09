from flask import Blueprint, request, jsonify, session
from flask_login import current_user
from openai import OpenAI
from core.config import Config

bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

client = OpenAI(api_key=Config.OPENAI_API_KEY)

# Message de rôle : envoyé une seule fois au début de la conversation
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Tu es un assistant spécialisé dans l'écologie numérique et la consommation énergétique de l'intelligence artificielle. "
        "Ta mission est d'aider les utilisateurs à comprendre l'impact environnemental de l'IA, à optimiser leur consommation, "
        "et à adopter une stratégie IA plus responsable et éthique. Sois clair, synthétique, professionnel, et orienté solution."
    )
}


@bp.route('/', methods=['POST'])
def chatbot():
    user_message = request.json.get('message')
    sender_id = str(current_user.id) if current_user.is_authenticated else "guest"
    print(f"Sender: {sender_id} | Message: {user_message}")

    # Initialise le contexte dans la session si ce n’est pas déjà fait
    if 'chat_history' not in session:
        session['chat_history'] = [SYSTEM_PROMPT]

    # Ajoute le message utilisateur dans le contexte
    session['chat_history'].append({
        "role": "user",
        "content": user_message
    })

    try:
        # Envoie tout l'historique à l'API OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=session['chat_history']
        )

        # Récupère la réponse du bot
        bot_reply = response.choices[0].message.content

        # Ajoute la réponse du bot à l’historique
        session['chat_history'].append({
            "role": "assistant",
            "content": bot_reply
        })

        # Flask sauvegarde la session automatiquement si elle est modifiée
        return jsonify({"response": bot_reply})

    except Exception as e:
        print(f"Erreur OpenAI: {e}")
        return jsonify({"error": "Erreur de communication avec le chatbot."}), 500


@bp.route('/session')
def session_data():
    return jsonify(session.get('chat_history', []))


@bp.route('/reset', methods=['POST'])
def reset_chat():
    session.pop("chat_history", None)
    return jsonify({"status": "reset"})