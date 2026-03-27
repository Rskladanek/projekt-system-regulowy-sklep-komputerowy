from __future__ import annotations

from decimal import Decimal

from flask import session

from ..models import Product


SESSION_CART_KEY = "cart"


def get_raw_cart() -> dict[str, int]:
    return session.get(SESSION_CART_KEY, {})



def save_raw_cart(cart: dict[str, int]) -> None:
    session[SESSION_CART_KEY] = cart
    session.modified = True



def clear_cart() -> None:
    session.pop(SESSION_CART_KEY, None)
    session.modified = True



def add_product_to_cart(product_id: int, quantity: int = 1) -> None:
    cart = get_raw_cart()
    key = str(product_id)
    cart[key] = cart.get(key, 0) + max(1, quantity)
    save_raw_cart(cart)



def update_cart_quantities(form_data) -> None:
    cart = get_raw_cart()
    updated_cart: dict[str, int] = {}

    for product_id, qty in cart.items():
        field_name = f"quantity_{product_id}"
        try:
            new_qty = int(form_data.get(field_name, qty))
        except (TypeError, ValueError):
            new_qty = qty

        if new_qty > 0:
            updated_cart[str(product_id)] = new_qty

    save_raw_cart(updated_cart)



def remove_product_from_cart(product_id: int) -> None:
    cart = get_raw_cart()
    cart.pop(str(product_id), None)
    save_raw_cart(cart)



def get_cart_items() -> list[dict]:
    cart = get_raw_cart()
    if not cart:
        return []

    product_ids = [int(product_id) for product_id in cart.keys()]
    products = Product.query.filter(Product.id.in_(product_ids), Product.active.is_(True)).all()
    products_by_id = {product.id: product for product in products}

    items = []
    for product_id_str, quantity in cart.items():
        product = products_by_id.get(int(product_id_str))
        if not product:
            continue

        unit_price = Decimal(product.price)
        line_total = (unit_price * quantity).quantize(Decimal("0.01"))
        items.append(
            {
                "product": product,
                "quantity": quantity,
                "unit_price": unit_price,
                "line_total": line_total,
            }
        )

    items.sort(key=lambda item: (item["product"].category, item["product"].name))
    return items



def get_cart_subtotal() -> Decimal:
    subtotal = sum((item["line_total"] for item in get_cart_items()), start=Decimal("0.00"))
    return subtotal.quantize(Decimal("0.01"))



def get_cart_count() -> int:
    return sum(get_raw_cart().values())
