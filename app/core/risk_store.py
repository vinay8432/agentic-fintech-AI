# Load JSON once

# Convert amounts back to Decimal

# Precompute metrics

# Store eligibility signals

import json
from pathlib import Path
from decimal import Decimal

from app.analysis.financial_metrics import aggregate_by_month, compute_cashflow_growth, compute_cashflow_volatility

DATA_PATH = Path("data/generated_transactions.json")

RISK_CACHE = {}

def _convert_to_decimal(obj):
    if isinstance(obj, str) and obj.replace(".", "", 1).isdigit():
        return Decimal(obj)
    elif isinstance(obj, list):
        return [_convert_to_decimal(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: _convert_to_decimal(value) for key, value in obj.items()}
    return obj

def load_and_precompute():
    global RISK_CACHE
    if RISK_CACHE:
        return RISK_CACHE

    with open(DATA_PATH, "r") as f:
        raw_data = json.load(f)

    for customer_id, payload in raw_data.items():
        transactions = _convert_to_decimal(payload["transactions"])

        monthly = aggregate_by_month(transactions)
        growth = compute_cashflow_growth(monthly)
        volatility = compute_cashflow_volatility(monthly)

        RISK_CACHE[customer_id] = {
            "growth": growth,
            "cv": volatility["cv"],
            "stability": volatility["stability_level"],
            "fraud_flag": any(txn["type"] == "debit_micro" for txn in transactions),
            "loss_flag": sum(m["net_cashflow"] for m in monthly.values()) < 0
        }
    return RISK_CACHE


def get_customer_metrics(customer_id: str)-> dict:
    if not RISK_CACHE:
        load_and_precompute()
    return RISK_CACHE.get(customer_id)
# Load JSON once

# Convert amounts back to Decimal

# Precompute metrics

# Store eligibility signals

import json
from pathlib import Path
from decimal import Decimal

from app.analysis.financial_metrics import aggregate_by_month, compute_cashflow_growth, compute_cashflow_volatility

DATA_PATH = Path("data/generated_transactions.json")

RISK_CACHE = {}

def _convert_to_decimal(obj):
    if isinstance(obj, str) and obj.replace(".", "", 1).isdigit():
        return Decimal(obj)
    elif isinstance(obj, list):
        return [_convert_to_decimal(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: _convert_to_decimal(value) for key, value in obj.items()}
    return obj

def load_and_precompute():
    global RISK_CACHE
    if RISK_CACHE:
        return RISK_CACHE

    with open(DATA_PATH, "r") as f:
        raw_data = json.load(f)

    for customer_id, payload in raw_data.items():
        transactions = _convert_to_decimal(payload["transactions"])

        monthly = aggregate_by_month(transactions)
        growth = compute_cashflow_growth(monthly)
        volatility = compute_cashflow_volatility(monthly)

        RISK_CACHE[customer_id] = {
            "growth": growth,
            "cv": volatility["cv"],
            "stability": volatility["stability_level"],
            "fraud_flag": any(txn["type"] == "debit_micro" for txn in transactions),
            "loss_flag": sum(m["net_cashflow"] for m in monthly.values()) < 0
        }
    return RISK_CACHE


def get_customer_metrics(customer_id: str)-> dict:
    if not RISK_CACHE:
        load_and_precompute()
    return RISK_CACHE.get(customer_id)


    
