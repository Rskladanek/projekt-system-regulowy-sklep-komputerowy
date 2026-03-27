from decimal import Decimal

from .base import Facts, Rule, RuleResult


ACCESSORY_CATEGORIES = ["klawiatura", "mysz"]


def has_computer_and_monitor(facts: Facts, result: RuleResult) -> bool:
    return facts.has_categories("komputer", "monitor")


def apply_bundle_discount(facts: Facts, result: RuleResult) -> None:
    result.add_percent_discount(
        code="R1",
        name="Zestaw komputer + monitor",
        percent=5,
        base_amount=facts.subtotal,
        priority=90,
        exclusive_group="bundle_discounts",
        description="Rabat 5% za zakup co najmniej jednego komputera i jednego monitora.",
    )


def has_computer_keyboard_mouse(facts: Facts, result: RuleResult) -> bool:
    return facts.has_categories("komputer", "klawiatura", "mysz")


def apply_accessory_bundle_discount(facts: Facts, result: RuleResult) -> None:
    accessories_total = facts.subtotal_for_categories(ACCESSORY_CATEGORIES)
    result.add_percent_discount(
        code="R2",
        name="Pakiet komputer + klawiatura + mysz",
        percent=7,
        base_amount=accessories_total,
        priority=95,
        exclusive_group="bundle_discounts",
        description="Rabat 7% na akcesoria przy zakupie komputera, klawiatury i myszy.",
    )


def has_three_same_monitors(facts: Facts, result: RuleResult) -> bool:
    return len(facts.same_monitor_lines_with_min_quantity(3)) > 0


def apply_monitor_bulk_discount(facts: Facts, result: RuleResult) -> None:
    eligible_total = sum(
        (item["line_total"] for item in facts.same_monitor_lines_with_min_quantity(3)),
        start=Decimal("0.00"),
    )
    result.add_percent_discount(
        code="R3",
        name="Promocja ilościowa na monitory",
        percent=10,
        base_amount=eligible_total,
        priority=85,
        description="Rabat 10% na monitor kupowany w liczbie co najmniej 3 sztuk tego samego modelu.",
    )


def exceeds_value_threshold(facts: Facts, result: RuleResult) -> bool:
    return facts.subtotal > Decimal("8000.00")


def apply_value_threshold_discount(facts: Facts, result: RuleResult) -> None:
    result.add_percent_discount(
        code="R4",
        name="Próg wartości koszyka",
        percent=3,
        base_amount=facts.subtotal,
        priority=70,
        description="Dodatkowy rabat 3% po przekroczeniu wartości koszyka 8000 zł.",
    )


def has_two_printers(facts: Facts, result: RuleResult) -> bool:
    return facts.count_by_category("drukarka") >= 2


def apply_free_shipping(facts: Facts, result: RuleResult) -> None:
    result.shipping_cost = Decimal("0.00")



def build_rules() -> list[Rule]:
    return [
        Rule(
            code="R2",
            name="Pakiet komputer + klawiatura + mysz",
            priority=95,
            condition=has_computer_keyboard_mouse,
            action=apply_accessory_bundle_discount,
            success_note="Koszyk zawiera komputer, klawiaturę i mysz. Dodano 7% rabatu na akcesoria.",
            failure_note="Brakuje pełnego zestawu komputer + klawiatura + mysz.",
        ),
        Rule(
            code="R1",
            name="Zestaw komputer + monitor",
            priority=90,
            condition=has_computer_and_monitor,
            action=apply_bundle_discount,
            success_note="Koszyk zawiera komputer i monitor. Dodano 5% rabatu zestawowego.",
            failure_note="Brakuje zestawu komputer + monitor.",
        ),
        Rule(
            code="R3",
            name="Promocja ilościowa na monitory",
            priority=85,
            condition=has_three_same_monitors,
            action=apply_monitor_bulk_discount,
            success_note="W koszyku są co najmniej 3 sztuki tego samego monitora. Dodano 10% rabatu na te monitory.",
            failure_note="Brak co najmniej 3 sztuk tego samego monitora.",
        ),
        Rule(
            code="R4",
            name="Próg wartości koszyka",
            priority=70,
            condition=exceeds_value_threshold,
            action=apply_value_threshold_discount,
            success_note="Wartość koszyka przekracza 8000 zł. Dodano dodatkowe 3% rabatu.",
            failure_note="Wartość koszyka nie przekracza 8000 zł.",
        ),
        Rule(
            code="R5",
            name="Darmowa dostawa dla drukarek",
            priority=60,
            condition=has_two_printers,
            action=apply_free_shipping,
            success_note="Kupiono co najmniej 2 drukarki. Dostawa została ustawiona na 0 zł.",
            failure_note="Nie spełniono warunku darmowej dostawy dla drukarek.",
        ),
    ]
