import sys

import pandas as pd

from analysis import analyze_orders
from validate_orders import validate_orders


def main():
    """Validate the data and analyze it if validation succeeds."""

    if len(sys.argv) != 2:
        print(
            "Usage: python main.py <csv_file>"
        )
        return

    file_path = sys.argv[1]

    orders = pd.read_csv(file_path)

    # Keep quantity as text so invalid values
    # can be detected by Pandera.
    orders["quantity"] = orders["quantity"].astype("string")

    # Validate the data before analysis.
    validated_orders, errors = validate_orders(orders)

    if errors is not None:
        print("Validation failed!")
        print()
        print("The data was not analyzed because "
              "validation failed.")
        print()
        print("Validation errors:")
        print(errors.to_string(index=False))
        return

    print("Validation successful!")
    print()

    # Analyze only validated data.
    results = analyze_orders(validated_orders)

    print("Analysis results:")
    print()
    print("Total sales:",
          round(results["total_sales"], 2))

    print("Number of orders:",
          results["order_count"])

    print("Average order value:",
          round(results["average_order_value"], 2))

    print()
    print("Sales by category:")
    print(results["sales_by_category"])


if __name__ == "__main__":
    main()