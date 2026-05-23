"""
DAY 2 — ADVANCED DATA ENGINEERING DEEP DIVE
Interview: 26 May 2026

Topics: Distributed Systems (CAP), Spark Deep (Memory, Tuning, Joins, Streaming),
        Delta Lake (Internals, Operations, Medallion), Kafka (Concepts, Spark Integration),
        Data Modeling & Quality, Airflow, AWS
"""

# =============================================================================
# PART 1: CAP THEOREM — INTERVIEW Q&A
# =============================================================================

"""
Q: Explain CAP theorem and how it applies to distributed data pipelines.
A: CAP says you can guarantee only 2 of 3: Consistency, Availability, Partition Tolerance.
   In distributed systems, P is non-negotiable (network partitions WILL happen).
   So you choose CP or AP.

   - CP (Consistency + Partition Tolerance): All nodes see same data. 
     Example: HBase, Zookeeper. Trade-off: writes blocked if nodes can't sync.
     - Banking system: CP to ensure no 2 balance amounts exist. If network fails, better to reject transactions than allow stale reads.

   - AP (Availability + Partition Tolerance): System stays up even if nodes out of sync.
     Example: Cassandra, DynamoDB. Trade-off: stale reads possible.
     - Social media feed: AP is fine since eventual consistency is acceptable. Better to show slightly old posts than no posts at all.
     Or 102 likes instead of 105.
   - CA (Consistency + Availability): Only in single-node systems. Not distributed.

   For pipelines: Choose AP so reads never block. Downstream can tolerate eventual consistency.
   For financial transactions: CP to avoid double-counting.
"""


# =============================================================================
# PART 2: DATA PARTITIONING & SKEW HANDLING
# =============================================================================

"""
PARTITIONING STRATEGIES:
  - Hash: hash(key) % numPartitions — even distribution, but can't skip partitions on read
  - Range: partition by value range — enables partition pruning on filter queries
  - List: partition by discrete values (e.g., country = 'IN', 'US', 'UK')

SKEW PROBLEM:
  80% of data has same key → 1 executor processes 80% → job fails or slows dramatically

FIX WITH SALTING:
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat, lit, floor, rand

spark = SparkSession.builder.appName("skew_example").getOrCreate()

# Simulated skewed data
data = [("USA", i) for i in range(800)] + \
       [("IN", i) for i in range(100)] + \
       [("UK", i) for i in range(100)]

df = spark.createDataFrame(data, ["country", "value"])

# Add salt to redistribute
NUM_SALTS = 10
salted_df = df.withColumn(
    "salted_country",
    concat(col("country"), lit("_"), (floor(rand() * NUM_SALTS)).cast("int"))
)

# Now data is spread across 10× more partitions
salted_df.groupBy("salted_country").count().orderBy("salted_country").show()

"""
REPARTITION vs COALESCE:
  - repartition(num): full shuffle, increases or decreases partitions
  - coalesce(num): merges partitions without full shuffle (decrease only)
  - Use coalesce when reducing partitions (no shuffle), repartition when increasing
"""


# =============================================================================
# PART 3: SPARK EXECUTION MODEL
# =============================================================================

"""
SPARK EXECUTION FLOW:
  1. Driver builds DAG from transformations (lazy)
  2. Action triggers DAG Scheduler to create stages
  3. Stages = groups of tasks that can run without shuffle
  4. Task Scheduler assigns tasks to executors
  5. Executors run tasks in parallel

KEY CONCEPTS:
  - Transformations: filter, map, select (lazy — build DAG nodes)
  - Actions: count, collect, save (trigger execution)
  - Narrow dependency: each partition → at most 1 child partition (no shuffle)
  - Wide dependency: each partition → multiple child partitions (shuffle needed)
  - Stage boundary = shuffle operation

LAZY EVALUATION:
  - Why it matters: allows Catalyst optimizer to reorder/combine operations
  - Debugging tip: if .count() is slow, check what transformations went before it

