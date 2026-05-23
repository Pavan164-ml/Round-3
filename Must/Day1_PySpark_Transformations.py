"""
DAY 1 — PYSPARK TRANSFORMATIONS PRACTICE
Interview: 26 May 2026 | Data Engineering + AI

Run with: spark-submit Day1_PySpark_Transformations.py
Or in Databricks notebook / PySpark shell.
"""

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType
from pyspark.sql.functions import (
    col, sum, avg, count, when, lit, udf, explode, split,
    row_number, rank, dense_rank, lag, lead, desc, asc,
    pandas_udf, PandasUDFType, broadcast, coalesce, isnan, isnull
)
from pyspark.sql.window import Window

# =============================================================================
# SETUP SPARK SESSION
# =============================================================================
spark = SparkSession.builder \
    .appName("Interview_Practice_Day1") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print("=" * 70)
print("PYSPARK INTERVIEW PRACTICE — DAY 1")
print("=" * 70)

# =============================================================================
# PROBLEM 1: Core Transformations (filter, select, withColumn, groupBy)
# =============================================================================

# Create sample data
data = [
    (1, "Alice", "Electronics", 250.00, "2026-01-15"),
    (2, "Bob", "Books", 120.00, "2026-01-16"),
    (3, "Alice", "Electronics", 480.00, "2026-02-10"),
    (4, "Charlie", "Food", 75.00, "2026-02-15"),
    (5, "Bob", "Electronics", 200.00, "2026-03-01"),
    (6, "Alice", "Books", 90.00, "2026-03-15"),
    (7, "Charlie", "Electronics", 320.00, "2026-03-20"),
    (8, "Diana", "Food", 150.00, "2026-04-01"),
    (9, "Bob", "Electronics", 310.00, "2026-04-10"),
    (10, "Alice", "Electronics", 600.00, "2026-04-15"),
]

schema = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("customer_name", StringType(), True),
    StructField("category", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("order_date", StringType(), True),
])

df = spark.createDataFrame(data, schema)
df.show(5, truncate=False)

# Filter — orders above 200
print("High value orders (>200):")
df.filter(col("amount") > 200).show()

# Select + withColumn — add year column
print("With year column:")
df.withColumn("year", split(col("order_date"), "-")[0]).show()

# groupBy + agg — total spend per customer
print("Total spend per customer:")
df.groupBy("customer_name").agg(
    sum("amount").alias("total_spent"),
    count("order_id").alias("order_count"),
    avg("amount").alias("avg_order_value")
).orderBy(desc("total_spent")).show()

# =============================================================================
# PROBLEM 2: Window Functions in PySpark
# =============================================================================

# Latest order per customer (ROW_NUMBER)
window_spec = Window.partitionBy("customer_name").orderBy(desc("order_date"))

df_with_rn = df.withColumn("rn", row_number().over(window_spec))
print("Latest order per customer:")
df_with_rn.filter(col("rn") == 1).select(
    "order_id", "customer_name", "category", "amount", "order_date"
).show()

# Running total per customer (Window spec with unbounded preceding)
running_window = Window.partitionBy("customer_name").orderBy("order_date") \
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)

print("Running total per customer:")
df.withColumn("running_total", sum("amount").over(running_window)) \
    .orderBy("customer_name", "order_date").show()

# LAG — previous order amount
lag_window = Window.partitionBy("customer_name").orderBy("order_date")

print("Previous order amount (LAG):")
df.withColumn("prev_amount", lag("amount", 1).over(lag_window)) \
  .withColumn("amount_change",
              when(col("prev_amount").isNull(), lit("FIRST_ORDER"))
              .when(col("amount") > col("prev_amount"), lit("INCREASED"))
              .otherwise(lit("DECREASED"))) \
  .orderBy("customer_name", "order_date").show()

# =============================================================================
# PROBLEM 3: Broadcast Join
# =============================================================================

# Small dimension table — broadcast to avoid shuffle
dim_data = [
    ("Electronics", "High Margin", "Online"),
    ("Books", "Medium Margin", "Online"),
    ("Food", "Low Margin", "Retail"),
]

dim_schema = StructType([
    StructField("category", StringType(), True),
    StructField("margin_tier", StringType(), True),
    StructField("channel", StringType(), True),
])

dim_df = spark.createDataFrame(dim_data, dim_schema)

# Use broadcast hint for the small table
print("Broadcast join (no shuffle!):")
result = df.join(dim_df.hint("broadcast"), "category")
result.explain()  # Check plan — should show BroadcastHashJoin
result.show(5)

# =============================================================================
# PROBLEM 4: explode + pivot
# =============================================================================

# Array data — customers with multiple tags
tag_data = [
    ("Alice", ["premium", "high_spender", "electronics_fan"]),
    ("Bob", ["standard", "electronics_fan"]),
    ("Charlie", ["premium", "foodie"]),
    ("Diana", ["standard"]),
]

tag_df = spark.createDataFrame(tag_data, ["customer_name", "tags"])

print("Exploded tags:")
tag_df.select("customer_name", explode("tags").alias("tag")).show()

# Pivot — count customers per tag
print("Pivot — customers per tag:")
tag_df.select("customer_name", explode("tags").alias("tag")) \
    .groupBy("tag").count().orderBy(desc("count")).show()

