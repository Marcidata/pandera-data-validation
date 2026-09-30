import sys

import pandas as pd


def validate_orders_manually(orders):
    """Validate order data using Pandas conditions."""

    errors = []

    required_columns = [
        "order_id",
        "order_date",
        "customer_id",
        "product_category",
        "quantity",
        "unit_price",
        "discount",
        "returned",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in orders.columns
    ]

    for column in missing_columns:
        errors.append(
            f"Missing required column: {column}"
        )

    if missing_columns:
        return errors

    invalid_dates = pd.to_datetime(
        orders["order_date"],
        errors="coerce",
    ).isna()

    if invalid_dates.any():
        errors.append(
            f"Invalid order_date values: {invalid_dates.sum()}"
        )

    missing_customer_id = orders["customer_id"].isna()

    if missing_customer_id.any():
        errors.append(
            f"Missing customer_id values: "
            f"{missing_customer_id.sum()}"
        )

    allowed_categories = [
        "Electronics",
        "Books",
        "Sports",
        "Home",
    ]

    invalid_categories = (
        ~orders["product_category"].isin(
            allowed_categories
        )
    )

    if invalid_categories.any():
        errors.append(
            f"Invalid product_category values: "
            f"{invalid_categories.sum()}"
        )

    quantity_numeric = pd.to_numeric(
        orders["quantity"],
        errors="coerce",
    )

    invalid_quantity = (
        quantity_numeric.isna()
        | quantity_numeric.le(0)
    )

    if invalid_quantity.any():
        errors.append(
            f"Invalid quantity values: "
            f"{invalid_quantity.sum()}"
        )

    invalid_unit_price = (
        orders["unit_price"].isna()
        | orders["unit_price"].le(0)
    )

    if invalid_unit_price.any():
        errors.append(
            f"Invalid unit_price values: "
            f"{invalid_unit_price.sum()}"
        )

    invalid_discount = (
        orders["discount"].isna()
        | orders["discount"].lt(0)
        | orders["discount"].gt(1)
    )

    if invalid_discount.any():
        errors.append(
            f"Invalid discount values: "
            f"{invalid_discount.sum()}"
        )

    valid_returned_values = ["true", "false"]

    returned_values = (
        orders["returned"]
        .astype("string")
        .str.lower()
    )

    invalid_returned = (
        ~returned_values.isin(valid_returned_values)
    )

    if invalid_returned.any():
        errors.append(
            f"Invalid returned values: "
            f"{invalid_returned.sum()}"
        )

    return errors


def main():
    """Read a CSV file and run manual validation."""

    if len(sys.argv) != 2:
        print(
            "Usage: python manual_validation.py <csv_file>"
        )
        return

    file_path = sys.argv[1]

    orders = pd.read_csv(file_path)

    errors = validate_orders_manually(orders)

    if errors:
        print("Manual validation failed!")
        print()
        print("File:", file_path)
        print()

        for error in errors:
            print("-", error)
    else:
        print("Manual validation successful!")
        print()
        print("File:", file_path)


if __name__ == "__main__":
    main()