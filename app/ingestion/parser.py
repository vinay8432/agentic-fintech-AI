import re
from typing import List, Dict
from datetime import datetime
from decimal import Decimal


class BankStatementParser:

    DATE_PATTERN = r"\d{2}-\d{2}-\d{4}"
    CREDIT_KEYWORDS = ["credit", "cr", "in"]
    DEBIT_KEYWORDS = ["debit", "dr", "wdl", "out"]

    def __init__(self, customer_id: str):
        self.customer_id = customer_id

    def _normalize_txn_type(self, raw_type: str) -> str:
        token = raw_type.lower().split()
        for key in token:
            if key in self.CREDIT_KEYWORDS:
                return "credit"
            elif key in self.DEBIT_KEYWORDS:
                return "debit"
        raise ValueError(f"Unknown transaction type: {raw_type}")

    def _parse_amount(self, amt: str) -> Decimal:
        cleaned = amt.replace(",", "").strip()
        return Decimal(cleaned)

    def _format_date(self, date_str: str) -> str:
        return datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")

    def parse_text(self, raw_text: str) -> List[Dict]:
        
        transactions = []
        lines = raw_text.split("\n")

        txn_pattern = re.compile(
            rf"({self.DATE_PATTERN})\s+(.+?)\s+(-?[\d,]+(?:\.\d+)?)\s+(.+)"
        )

        for line in lines:
            try:
                line = line.strip()

                match = txn_pattern.match(line)
                if not match:
                    continue

                date_raw, txn_type_raw, amount_raw, description_raw = match.groups()

                transaction = {
                    "customer_id": self.customer_id,
                    "date": self._format_date(date_raw),
                    "transaction_type": self._normalize_txn_type(txn_type_raw),
                    "amount": self._parse_amount(amount_raw),
                    "description": description_raw.strip(),
                }

                transactions.append(transaction)
            except Exception as e:
                print(f"Error parsing line: '{line}' - {e}")
                continue

        return transactions
    