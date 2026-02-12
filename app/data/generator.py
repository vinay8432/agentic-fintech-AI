import random
from decimal import Decimal
from typing import List, Dict


class FinancialProfileGenerator:

    @staticmethod
    def _distribute_amount(total: Decimal, count: int) -> List[Decimal]:
        if count <= 0:
            return []
        if count == 1:
            return [total]

        weights = [random.randint(1, 100) for _ in range(count)]
        total_weight = sum(weights)

        amounts = [
            (Decimal(w) / Decimal(total_weight) * total).quantize(Decimal("0.01"))
            for w in weights
        ]

        diff = total - sum(amounts)
        amounts[-1] += diff
        return amounts

    # ---------- Stable Profile ----------

    def generate_stable_profile(
        self,
        customer_id: str,
        year: int,
        monthly_avg_inflow: Decimal = Decimal("500000"),
        monthly_avg_outflow: Decimal = Decimal("400000"),
    ) -> List[Dict]:

        transactions = []

        for month in range(1, 13):

            inflow_noise = Decimal(random.randint(-5, 5)) / Decimal("100")
            inflow = (monthly_avg_inflow * (1 + inflow_noise)).quantize(Decimal("0.01"))

            credits = self._distribute_amount(inflow, random.randint(10, 20))

            for amt in credits:
                transactions.append({
                    "customer_id": customer_id,
                    "year": year,
                    "month": month,
                    "amount": amt,
                    "type": "credit"
                })

            outflow_noise = Decimal(random.randint(-2, 2)) / Decimal("100")
            outflow = (monthly_avg_outflow * (1 + outflow_noise)).quantize(Decimal("0.01"))

            debits = self._distribute_amount(outflow, random.randint(15, 25))

            for amt in debits:
                transactions.append({
                    "customer_id": customer_id,
                    "year": year,
                    "month": month,
                    "amount": amt,
                    "type": "debit"
                })

        return transactions

    # ---------- Growing Profile ----------

    def generate_growing_profile(
        self,
        customer_id: str,
        year: int,
        base_inflow: Decimal = Decimal("300000"),
        base_outflow: Decimal = Decimal("200000"),
        monthly_growth: Decimal = Decimal("0.05"),
    ) -> List[Dict]:

        transactions = []

        for month in range(1, 13):

            inflow = (base_inflow * ((1 + monthly_growth) ** (month - 1))).quantize(Decimal("0.01"))
            outflow = (base_outflow * ((1 + monthly_growth * Decimal("0.8")) ** (month - 1))).quantize(Decimal("0.01"))

            credits = self._distribute_amount(inflow, random.randint(12, 22))
            debits = self._distribute_amount(outflow, random.randint(15, 28))

            for amt in credits:
                transactions.append({
                    "customer_id": customer_id,
                    "year": year,
                    "month": month,
                    "amount": amt,
                    "type": "credit"
                })

            for amt in debits:
                transactions.append({
                    "customer_id": customer_id,
                    "year": year,
                    "month": month,
                    "amount": amt,
                    "type": "debit"
                })

        return transactions

    # ---------- Declining Profile ----------

    def generate_declining_profile(
        self,
        customer_id: str,
        year: int,
        base_inflow: Decimal = Decimal("600000"),
        base_outflow: Decimal = Decimal("500000"),
        monthly_decline: Decimal = Decimal("0.05"),
    ) -> List[Dict]:

        transactions = []

        for month in range(1, 13):

            factor = (1 - monthly_decline) ** (month - 1)

            inflow = (base_inflow * factor).quantize(Decimal("0.01"))
            outflow = (base_outflow * factor).quantize(Decimal("0.01"))

            credits = self._distribute_amount(inflow, random.randint(8, 18))
            debits = self._distribute_amount(outflow, random.randint(12, 22))

            for amt in credits:
                transactions.append({
                    "customer_id": customer_id,
                    "year": year,
                    "month": month,
                    "amount": amt,
                    "type": "credit"
                })

            for amt in debits:
                transactions.append({
                    "customer_id": customer_id,
                    "year": year,
                    "month": month,
                    "amount": amt,
                    "type": "debit"
                })

        return transactions

    # ---------- Fraud Profile ----------

    def generate_fraud_profile(
        self,
        customer_id: str,
        year: int,
        baseline_inflow: Decimal = Decimal("200000"),
        baseline_outflow: Decimal = Decimal("180000"),
    ) -> List[Dict]:

        transactions = []

        for month in range(1, 13):

            inflow = baseline_inflow
            outflow = baseline_outflow

            # occasional spike fraud
            if random.random() < 0.35:
                spike = Decimal(random.randint(3, 8))
                inflow *= spike

            credits = self._distribute_amount(inflow, random.randint(5, 15))
            debits = self._distribute_amount(outflow, random.randint(20, 40))

            # micro debit burst pattern
            if random.random() < 0.5:
                micro_total = Decimal("5000")
                micro_txns = self._distribute_amount(micro_total, 25)

                for amt in micro_txns:
                    transactions.append({
                        "customer_id": customer_id,
                        "year": year,
                        "month": month,
                        "amount": amt,
                        "type": "debit_micro"
                    })

            for amt in credits:
                transactions.append({
                    "customer_id": customer_id,
                    "year": year,
                    "month": month,
                    "amount": amt,
                    "type": "credit"
                })

            for amt in debits:
                transactions.append({
                    "customer_id": customer_id,
                    "year": year,
                    "month": month,
                    "amount": amt,
                    "type": "debit"
                })

        return transactions


# ---------- Dispatcher ----------

def generate_customer_transactions(customer_id: str, profile_type: str, year: int = 2025):

    generator = FinancialProfileGenerator()

    strategies = {
        "stable": generator.generate_stable_profile,
        "growing": generator.generate_growing_profile,
        "declining": generator.generate_declining_profile,
        "fraud": generator.generate_fraud_profile,
    }

    if profile_type not in strategies:
        raise ValueError(f"Unknown profile type: {profile_type}")

    return strategies[profile_type](customer_id, year)