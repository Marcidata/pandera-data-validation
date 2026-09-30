import sys

import pandas as pd
import pandera.pandas as pa
from pandera.errors import SchemaErrors


def create_orders_schema():
    """Create the Pandera schema for order data."""

    return pa.DataFrameSchema(
        {
            "order_id": pa.Column(
                str
            ),

            "order_date": pa.Column(
                str,
                checks=pa.Check(
                    lambda s: pd.to_datetime(
                        s,
                        errors="coerce"
                    ).notna()
                ),
            ),

            "customer_id": pa.Column(
                str,
                nullable=False,
            ),

            "product_category": pa.Column(
                str,
                checks=pa.Check.isin(
                    [
                        "Electronics",
                        "Books",
                        "Sports",
                        "Home",
                    ]
                ),
            ),

            "quantity": pa.Column(
                str,
                checks=[
                    pa.Check(
                        lambda s: pd.to_numeric(
                            s,
                            errors="coerce"
                        ).notna()
                    ),
                    pa.Check(
                        lambda s: pd.to_numeric(
                            s,
                            errors="coerce"
                        ).fillna(0).gt(0)
                    ),
                ],
            ),

            "unit_price": pa.Column(
                float,
                checks=pa.Check.gt(0),
            ),

            "discount": pa.Column(
                float,
                nullable=False,
                checks=pa.Check.between(0, 1),
            ),

            "returned": pa.Column(
                bool
            ),
        }
    )


def validate_orders(orders):
    """Validate an orders DataFrame with Pandera."""

    schema = create_orders_schema()

    try:
        validated_orders = schema.validate(
            orders,
            lazy=True
        )

        return validated_orders, None

    except SchemaErrors as error:
        return None, error.failure_cases


def main():
    """Read a CSV file and run validation."""

    if len(sys.argv) != 2:
        print(
            "Usage: python validate_orders.py "
            "<csv_file>"
        )
        return

    file_path = sys.argv[1]

    orders = pd.read_csv(file_path)

    orders["quantity"] = orders["quantity"].astype("string")

    validated_orders, errors = validate_orders(orders)

    if errors is None:
        print("Validation successful!")
        print()
        print("File:", file_path)
        print("Number of valid orders:", len(validated_orders))
        print()
        print("First 5 rows:")
        print(validated_orders.head())

    else:
        print("Validation failed!")
        print()
        print("File:", file_path)
        print()
        print("Validation errors:")
        print(errors.to_string(index=False))


if __name__ == "__main__":
    main()