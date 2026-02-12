import json
import random
from decimal import Decimal
from pathlib import Path

try:
    from app.data.generator import FinancialProfileGenerator, generate_customer_transactions
except ImportError:
    from ..data.generator import FinancialProfileGenerator, generate_customer_transactions



OUTPUT_PATH = Path("data/generated_transactions.json")


def decimal_to_string(obj):
    """
    Recursively convert Decimal values to strings
    so JSON can serialize safely.
    """
    if isinstance(obj, Decimal):
        return str(obj)
    elif isinstance(obj, list):
        return [decimal_to_string(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: decimal_to_string(value) for key, value in obj.items()}
    return obj


def generate_dataset(num_customers: int = 20, year: int = 2025):

    profiles = ["stable", "growing", "declining", "fraud"]

    dataset = {}
    print("Starting dataset generation...")
    for i in range(1, num_customers + 1):
        customer_id = f"cust_{i:03d}"
        profile = random.choice(profiles)

        transactions = generate_customer_transactions(
            customer_id=customer_id,
            profile_type=profile,
            year=year
        )
        print(f"Generated {len(transactions)} transactions for {customer_id} with profile {profile}")
        dataset[customer_id] = {
            "profile": profile,
            "transactions": transactions
        }

    # Convert Decimal to string before saving
    dataset_serializable = decimal_to_string(dataset)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(dataset_serializable, f, indent=2)

    print(f"Dataset generated at: {OUTPUT_PATH}")


if __name__ == "__main__":
    print("Generating synthetic dataset of bank transactions...")
    generate_dataset()