from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_user, current_user, logout_user
from models.db import db, User, Cart, CartItem
from routes.panier import get_or_create_cart
import uuid

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)

            # Générer un nouveau session_id
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id

            # 🔄 Récupérer ou fusionner le panier utilisateur/session
            get_or_create_cart()  # ✅ AJOUT ACTIF

            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))

        flash('Invalid username or password', 'danger')

    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vérifie si le nom d'utilisateur est déjà pris
        if User.query.filter_by(username=username).first():
            flash('Ce nom d’utilisateur est déjà utilisé. Choisissez-en un autre.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        get_or_create_cart()

        flash('Inscription réussie ! Vous êtes maintenant connecté.', 'success')
        return redirect(url_for('main.index'))

    return render_template('register.html')

@bp.route('/logout')
def logout():
    # Nettoyage de session
    session.pop('session_id', None)
    session.pop('cart_id', None)

    logout_user()

    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))
