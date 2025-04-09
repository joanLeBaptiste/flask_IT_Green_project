# models/models.py
from flask_login import UserMixin
from datetime import datetime
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), default='user')  # Par défaut, le rôle est 'user'

    def is_admin(self):
        return self.role == 'admin'

    def check_password(self, password):
        return self.password == password

class Service(db.Model):
    id_service = db.Column(db.Integer, primary_key=True)
    nom_service = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    price = db.Column(db.Float, nullable=False)
    picture_path = db.Column(db.String(255), nullable=True)
    categorie = db.Column(db.String(120), nullable=False)
    niveau = db.Column(db.String(50), nullable=True)  # ex: basique, avancé, expert

    def __repr__(self):
        return f"<Service {self.nom_service} - {self.categorie}>"

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    session_id = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('carts', lazy=True))
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade="all, delete-orphan")

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id_service'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)

    service = db.relationship('Service', backref=db.backref('cart_items', lazy=True))

