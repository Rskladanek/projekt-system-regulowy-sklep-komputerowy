from .base import Facts, RuleResult


class RuleEngine:
    def __init__(self, rules: list):
        self.rules = sorted(rules, key=lambda rule: rule.priority, reverse=True)

    def run(self, facts: Facts) -> RuleResult:
        result = RuleResult(subtotal=facts.subtotal)

        for rule in self.rules:
            rule.evaluate(facts, result)

        result.resolve_conflicts()
        return result
