import pandas as pd

from validate_orders import validate_orders


def test_valid_orders_pass_validation():
    orders = pd.read_csv("data/valid_orders.csv")
    orders["quantity"] = orders["quantity"].astype("string")

    validated_orders, errors = validate_orders(orders)

    assert errors is None
    assert validated_orders is not None
    assert len(validated_orders) == 20


def test_invalid_orders_fail_validation():
    orders = pd.read_csv("data/invalid_orders.csv")
    orders["quantity"] = orders["quantity"].astype("string")

    validated_orders, errors = validate_orders(orders)

    assert validated_orders is None
    assert errors is not None

    invalid_columns = set(errors["column"])

    assert "order_date" in invalid_columns
    assert "customer_id" in invalid_columns
    assert "product_category" in invalid_columns
    assert "quantity" in invalid_columns
    assert "unit_price" in invalid_columns
    assert "discount" in invalid_columns
    assert "returned" in invalid_columns


def test_missing_column_fails_validation():
    orders = pd.read_csv("data/missing_column_orders.csv")
    orders["quantity"] = orders["quantity"].astype("string")

    validated_orders, errors = validate_orders(orders)

    assert validated_orders is None
    assert errors is not None

    missing_columns = set(errors["failure_case"])

    assert "discount" in missing_columns