CATALYST OPTIMIZER:
  - Rule-based: predicate pushdown, constant folding, column pruning
  - Cost-based: chooses join strategy based on table stats
  - Tungsten: generates optimized bytecode, uses off-heap memory
"""


# =============================================================================
# PART 4: SPARK MEMORY MANAGEMENT
# =============================================================================

"""
MEMORY HIERARCHY:
  - On-heap: JVM heap. Subject to GC pauses.
  - Off-heap: Direct memory (Tungsten). No GC, faster serialization.

SPARK MEMORY FRACTIONS (spark.memory.fraction = 0.6):
  - 60%: Unified Execution + Storage (shared)
  - 40%: Reserved for user code (UDFs, internal metadata)

Within the 60%:
  - Execution: shuffle buffers, join hashes, aggregation
  - Storage: cached DataFrames/RDDs
  - When execution needs more, it can evict storage (but not the other way around)

OOM FIXES:
  1. Increase executor memory: spark.executor.memory
  2. Reduce caching: cache only what's reused
  3. Persist with MEMORY_AND_DISK instead of MEMORY_ONLY
  4. Increase parallelism: more partitions = less data per task
  5. Tune spark.memory.fraction / spark.memory.storageFraction
"""


# =============================================================================
# PART 5: SPARK PERFORMANCE TUNING
# =============================================================================

"""
AQE (Adaptive Query Execution) — spark.sql.adaptive.enabled=true:
  1. Dynamically coalesces shuffle partitions
  2. Dynamically switches join strategy (sort-merge → broadcast hash)
  3. Dynamically handles skew join (splits skewed partitions)

TUNING CONFIG QUICK REFERENCE:
  spark.sql.shuffle.partitions = 200 (default) → 2-3x number of cores
  spark.sql.autoBroadcastJoinThreshold = 10MB (default)
  spark.sql.adaptive.coalescePartitions.parallelismFirst = false
  spark.sql.adaptive.coalescePartitions.minPartitionSize = 10MB
  spark.sql.adaptive.coalescePartitions.initialPartitionNum = 200
  spark.serializer = org.apache.spark.serializer.KryoSerializer
  spark.sql.adaptive.skewJoin.enabled = true
  spark.sql.adaptive.skewJoin.skewedPartitionFactor = 5
  spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes = 256MB

EXPLAIN() PATTERNS:
  - df.explain() — physical plan summary
  - df.explain("formatted") — detailed plan with costs
  - df.explain("codegen") — generated Java code
"""


# =============================================================================
# PART 6: SPARK JOINS
# =============================================================================

"""
JOIN TYPES IN SPARK:
  - Broadcast Hash Join: small table ≤ threshold → copied to all executors. O(n), no shuffle.
  - Sort-Merge Join: large-to-large. Sort both sides by join key, then merge. O(n log n)
  - Shuffle Hash Join: one side fits in hash table. Shuffle both, build hash from smaller.

WHEN EACH IS USED:
  - Fact table (100TB) + Dim table (1MB) → Broadcast Hash Join (hint it!)
  - Fact table + Fact table → Sort-Merge Join (default)
  - Medium table + Medium table → Shuffle Hash Join (if one fits in hash)

FORCING JOIN TYPE:
  df1.join(df2.hint("broadcast"), "key")        # Broadcast
  df1.join(df2.hint("shuffle_hash"), "key")     # Shuffle Hash  
  df1.join(df2.hint("sort_merge"), "key")       # Sort Merge
  df1.join(df2.hint("shuffle_replicate_nl"), "key")  # Cartesian (danger!)
"""


# =============================================================================
# PART 7: STRUCTURED STREAMING
# =============================================================================

"""
STREAMING CONCEPTS:
  - Input Table → unbounded, continuously appended to
  - Result Table → updated every trigger interval
  - Output to sink: Complete, Append, Update modes

