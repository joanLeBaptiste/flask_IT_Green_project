from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.db import db, User

bp = Blueprint('account', __name__, url_prefix='/account')


@bp.route('/', methods=['GET', 'POST'])
@login_required  # ✅ protège l'accès à la route
def account():
    user = current_user  # ✅ récupère l'utilisateur connecté

    if request.method == 'POST':
        new_username = request.form.get('username')

        if new_username and new_username != user.username:
            user.username = new_username
            db.session.commit()
            flash('Username updated successfully.', 'success')
        else:
            flash('No changes were made.', 'info')

    return render_template('account.html', user=user)
