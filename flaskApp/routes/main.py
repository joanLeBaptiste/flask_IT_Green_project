from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.db import Service, db  # <-- remplace Product par Service
import os
from flask_login import login_required, current_user
from functools import wraps
from werkzeug.utils import secure_filename
from flask import send_from_directory

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('index.html')
@bp.route('/privacy')
def privacy():
    return render_template('privacy.html')
@bp.route('/sensibilisation')
def sensibilisation():
    return render_template('sensibilisation.html')




@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('static/uploads', filename)


@bp.route('/services')  # <-- anciennement /produit
def services():
    services = Service.query.all()
    return render_template('services.html', services=services)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/add_service', methods=['GET', 'POST'])  # <-- anciennement /add
@login_required
@admin_required
def add_service():
    if request.method == 'POST':
        nom_service = request.form['nom_service']
        description = request.form['description']
        categorie = request.form['categorie']
        price = request.form['price']
        niveau = request.form.get('niveau')

        if not nom_service or not description or not categorie or not price:
            flash('All fields except image are required.', 'error')
            return redirect(url_for('main.add_service'))

        picture_path = None
        if 'picture' in request.files:
            file = request.files['picture']
            if file.filename != '':
                filename = secure_filename(file.filename)
                picture_path = os.path.join('uploads', filename)
                file.save(os.path.join('static', picture_path))

        new_service = Service(
            nom_service=nom_service,
            description=description,
            picture_path=picture_path,
            categorie=categorie,
            niveau=niveau,
            price=float(price)
        )

        db.session.add(new_service)
        db.session.commit()

        flash('Service added successfully!', 'success')
        return redirect(url_for('main.add_service'))

    return render_template('add_service.html')
