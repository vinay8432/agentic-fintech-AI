from decimal import Decimal
from app.core.risk_store import get_customer_metrics
from app.core.rule_engine import evaluate_loan_eligibility


def get_customer_loan_eligibility(customer_id: str, loan_amount: float) -> dict:
    """
    Business-level tool exposed to LLM.
    Fetches metrics, applies rule engine, and returns JSON-safe result.
    """

    # 1️⃣ Fetch precomputed metrics
    metrics = get_customer_metrics(customer_id)

    if not metrics:
        return {
            "eligible": False,
            "reason_code": "CUSTOMER_NOT_FOUND"
        }

    # 2️⃣ Convert loan amount to Decimal (for deterministic rule logic)
    loan_amount_decimal = Decimal(str(loan_amount))

    # 3️⃣ Evaluate eligibility via rule engine
    decision = evaluate_loan_eligibility(metrics, loan_amount_decimal)

    # 4️⃣ Convert any Decimal values to float for JSON compatibility
    json_safe_result = {}

    for key, value in decision.items():
        if isinstance(value, Decimal):
            json_safe_result[key] = float(value)
        else:
            json_safe_result[key] = value

    return json_safe_result

from decimal import Decimal
from app.core.risk_store import get_customer_metrics
from app.core.rule_engine import evaluate_loan_eligibility


def get_customer_loan_eligibility(customer_id: str, loan_amount: float) -> dict:
    """
    Business-level tool exposed to LLM.
    Fetches metrics, applies rule engine, and returns JSON-safe result.
    """

    # 1️⃣ Fetch precomputed metrics
    metrics = get_customer_metrics(customer_id)

    if not metrics:
        return {
            "eligible": False,
            "reason_code": "CUSTOMER_NOT_FOUND"
        }

    # 2️⃣ Convert loan amount to Decimal (for deterministic rule logic)
    loan_amount_decimal = Decimal(str(loan_amount))

    # 3️⃣ Evaluate eligibility via rule engine
    decision = evaluate_loan_eligibility(metrics, loan_amount_decimal)

    # 4️⃣ Convert any Decimal values to float for JSON compatibility
    json_safe_result = {}

    for key, value in decision.items():
        if isinstance(value, Decimal):
            json_safe_result[key] = float(value)
        else:
            json_safe_result[key] = value

    return json_safe_result
