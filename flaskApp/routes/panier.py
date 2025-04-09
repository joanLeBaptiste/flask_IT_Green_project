import uuid
from flask import Blueprint, session, redirect, url_for, render_template, flash
from models.db import db, Cart, CartItem, Service
from flask_login import current_user, login_required

bp = Blueprint('panier', __name__, url_prefix='/panier')


@bp.route('/add/<int:service_id>', methods=['POST'])  # anciennement product_id
def add_to_cart(service_id):
    service = Service.query.get_or_404(service_id)
    cart = get_or_create_cart()

    item = CartItem.query.filter_by(cart_id=cart.id, service_id=service.id_service).first()
    if item:
        item.quantity += 1
    else:
        item = CartItem(cart_id=cart.id, service_id=service.id_service)
        db.session.add(item)

    db.session.commit()
    flash('Service added to cart.', 'success')
    return redirect(url_for('main.index'))


@bp.route('/view')
def view_cart():
    cart = get_or_create_cart()
    return render_template('panier.html', cart=cart)


def get_or_create_cart():
    session_id = session.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id

    cart = Cart.query.filter_by(session_id=session_id).first()

    if current_user.is_authenticated:
        user_cart = Cart.query.filter_by(user_id=current_user.id).first()
        if user_cart:
            cart = user_cart
            cart.session_id = session_id
            db.session.commit()

            session_cart = Cart.query.filter_by(session_id=session_id).first()
            if session_cart and session_cart.id != cart.id:
                for item in session_cart.items:
                    existing_item = CartItem.query.filter_by(cart_id=cart.id, service_id=item.service_id).first()
                    if existing_item:
                        existing_item.quantity += item.quantity
                    else:
                        new_item = CartItem(cart_id=cart.id, service_id=item.service_id, quantity=item.quantity)
                        db.session.add(new_item)

                db.session.delete(session_cart)
                db.session.commit()
        elif cart:
            cart.user_id = current_user.id
            db.session.commit()
        else:
            cart = Cart(user_id=current_user.id, session_id=session_id)
            db.session.add(cart)
            db.session.commit()
    elif not cart:
        cart = Cart(session_id=session_id)
        db.session.add(cart)
        db.session.commit()

    session['cart_id'] = cart.id
    return cart


@bp.route('/remove/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    cart = get_or_create_cart()

    if item.cart_id == cart.id:
        db.session.delete(item)
        db.session.commit()
        flash('Service removed from cart.', 'success')
    else:
        flash('Error: Item not found in your cart.', 'danger')

    return redirect(url_for('panier.view_cart'))