WATERMARKING:
  - Defines how late data can arrive and still be processed
  - window = "1 hour", watermark = "10 minutes" → data up to 10min late included
  - After watermark passes, late data is discarded

CHECKPOINTING:
  - Stores offset positions, schema, state info
  - Enables exactly-once or at-least-once semantics
  - Must point to different location than data output

TRIGGER TYPES:
  - processingTime("10 seconds") → micro-batch every 10s
  - once() → run one batch, then stop (batch-on-demand)
  - availableNow() → process all available, then stop
  - continuous() → low-latency (milliseconds), experimental

STREAMING + KAFKA CODE PATTERN:
"""

from pyspark.sql.functions import col, from_json, window
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

kafka_schema = StructType([
    StructField("event_id", StringType()),
    StructField("user_id", StringType()),
    StructField("event_type", StringType()),
    StructField("amount", DoubleType()),
    StructField("timestamp", StringType()),
])

# Read from Kafka
streaming_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker1:9092,broker2:9092") \
    .option("subscribe", "user_events") \
    .option("startingOffsets", "earliest") \
    .option("maxOffsetsPerTrigger", 10000) \
    .load()

# Parse JSON from Kafka value
parsed_df = streaming_df \
    .select(from_json(col("value").cast("string"), kafka_schema).alias("data")) \
    .select("data.*")

# Aggregation with watermark
aggregated = parsed_df \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(
        window(col("timestamp"), "1 hour", "30 minutes"),
        col("event_type")
    ).count()

# Write to Delta sink
query = aggregated.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "s3://checkpoints/user_events/") \
    .option("path", "s3://gold/streaming_events/") \
    .trigger(processingTime="10 seconds") \
    .start()

query.awaitTermination()


# =============================================================================
# PART 8: DELTA LAKE DEEP DIVE
# =============================================================================

"""
DELTA LAKE INTERNALS:
  - _delta_log/ contains JSON transaction log entries
  - Each entry = atomic commit (add/remove file + metadata)
  - Parquet data files + JSON metadata = ACID on object store
  - Snapshot isolation: readers see consistent state from when query started
  - Optimistic concurrency control: writers detect conflicts, retry

TIME TRAVEL:
  df.read.format("delta").option("versionAsOf", 42).load("path")
  df.read.format("delta").option("timestampAsOf", "2026-05-20").load("path")

SCHEMA EVOLUTION:
  .option("mergeSchema", "true") — allows adding new columns

DELTA OPERATIONS:
  - OPTIMIZE: coalesce small files into larger ones
  - ZORDER BY (col1, col2): multi-dimensional clustering for read skipping
  - VACUUM: remove files older than retention (default 7 days)
  - DESCRIBE HISTORY: see table lineage
  - FSCK REPAIR TABLE: fix metastore after manual file changes

MEDALLION ARCHITECTURE:
  Bronze ──ingestion──► Silver ──cleaning──► Gold
  │ Raw, append-only    │ Cleaned, deduped   │ Aggregated, business-ready
  │ Schema on read      │ Quality validated  │ Denormalized for consumers
  
  Quality gates: validate schema, dedup, check nulls, data quality constraints
"""

# Delta MERGE INTO (SCD Type 2 example)
print("""
MERGE INTO silver.customers AS target
USING (
  SELECT src.*, current_timestamp() AS effective_date
  FROM staging.customers_updates src
) AS source
ON target.customer_id = source.customer_id

-- Type 1: Update current address
WHEN MATCHED AND target.is_current = true 
    AND target.address <> source.address THEN
  UPDATE SET 
    address = source.address,
    updated_at = current_timestamp()

-- Type 2: Close old record, insert new
WHEN MATCHED AND target.is_current = true 
    AND target.address <> source.address THEN
  UPDATE SET 
    is_current = false,
    end_date = current_timestamp()

