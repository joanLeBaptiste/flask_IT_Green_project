# app.py
from flask import Flask, request, jsonify, session
from flask_login import LoginManager, current_user
from models import db
from models.db import User
from core.config import Config
import requests


from routes.account import bp as account_bp
from routes.auth import bp as auth_bp
from routes.main import bp as main_bp
from routes.panier import bp as panier_bp
from routes.chatbot import bp as chatbot_bp

from routes.analyse import bp as analyse_bp



print(f"📁 SQLITE PATH: {Config.SQLALCHEMY_DATABASE_URI}")
# Créer et configurer l'application Flask
app = Flask(__name__)
app.config.from_object(Config)

# Initialiser SQLAlchemy avec l'application
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Définir la clé API OpenAI #### ajout

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(account_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(panier_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(analyse_bp)


def create_db():
    """Créer la base de données et les tables si elles n'existent pas déjà"""
    with app.app_context():
        db.create_all()

@app.route("/session_data")
def session_data():
    return str(session)


if __name__ == '__main__':
    create_db()  # Créer la base de données avant de lancer l'app si elle existe pas
    app.run(debug=True)

#