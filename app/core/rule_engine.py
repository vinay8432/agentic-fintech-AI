# app/core/rule_engine.py

from decimal import Decimal
from app.config.policy_config import POLICY_CONFIG

def evaluate_loan_eligibility(metrics: dict, loan_amount: Decimal) -> dict:
    """
    Deterministically evaluates eligibility.
    """

    cv = metrics["cv"]
    growth = metrics["growth"]
    fraud_flag = metrics["fraud_flag"]
    loss_flag = metrics["loss_flag"]

    # Select rule based on loan amount
    applicable_rule = None
    for rule in POLICY_CONFIG["loan_rules"]:
        if loan_amount <= rule["max_amount"]:
            applicable_rule = rule
            break

    if applicable_rule is None:
        return {
            "eligible": False,
            "reason_code": "LOAN_AMOUNT_EXCEEDS_POLICY_LIMIT"
        }

    # Deterministic checks
    if loss_flag:
        return {"eligible": False, "reason_code": "LOSS_MAKING"}

    if fraud_flag:
        return {"eligible": False, "reason_code": "FRAUD_PATTERN_DETECTED"}

    if applicable_rule["require_positive_growth"] and growth <= Decimal("0"):
        return {"eligible": False, "reason_code": "NEGATIVE_GROWTH"}

    if cv > applicable_rule["max_cv"]:
        return {
            "eligible": False,
            "reason_code": "VOLATILITY_THRESHOLD_EXCEEDED"
        }

    return {"eligible": True, "reason_code": "ELIGIBLE"}