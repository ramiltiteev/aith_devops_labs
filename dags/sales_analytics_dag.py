from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import pendulum
from airflow.decorators import dag, task


def _round(value: float) -> float:
    return round(value, 2)


@dag(
    dag_id="sales_analytics_pipeline",
    description="Generates a sales report with daily and regional metrics.",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
    tags=["lab", "analytics"],
)
def sales_analytics_pipeline():
    @task
    def generate_orders() -> list[dict]:
        return [
            {"order_id": 1, "region": "North", "category": "Books", "quantity": 4, "unit_price": 12.5},
            {"order_id": 2, "region": "South", "category": "Games", "quantity": 2, "unit_price": 55.0},
            {"order_id": 3, "region": "North", "category": "Games", "quantity": 1, "unit_price": 60.0},
            {"order_id": 4, "region": "West", "category": "Books", "quantity": 8, "unit_price": 11.0},
            {"order_id": 5, "region": "East", "category": "Courses", "quantity": 3, "unit_price": 99.99},
            {"order_id": 6, "region": "South", "category": "Books", "quantity": 5, "unit_price": 13.25},
        ]

    @task
    def enrich_orders(orders: list[dict]) -> list[dict]:
        enriched_orders = []
        for order in orders:
            revenue = order["quantity"] * order["unit_price"]
            enriched_orders.append(
                {
                    **order,
                    "revenue": _round(revenue),
                }
            )
        return enriched_orders

    @task
    def calculate_daily_metrics(orders: list[dict]) -> dict:
        total_orders = len(orders)
        total_items = sum(order["quantity"] for order in orders)
        total_revenue = sum(order["revenue"] for order in orders)
        average_order_value = total_revenue / total_orders if total_orders else 0

        return {
            "total_orders": total_orders,
            "total_items": total_items,
            "total_revenue": _round(total_revenue),
            "average_order_value": _round(average_order_value),
        }

    @task
    def calculate_regional_metrics(orders: list[dict]) -> list[dict]:
        regions: dict[str, dict[str, float]] = defaultdict(lambda: {"orders": 0, "items": 0, "revenue": 0.0})

        for order in orders:
            region_stats = regions[order["region"]]
            region_stats["orders"] += 1
            region_stats["items"] += order["quantity"]
            region_stats["revenue"] += order["revenue"]

        regional_metrics = []
        for region, stats in sorted(regions.items()):
            regional_metrics.append(
                {
                    "region": region,
                    "orders": int(stats["orders"]),
                    "items": int(stats["items"]),
                    "revenue": _round(stats["revenue"]),
                }
            )

        return regional_metrics

    @task
    def save_report(daily_metrics: dict, regional_metrics: list[dict]) -> str:
        report_dir = Path("/opt/airflow/reports")
        report_dir.mkdir(parents=True, exist_ok=True)

        report = {
            "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "daily_metrics": daily_metrics,
            "regional_metrics": regional_metrics,
        }

        output_path = report_dir / "sales_report.json"
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return str(output_path)

    raw_orders = generate_orders()
    enriched_orders = enrich_orders(raw_orders)
    daily_metrics = calculate_daily_metrics(enriched_orders)
    regional_metrics = calculate_regional_metrics(enriched_orders)
    save_report(daily_metrics, regional_metrics)


sales_analytics_pipeline()
