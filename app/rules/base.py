from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Callable


TWOPLACES = Decimal("0.01")


def to_decimal(value) -> Decimal:
    if isinstance(value, Decimal):
        return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)
    return Decimal(str(value)).quantize(TWOPLACES, rounding=ROUND_HALF_UP)


@dataclass
class RuleLogEntry:
    rule_code: str
    matched: bool
    note: str


class Facts:
    def __init__(self, items: list[dict]):
        self.items = items

    @property
    def subtotal(self) -> Decimal:
        return sum((item["line_total"] for item in self.items), start=Decimal("0.00")).quantize(TWOPLACES)

    def count_by_category(self, category: str) -> int:
        return sum(item["quantity"] for item in self.items if item["product"].category == category)

    def has_categories(self, *categories: str) -> bool:
        return all(self.count_by_category(category) >= 1 for category in categories)

    def subtotal_for_category(self, category: str) -> Decimal:
        total = sum(
            (item["line_total"] for item in self.items if item["product"].category == category),
            start=Decimal("0.00"),
        )
        return total.quantize(TWOPLACES)

    def subtotal_for_categories(self, categories: list[str]) -> Decimal:
        total = sum((self.subtotal_for_category(category) for category in categories), start=Decimal("0.00"))
        return total.quantize(TWOPLACES)

    def product_quantity(self, product_id: int) -> int:
        for item in self.items:
            if item["product"].id == product_id:
                return item["quantity"]
        return 0

    def same_monitor_lines_with_min_quantity(self, min_quantity: int) -> list[dict]:
        return [
            item
            for item in self.items
            if item["product"].category == "monitor" and item["quantity"] >= min_quantity
        ]


class RuleResult:
    def __init__(self, subtotal: Decimal, default_shipping_cost: Decimal = Decimal("25.00")):
        self.subtotal = to_decimal(subtotal)
        self.default_shipping_cost = to_decimal(default_shipping_cost)
        self.shipping_cost = self.default_shipping_cost
        self.applied_promotions: list[dict] = []
        self.logs: list[RuleLogEntry] = []
        self.conflict_notes: list[str] = []

    def add_log(self, rule_code: str, matched: bool, note: str) -> None:
        self.logs.append(RuleLogEntry(rule_code=rule_code, matched=matched, note=note))

    def add_discount(
        self,
        *,
        code: str,
        name: str,
        description: str,
        amount: Decimal,
        priority: int,
        exclusive_group: str | None = None,
    ) -> None:
        amount = to_decimal(amount)
        if amount <= 0:
            return
        self.applied_promotions.append(
            {
                "rule_code": code,
                "rule_name": name,
                "description": description,
                "discount_value": amount,
                "priority": priority,
                "exclusive_group": exclusive_group,
            }
        )

    def add_percent_discount(
        self,
        *,
        code: str,
        name: str,
        description: str,
        percent: Decimal | int | float,
        base_amount: Decimal,
        priority: int,
        exclusive_group: str | None = None,
    ) -> None:
        base_amount = to_decimal(base_amount)
        percent = Decimal(str(percent))
        amount = (base_amount * percent / Decimal("100")).quantize(TWOPLACES, rounding=ROUND_HALF_UP)
        self.add_discount(
            code=code,
            name=name,
            description=description,
            amount=amount,
            priority=priority,
            exclusive_group=exclusive_group,
        )

    def set_free_shipping(self, *, code: str, note: str) -> None:
        self.shipping_cost = Decimal("0.00")
        self.add_log(code, True, note)

    def resolve_conflicts(self) -> None:
        grouped: dict[str, list[dict]] = defaultdict(list)
        remaining: list[dict] = []

        for promo in self.applied_promotions:
            if promo["exclusive_group"]:
                grouped[promo["exclusive_group"]].append(promo)
            else:
                remaining.append(promo)

        for group_name, promos in grouped.items():
            promos_sorted = sorted(
                promos,
                key=lambda promo: (promo["discount_value"], promo["priority"]),
                reverse=True,
            )
            winner = promos_sorted[0]
            remaining.append(winner)

            if len(promos_sorted) > 1:
                losers = promos_sorted[1:]
                removed_codes = ", ".join(promo["rule_code"] for promo in losers)
                self.conflict_notes.append(
                    f"R6: konflikt w grupie '{group_name}'. Zostawiono {winner['rule_code']} ({winner['rule_name']}), odrzucono {removed_codes}."
                )

        self.applied_promotions = sorted(remaining, key=lambda promo: promo["priority"], reverse=True)

    @property
    def total_discount(self) -> Decimal:
        total = sum((promo["discount_value"] for promo in self.applied_promotions), start=Decimal("0.00"))
        return total.quantize(TWOPLACES)

    @property
    def total_after(self) -> Decimal:
        total = self.subtotal - self.total_discount + self.shipping_cost
        if total < 0:
            total = Decimal("0.00")
        return total.quantize(TWOPLACES)


class Rule:
    def __init__(
        self,
        code: str,
        name: str,
        priority: int,
        condition: Callable[[Facts, RuleResult], bool],
        action: Callable[[Facts, RuleResult], None],
        success_note: str,
        failure_note: str,
    ):
        self.code = code
        self.name = name
        self.priority = priority
        self.condition = condition
        self.action = action
        self.success_note = success_note
        self.failure_note = failure_note

    def evaluate(self, facts: Facts, result: RuleResult) -> bool:
        if self.condition(facts, result):
            self.action(facts, result)
            result.add_log(self.code, True, self.success_note)
            return True

        result.add_log(self.code, False, self.failure_note)
        return False
