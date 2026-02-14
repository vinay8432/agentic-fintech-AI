from typing import Dict, List
from decimal import Decimal


def aggregate_by_month(transactions: List[Dict]) -> Dict:
    result = {}
    for txn in transactions:
        key = (txn["year"],txn["month"])
        if key not in result:
            result[key] = { "total_credit": Decimal("0"), "total_debit": Decimal("0"), "net_cashflow": Decimal("0") }
        if txn["type"] == "credit":
            result[key]["total_credit"] += txn["amount"]
        elif txn["type"] == "debit":
            result[key]["total_debit"] += txn["amount"]
        result[key]["net_cashflow"] = result[key]["total_credit"] - result[key]["total_debit"]
    return result

def compute_cashflow_growth(monthly_data: Dict) -> Decimal:
    sorted_months = sorted(monthly_data.keys())
    if len(sorted_months) < 2:
        return Decimal("0")
    
    first_month = sorted_months[0]
    last_month = sorted_months[-1]
    
    first_cashflow = monthly_data[first_month]["net_cashflow"]
    last_cashflow = monthly_data[last_month]["net_cashflow"]
    
    if first_cashflow == Decimal("0"):
        return Decimal("0")
    
    growth = (last_cashflow - first_cashflow) / abs(first_cashflow)
    return growth.quantize(Decimal("0.0001"))



def compute_cashflow_volatility(monthly_data: Dict) -> Dict:
    cashflows = [data["net_cashflow"] for data in monthly_data.values()]
    if not cashflows:
        return {"cv": Decimal("0"), "stability_level": "stable"}
    
    mean = sum(cashflows) / len(cashflows)

    if mean <= 0:
        return {"cv": Decimal("0"), "stability_level": "loss_making"}
    variance = sum((cf - mean) ** 2 for cf in cashflows) / len(cashflows)
    std_dev = variance.sqrt()
    cv = std_dev / abs(mean) if mean != Decimal("0") else Decimal("0")
    if mean < Decimal("0"):
        stability_level = "loss_making"
    elif cv <= Decimal("0.15"):
        stability_level = "stable"
    elif cv <= Decimal("0.35"):
        stability_level = "moderate"
    else:
        stability_level = "unstable"
    return {"cv": cv.quantize(Decimal("0.0001")), "stability_level": stability_level}

