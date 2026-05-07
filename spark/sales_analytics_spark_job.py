from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a sales analytics report with PySpark.")
    parser.add_argument(
        "--output",
        default="/opt/airflow/reports/sales_report.json",
        help="Path to the JSON report file.",
    )
    return parser.parse_args()


def build_orders() -> list[dict]:
    return [
        {"order_id": 1, "region": "North", "category": "Books", "quantity": 4, "unit_price": 12.5},
        {"order_id": 2, "region": "South", "category": "Games", "quantity": 2, "unit_price": 55.0},
        {"order_id": 3, "region": "North", "category": "Games", "quantity": 1, "unit_price": 60.0},
        {"order_id": 4, "region": "West", "category": "Books", "quantity": 8, "unit_price": 11.0},
        {"order_id": 5, "region": "East", "category": "Courses", "quantity": 3, "unit_price": 99.99},
        {"order_id": 6, "region": "South", "category": "Books", "quantity": 5, "unit_price": 13.25},
    ]


def build_report(spark: SparkSession) -> dict:
    orders_df = spark.createDataFrame(build_orders()).withColumn(
        "revenue",
        F.round(F.col("quantity") * F.col("unit_price"), 2),
    )

    daily_metrics_row = (
        orders_df.agg(
            F.count("order_id").alias("total_orders"),
            F.sum("quantity").alias("total_items"),
            F.round(F.sum("revenue"), 2).alias("total_revenue"),
            F.round(F.avg("revenue"), 2).alias("average_order_value"),
        )
        .first()
    )

    regional_metrics_rows = (
        orders_df.groupBy("region")
        .agg(
            F.count("order_id").alias("orders"),
            F.sum("quantity").alias("items"),
            F.round(F.sum("revenue"), 2).alias("revenue"),
        )
        .orderBy("region")
        .collect()
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "daily_metrics": {
            "total_orders": int(daily_metrics_row["total_orders"]),
            "total_items": int(daily_metrics_row["total_items"]),
            "total_revenue": float(daily_metrics_row["total_revenue"]),
            "average_order_value": float(daily_metrics_row["average_order_value"]),
        },
        "regional_metrics": [
            {
                "region": row["region"],
                "orders": int(row["orders"]),
                "items": int(row["items"]),
                "revenue": float(row["revenue"]),
            }
            for row in regional_metrics_rows
        ],
    }


def save_report(report: dict, output_path: str) -> None:
    target_path = Path(output_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(json.dumps(report, indent=2), encoding="utf-8")


def main() -> None:
    args = parse_args()
    spark = SparkSession.builder.appName("SalesAnalyticsSparkJob").getOrCreate()

    try:
        report = build_report(spark)
        save_report(report, args.output)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
