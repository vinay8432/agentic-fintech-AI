# app/config/policy_config.py

from decimal import Decimal

POLICY_CONFIG = {
    "loan_rules": [
        {
            "max_amount": Decimal("500000"),   # up to 5L
            "max_cv": Decimal("0.35"),
            "require_positive_growth": True
        },
        {
            "max_amount": Decimal("2000000"),  # up to 20L
            "max_cv": Decimal("0.25"),
            "require_positive_growth": True
        }
    ]
}