# =============================================================================
# PROBLEM 5: Schema Management
# =============================================================================

# Explicit schema — ALWAYS prefer this over inferSchema
print("Using explicit schema (faster for large data):")
orders_schema = StructType([
    StructField("order_id", IntegerType(), False),
    StructField("customer_name", StringType(), True),
    StructField("amount", DoubleType(), True),
])

explicit_df = spark.createDataFrame([], orders_schema)
print(f"Schema: {explicit_df.schema.simpleString()}")

# =============================================================================
# PROBLEM 6: Pandas UDF (Vectorized, 10-100x faster than Python UDF)
# =============================================================================

# Regular Python UDF (slow — row-by-row Python overhead)
def spend_category_python(amount):
    if amount > 400:
        return "High"
    elif amount > 200:
        return "Medium"
    else:
        return "Low"

spend_udf = udf(spend_category_python, StringType())

print("Python UDF result:")
df.withColumn("spend_tier_python", spend_udf("amount")).show(5)

# Pandas UDF (vectorized — uses Apache Arrow, much faster)
@pandas_udf(StringType(), PandasUDFType.SCALAR)
def spend_category_pandas(amount_series):
    import pandas as pd
    return pd.cut(
        amount_series,
        bins=[0, 200, 400, float('inf')],
        labels=["Low", "Medium", "High"]
    )

print("Pandas UDF result (10-100x faster!):")
df.withColumn("spend_tier_pandas", spend_category_pandas("amount")).show(5)

# =============================================================================
# PROBLEM 7: Handling Nulls & Deduplication
# =============================================================================

# Create data with nulls and duplicates
messy_data = [
    (1, "Alice", 250.00, "2026-01-15"),
    (2, "Bob", None, "2026-01-16"),
    (3, "Alice", 250.00, "2026-01-15"),  # Duplicate
    (4, None, 320.00, "2026-03-20"),
    (5, "Bob", None, "2026-04-10"),
]

messy_df = spark.createDataFrame(messy_data, ["id", "name", "amount", "date"])

print("Messy data (nulls + duplicates):")
messy_df.show()

# Fill nulls
print("Fill null amount with 0:")
messy_df.fillna({"amount": 0.0}).show()

# Drop rows where name is null
print("Drop rows with null name:")
messy_df.na.drop(subset=["name"]).show()

# Deduplication
print("Deduplicated (by all columns):")
messy_df.dropDuplicates().show()

# Window-based dedup — keep latest per customer
window_dedup = Window.partitionBy("name").orderBy(desc("date"))
print("Window-based dedup (latest per customer):")
messy_df.withColumn("rn", row_number().over(window_dedup)) \
    .filter(col("rn") == 1).drop("rn").show()

# =============================================================================
# PROBLEM 8: Read/Write Modes
# =============================================================================

# Write with partition + mode
print("\n--- Write Modes ---")
print("  overwrite  — replace entire table/partition")
print("  append     — add new data")
print("  ignore     — skip if exists")
print("  errorIfExists — raise error if exists (default)")

# Example (commented out — requires actual storage):
# df.write.format("delta") \
#   .mode("overwrite") \
#   .partitionBy("category") \
#   .save("s3://bucket/gold/orders")

# =============================================================================
# PROBLEM 9: Spark SQL — MERGE INTO (Delta Lake)
# =============================================================================

print("\n--- MERGE INTO (Delta Upsert) ---")
print("""
MERGE INTO silver.customers AS target
USING staging.customers AS source
ON target.customer_id = source.customer_id
WHEN MATCHED THEN UPDATE SET
    target.customer_name = source.customer_name,
    target.updated_at = current_timestamp()
WHEN NOT MATCHED THEN INSERT
    (customer_id, customer_name, created_at)
VALUES
    (source.customer_id, source.customer_name, current_timestamp())
""")

# =============================================================================
# PROBLEM 10: Query Optimization — EXPLAIN
# =============================================================================

print("\n--- Query Plan Analysis ---")
# Create a larger test
test_df = df.groupBy("customer_name").agg(
    sum("amount").alias("total"),
    avg("amount").alias("avg_amount")
).filter(col("total") > 300)

print("Query plan (Physical):")
test_df.explain(mode="formatted")

# =============================================================================
# PROBLEM 11: Partition Pruning Example
# =============================================================================

print("\n--- Partition Pruning ---")
print("""
# When data is partitioned by date, filter on date column:
# spark.read.parquet("s3://bucket/orders/") \\
#   .filter(col("order_date") >= "2026-03-01")  <- reads only relevant partitions!
# 
# Always include partition columns in WHERE for large datasets.
""")

# =============================================================================
# PROBLEM 12: Handling Skew — Salting
# =============================================================================

print("\n--- Handling Skewed Joins with Salting ---")
print("""
# Problem: One key ('USA') has 80% of data, one executor overloaded
# Solution: Add salt to redistribute

from pyspark.sql.functions import concat, lit, floor, rand

# Add salt column (0 to N-1)
skewed_df = df.withColumn(
    "salted_key", 
    concat(col("customer_name"), lit("_"), (floor(rand() * 10)).cast("int"))
)

# Join on salted_key instead of customer_name
# Also salt the small table for the join
""")

print("\n=== END OF PYSPARK PRACTICE ===")

spark.stop()