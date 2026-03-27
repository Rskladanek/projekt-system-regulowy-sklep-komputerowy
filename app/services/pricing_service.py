from __future__ import annotations

from .. import db
from ..models import Cart, CartItem, PromotionResult, RuleLog
from ..rules.base import Facts
from ..rules.engine import RuleEngine
from ..rules.promotions import build_rules
from .cart_service import get_cart_items



def analyze_current_cart(save_to_history: bool = True):
    items = get_cart_items()
    facts = Facts(items)
    engine = RuleEngine(build_rules())
    result = engine.run(facts)

    saved_cart = None
    if save_to_history and items:
        saved_cart = save_analysis(facts, result)

    return items, facts, result, saved_cart



def save_analysis(facts: Facts, result) -> Cart:
    cart = Cart(
        total_before=facts.subtotal,
        total_after=result.total_after,
        shipping_cost=result.shipping_cost,
        total_discount=result.total_discount,
    )
    db.session.add(cart)
    db.session.flush()

    for item in facts.items:
        db.session.add(
            CartItem(
                cart_id=cart.id,
                product_id=item["product"].id,
                quantity=item["quantity"],
                unit_price=item["unit_price"],
            )
        )

    for promo in result.applied_promotions:
        db.session.add(
            PromotionResult(
                cart_id=cart.id,
                rule_code=promo["rule_code"],
                rule_name=promo["rule_name"],
                discount_value=promo["discount_value"],
                description=promo["description"],
            )
        )

    for log in result.logs:
        db.session.add(
            RuleLog(
                cart_id=cart.id,
                rule_code=log.rule_code,
                matched=log.matched,
                note=log.note,
            )
        )

    for note in result.conflict_notes:
        db.session.add(
            RuleLog(
                cart_id=cart.id,
                rule_code="R6",
                matched=True,
                note=note,
            )
        )

    db.session.commit()
    return cart
