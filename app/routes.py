from collections import defaultdict

from flask import Blueprint, flash, redirect, render_template, request, url_for

from .models import Cart, Product
from .services.cart_service import (
    add_product_to_cart,
    clear_cart,
    get_cart_count,
    get_cart_items,
    get_cart_subtotal,
    remove_product_from_cart,
    update_cart_quantities,
)
from .services.pricing_service import analyze_current_cart


main_bp = Blueprint("main", __name__)


@main_bp.app_context_processor
def inject_cart_summary():
    return {"cart_count": get_cart_count()}


@main_bp.route("/")
def index():
    return redirect(url_for("main.products"))


@main_bp.route("/products")
def products():
    products = Product.query.filter_by(active=True).order_by(Product.category, Product.name).all()
    grouped_products = defaultdict(list)
    for product in products:
        grouped_products[product.category].append(product)

    return render_template("products.html", grouped_products=dict(grouped_products))


@main_bp.post("/cart/add/<int:product_id>")
def add_to_cart(product_id: int):
    product = Product.query.get_or_404(product_id)
    quantity = request.form.get("quantity", 1, type=int) or 1
    add_product_to_cart(product.id, quantity)
    flash(f"Dodano do koszyka: {product.name}", "success")
    return redirect(url_for("main.products"))


@main_bp.route("/cart")
def cart():
    items = get_cart_items()
    subtotal = get_cart_subtotal()
    return render_template("cart.html", items=items, subtotal=subtotal)


@main_bp.post("/cart/update")
def update_cart():
    update_cart_quantities(request.form)
    flash("Koszyk został zaktualizowany.", "success")
    return redirect(url_for("main.cart"))


@main_bp.post("/cart/remove/<int:product_id>")
def remove_from_cart(product_id: int):
    remove_product_from_cart(product_id)
    flash("Produkt został usunięty z koszyka.", "info")
    return redirect(url_for("main.cart"))


@main_bp.post("/cart/clear")
def clear_current_cart():
    clear_cart()
    flash("Koszyk został wyczyszczony.", "info")
    return redirect(url_for("main.cart"))


@main_bp.post("/cart/analyze")
def analyze_cart():
    items, facts, result, saved_cart = analyze_current_cart(save_to_history=True)

    if not items:
        flash("Koszyk jest pusty. Dodaj produkty przed analizą promocji.", "warning")
        return redirect(url_for("main.cart"))

    clear_cart()
    flash("Analiza promocji została wykonana.", "success")
    return redirect(url_for("main.summary", cart_id=saved_cart.id))


@main_bp.route("/summary/<int:cart_id>")
def summary(cart_id: int):
    cart = Cart.query.get_or_404(cart_id)
    logs = sorted(cart.rule_logs, key=lambda log: (log.rule_code, not log.matched))
    return render_template("summary.html", cart=cart, logs=logs)
