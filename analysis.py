import pandas as pd


def analyze_orders(orders):
    """Calculate simple sales statistics from validated orders."""
    orders = orders.copy()

    # Convert quantity to numeric
    orders["quantity"] = pd.to_numeric(
        orders["quantity"]
    )

    # Calculate sales amount for each order
    orders["sales"] = (
        orders["quantity"]
        * orders["unit_price"]
        * (1 - orders["discount"])
    )

    total_sales = orders["sales"].sum()

    order_count = len(orders)

    average_order_value = (
        total_sales / order_count
        if order_count > 0
        else 0
    )

    sales_by_category = (
        orders
        .groupby("product_category")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "total_sales": total_sales,
        "order_count": order_count,
        "average_order_value": average_order_value,
        "sales_by_category": sales_by_category,
    }