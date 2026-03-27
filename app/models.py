from datetime import datetime
from decimal import Decimal

from . import db


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Product {self.name}>"


class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    total_before = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    total_after = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    shipping_cost = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    total_discount = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal("0.00"))

    items = db.relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
    promotion_results = db.relationship(
        "PromotionResult", back_populates="cart", cascade="all, delete-orphan"
    )
    rule_logs = db.relationship("RuleLog", back_populates="cart", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Cart {self.id}>"


class CartItem(db.Model):
    __tablename__ = "cart_item"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

    cart = db.relationship("Cart", back_populates="items")
    product = db.relationship("Product")

    def __repr__(self) -> str:
        return f"<CartItem cart={self.cart_id} product={self.product_id} qty={self.quantity}>"


class PromotionResult(db.Model):
    __tablename__ = "promotion_result"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
    rule_code = db.Column(db.String(20), nullable=False)
    rule_name = db.Column(db.String(120), nullable=False)
    discount_value = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    description = db.Column(db.Text, nullable=False)

    cart = db.relationship("Cart", back_populates="promotion_results")

    def __repr__(self) -> str:
        return f"<PromotionResult {self.rule_code}>"


class RuleLog(db.Model):
    __tablename__ = "rule_log"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
    rule_code = db.Column(db.String(20), nullable=False)
    matched = db.Column(db.Boolean, nullable=False, default=False)
    note = db.Column(db.Text, nullable=False)

    cart = db.relationship("Cart", back_populates="rule_logs")

    def __repr__(self) -> str:
        return f"<RuleLog {self.rule_code} matched={self.matched}>"