WHEN NOT MATCHED THEN
  INSERT (customer_id, name, address, is_current, start_date)
  VALUES (source.customer_id, source.name, source.address, true, current_timestamp())
""")


# =============================================================================
# PART 9: KAFKA DELIVERY SEMANTICS
# =============================================================================

"""
DELIVERY SEMANTICS:
  1. At-most-once: Message sent once → may be lost but never duplicated
     - Auto-commit offset, may fail after sending but before processing
  2. At-least-once: Message retried until acknowledged → may duplicate
     - Manual offset commit after processing → if fails, same message re-processed
  3. Exactly-once: Each message processed exactly once
     - Requires: idempotent producer (enable.idempotence=true) 
       + transactional consumer (isolation.level=read_committed)
     - Non-trivial: need dedup or idempotent sink

CONSUMER OFFSET MANAGEMENT:
  - auto-commit: easy but can lose messages (at-most-once)
  - manual commit: harder but reliable (at-least-once)
  - commitSync: blocks until acknowledged
  - commitAsync: non-blocking, but can miss failures

REPLICATION:
  - Replication factor: 3 is typical for production
  - ISR (In-Sync Replicas): replicas that are fully caught up with leader
  - min.insync.replicas: minimum ISR for write acceptance
  - acks=all: write must be replicated to all ISR before acknowledgment
"""


# =============================================================================
# PART 10: SPARK + KAFKA INTEGRATION
# =============================================================================

"""
STREAMING FROM KAFKA:
  Option                        | When to use
  ──────────────────────────────┼──────────────────────────────────
  startingOffsets="earliest"   | First run, want all historical data
  startingOffsets="latest"     | Subsequent runs, only new messages
  maxOffsetsPerTrigger=10000   | Rate limit to avoid backpressure

SCHEMA HANDLING:
  - Kafka messages often use Avro + Schema Registry
  - Use from_avro() function with schema registry integration
  - For JSON: from_json(col("value").cast("string"), schema)
  
ERROR HANDLING:
  - Corrupt records: use .option("failOnDataLoss", "false")
  - Dead letter queue: write failed records to separate topic
"""

# =============================================================================
# PART 11: AIRFLOW ADVANCED
# =============================================================================

"""
AIRFLOW KEY CONCEPTS (for interview):
  - DAG: Directed Acyclic Graph defining pipeline structure
  - Operator: Single task (PythonOperator, BashOperator, SparkSubmitOperator)
  - XCom: Cross-communication — push/pull data between tasks (small data only!)
  - Sensor: Waits for external condition (file arrival, data availability)
  - TaskGroup: Group tasks visually (replaced SubDAG — SubDAGs share scheduler)

ADVANCED:
  - Dynamic DAGs: generate DAGs from YAML config
  - SLA miss callback: alert if task exceeds expected duration
  - Pool: limit concurrent execution slots
  - Catchup: backfill missed DAG runs
  - LatestOnly: skip if DAG wasn't scheduled on time
"""


# =============================================================================
# PART 12: S3 BEST PRACTICES
# =============================================================================

"""
S3 PARTITIONING STRATEGY:
  Good:  s3://bucket/dt=2026-05-22/country=IN/file.parquet
  Avoid: s3://bucket/2026/05/22/IN/file.parquet  (no partition metadata)

ATHENA OPTIMIZATION:
  - Use columnar formats (Parquet/ORC)
  - Partition projection: define partition pattern to skip catalog lookup
  - Compress with Snappy (balance of speed and size)
  - Avoid SELECT *, use column pruning

EMR COST SAVING:
  - Task nodes on Spot instances: 60-70% cheaper
  - Fallback to on-demand if spot interrupted
  - Right-size cluster: 4-5 cores/executor, 4GB RAM/core
  - Use EMRFS consistent view for S3
"""

print("=== END OF DAY 2 — ADVANCED DE DEEP DIVE ===")
print("Next: Continue with GenAI (separate file)")