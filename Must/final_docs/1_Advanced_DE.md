# Advanced Data Engineering — Apache Spark & Modern Data Stack

> A comprehensive interview preparation guide covering Apache Spark, Delta Lake, Data Modeling, Airflow, Storage Formats, AWS EMR, Athena, and Glue.

---

## Table of Contents

1. [Apache Spark](#apache-spark)
2. [Spark Execution Model](#spark-execution-model)
3. [Debugging Slow EMR Jobs](#debugging-slow-emr-jobs)
4. [Partitioning & Skew](#partitioning--skew)
5. [Spark Shuffle & Performance Tuning](#spark-shuffle--performance-tuning)
6. [Spark Memory Management](#spark-memory-management)
7. [Spark Join Types](#spark-join-types)
8. [Streaming](#streaming)
9. [Delta Lake](#delta-lake)
10. [Data Modeling — SCD Types](#data-modeling--scd-types)
11. [Data Quality & Anomaly Detection](#data-quality--anomaly-detection)
12. [Airflow Advanced Concepts](#airflow-advanced-concepts)
13. [Data Storage Formats](#data-storage-formats)
14. [AWS EMR Deep Dive](#aws-emr-deep-dive)
15. [AWS Athena & Glue](#aws-athena--glue)

---

## Apache Spark

Apache Spark is a unified, open-source, distributed data-processing engine designed for speed and ease of use. It provides high-level APIs in Java, Scala, Python, and R, and an optimized engine that supports general execution graphs.

---

## Spark Execution Model

| Component | Role |
|-----------|------|
| **Driver** | Coordinates execution, maintains metadata, and handles job scheduling. Runs the main program and creates `SparkContext`. |
| **Executors** | Run tasks and store data. |
| **Tasks** | Units of work sent to executors. |
| **Stages** | Sets of tasks that can be executed in parallel. |
| **DAG** | Directed Acyclic Graph representing the execution plan. |
| **Lazy Evaluation** | Transformations build a plan but are not executed immediately. |
| **Actions** | Trigger execution of the plan. |
| **Catalyst Optimizer** | Rewrites the logical plan for optimization. |
| **Tungsten** | Optimizes memory and CPU usage for better performance. |

---

### Debugging a Slow EMR Job

> Check the **DAG** in the Spark UI to find the stage causing **shuffle spill**, not just the final action.

- Use **Spark UI** to identify stages with shuffle spill and optimize those stages.
- Consider:
  - Optimizing data partitioning
  - Reducing data shuffling
  - Tuning Spark configurations to mitigate shuffle spill

---

## Partitioning & Skew

### Partitioning Types

#### Hash Partitioning

- Distributes data based on the hash of the key.
- Ensures data is distributed evenly across partitions, improving performance and reducing skew.
- **Problem**: Does not work well with range queries — does not preserve data order, leading to inefficient queries.

#### Range Partitioning

- Distributes data based on a range of key values (e.g., timestamp partitioned by daily or monthly ranges).
- **Advantage**: Preserves order, great for range queries.
- **Problem**: Can lead to data skew if data is not evenly distributed across ranges.

#### Custom Partitioning

- Allows users to define their own partitioning logic (e.g., by geographic location or customer segment).
- Ensures related data is stored together, reducing data shuffling.

### Partition Pruning

- A technique that allows Spark to **skip reading unnecessary partitions** when executing a query.
- **Example**: If a table is partitioned by `date` and the query filters for a specific date range, Spark prunes irrelevant partitions, resulting in faster query execution.

### Data Skew & Fixes

**Data skew** occurs when one or more partitions contain significantly more data than others, leading to uneven workload distribution (e.g., one executor processes 80% of data while others are idle).

#### Fixes for Data Skew

| Technique | Description |
|-----------|-------------|
| **Salting** | Add a random prefix to the key to distribute data more evenly. |
| **`repartition()`** | Redistributes data across partitions to ensure even distribution. |
| **`coalesce()`** | Reduces the number of partitions (combines small partitions into larger ones) to create more balanced workloads. |
| **AQE Skew Join Hints** | Adaptive Query Execution can automatically detect skewed keys and apply optimizations. |

#### Adaptive Query Execution (AQE)

> Enabled by default in Spark 3.0+ (`spark.sql.adaptive.enabled=true`).

**Key Difference**: The **Catalyst optimizer** performs static optimizations before execution, while **AQE** makes dynamic adjustments during runtime based on actual data characteristics.

**Optimizations AQE can apply:**

- Dynamically coalescing shuffle partitions based on data size.
- Dynamically optimizing **skewed joins** — splitting skewed keys into multiple partitions or using a different join strategy.
- Dynamically optimizing **join strategies** — switching from sort-merge join to broadcast join when appropriate.
- Dynamically optimizing **aggregate operations** by adjusting the number of reducers based on data size.

---

## Spark Shuffle & Performance Tuning

### Operations That Trigger a Shuffle

| Operation | Explanation |
|-----------|-------------|
| **`groupBy`** | Redistributes data to group records by key. Optimize by reducing shuffle partitions or using combiners (functions that combine multiple values into one). |
| **`join`** | Shuffles data to align keys from both datasets. Large datasets use **sort-merge join (SMJ)** by default; small datasets can use **broadcast join** to avoid shuffling. |
| **`repartition()`** | Explicitly redistributes data across a specified number of partitions. Increases parallelism but involves a full shuffle. |

### Tuning Shuffle Partitions

> **Configuration**: `spark.sql.shuffle.partitions` (default: `200`)

- Set to **2–3× the number of cores** in your cluster for better parallelism.
- Optimal value depends on workload and cluster configuration — experimentation is recommended.

### AQE (`spark.sql.adaptive.enabled=true`)

- Enabled by default in Spark 3.0+.
- Dynamically optimizes query execution plans based on runtime statistics.
- The major difference from the **Catalyst optimizer**: AQE adjusts the execution plan during runtime based on actual data characteristics, while Catalyst performs static optimizations on the logical plan before execution.

### Kryo Serialization

- **Serialization** converts data into a byte format for network transfer or disk storage.
- **Kryo** is a more efficient serialization format than the default Java serialization.
- Reduces the amount of data transferred during shuffles, improving performance.

### Why Does Spark Require the JVM?

- Spark was originally developed in **Scala**, which runs on the **JVM**.
- The JVM provides a **platform-independent** environment for running Spark applications.
- **Performance impact**:
  - **Garbage collection (GC)** can cause pauses in execution.
  - Memory management can lead to `OutOfMemory` errors if not properly configured.

### What Is Garbage Collection in Spark?

- GC is the process of automatically freeing memory no longer in use.
- Important in Spark because applications consume large amounts of memory.
- Proper GC tuning prevents performance issues and application failures.

---

## Spark Memory Management

### Components of an EMR Cluster

| Component | Description |
|-----------|-------------|
| **Master Node** | Manages the cluster and coordinates worker nodes. |
| **Worker Nodes** | Run the Spark jobs. |
| **Job Tracker** | Tracks job progress and manages allocated resources. |
| **Task Tracker** | Tracks task-level progress within a job. |
| **HDFS** | Distributed file system for storing data — scalable and fault-tolerant. S3 is object storage, not designed for large-scale processing like HDFS. |
| **YARN** | Resource manager that allocates resources to Spark jobs. |

### Storage Categorization in Spark

| Type | Description |
|------|-------------|
| **On-Heap Memory** | Managed by the JVM. Used for RDDs, DataFrames, and intermediate data structures. |
| **Off-Heap Memory** | Allocated outside the JVM heap. Used for serialized data or shuffle operations. |

Both types are part of **RAM** and critical for Spark performance.

### Unified Memory Management

- Allows **dynamic allocation** of memory between **execution** (shuffling, sorting, aggregations) and **storage** (caching, persisting).
- Automatically adjusts based on workload and available resources.
- Improves performance and resource utilization.
- Contrasts with **static memory management**, which requires manual configuration.

### Checkpointing in Spark

- Saves the state of an RDD or DataFrame to a reliable storage system (e.g., HDFS).
- Provides **fault tolerance** — if a node fails, processing can resume from the checkpoint.
- Particularly important for **long-running applications** or complex transformations.

### Checkpoint vs. Cache/Persist

| Aspect | Checkpoint | Cache/Persist |
|--------|------------|---------------|
| Purpose | Fault tolerance & recovery | Performance optimization |
| Storage | Writes to disk (slower) | Stores in memory (faster) |
| Durability | Yes — survives application failures | No — data may be lost on failure |

---

## Spark Join Types

### Hash Join

- Uses a hash function to partition data based on the join key.
- Used when **one table is small enough to fit in memory**.
- Creates a hash table for the smaller table, then probes it with the larger table.
- More efficient than sort-merge join for certain workloads (skewed keys, unsorted keys).

### Broadcast Hash Join (BHJ)

> Used when the **small table fits in memory** — **no shuffle** required.

- Spark broadcasts the smaller table to all executors, then performs a hash join locally.

### Broadcast Hash Join vs. Broadcast Nested Loop Join

| Type | When Used | Efficiency |
|------|-----------|------------|
| **Broadcast Hash Join** | Small table fits in memory | More efficient — builds a hash table for fast lookups |
| **Broadcast Nested Loop Join** | Small table cannot fit in memory | Less efficient — iterates row-by-row, comparing each row of the larger table with each row of the smaller table |

### Sort-Merge Join (SMJ)

> Default for **large-large** joins. Both sides are sorted + shuffled.

- Spark sorts both tables by the join key, then merges matching rows.
- Efficient for large datasets, but shuffle and sort operations can cause performance issues.

### Shuffle Hash Join (SHJ)

- Used when one table is small enough for in-memory hashing but too large to broadcast.
- Spark partitions the larger table by join key, then performs a hash join within each partition.
- Hint: `/*+ BROADCAST(t) */` or configure `autoBroadcastJoinThreshold`.

### Two Large Tables Joined on `user_id`

- **Default**: Sort-Merge Join (SMJ).
- If `user_id` is **skewed** (e.g., power users dominate data), **add salting**:
  - Create a `salted_user_id` column by concatenating a random prefix with the original `user_id`.
  - Use the salted key for the join to distribute data evenly.

---

## Streaming

### Batch vs. Streaming

| Batch Processing | Streaming |
|-----------------|-----------|
| Finite set of data | Continuous flow of data |
| Processes data at rest | Processes data in real-time as it arrives |

### Key Components of a Streaming Application

| Component | Description |
|-----------|-------------|
| **Source** | Origin of streaming data (e.g., Kafka, Kinesis, file system). |
| **Stream Processing Engine** | Processes the streaming data (e.g., Spark Structured Streaming, Flink, Storm). |
| **Sink** | Destination for processed data (e.g., database, file system, messaging system). |
| **Sharding** | Divides streaming data into smaller chunks (shards) for parallel processing. |
| **Partitioning** | Divides data into partitions based on a key for efficient processing. |

### Key Streaming Concepts

| Concept | Description |
|---------|-------------|
| **Micro-Batch Processing** | Processes data in small batches — near real-time with fault tolerance (default in Spark Structured Streaming). |
| **Continuous Processing** | Processes data as it arrives — even lower latency (Spark 2.3+). |
| **Watermarking** | Handles late data. Example: `.withWatermark('ts', '10 minutes')` — data arriving >10 min after event time is considered late. |
| **Triggers** | Control when the query executes: `processingTime` (e.g., every 10s), `once` (single run), `availableNow` (process all available then stop). |
| **Checkpointing** | Saves streaming query state at intervals for fault tolerance and recovery. |

### Spark Structured Streaming

- Solves the need for a **unified API** for both batch and streaming.
- Treats streaming data as an **unbounded table** continuously updated as new data arrives.
- Uses familiar **DataFrame/Dataset APIs** — write once, run in batch or streaming.

```
Streaming DataFrame / Dataset
           │
           ▼
    Unbounded Table
           │
           ▼
    Micro-Batch (default)  ─── or ───  Continuous
           │
           ▼
        Sink
```

---

## Delta Lake

### Checkpointing in Delta Lake

- Saves the state of the Delta Lake at a specific point in time.
- Stores metadata and data changes for **efficient recovery** and **time travel**.
- **Critical benefit**: Consolidates thousands of small JSON transaction log files into a single checkpoint file, reducing memory overhead and improving read performance.

### Do Users Need to Manage Checkpoints?

> No — Delta Lake **automatically manages checkpoints** at regular intervals. Users can configure the frequency but do not need to manually create or manage them.

### Contents of a JSON File in the Delta Log

Each JSON file contains metadata about an operation performed on the Delta Lake:

- Type of operation (insert, update, delete)
- Timestamp of the operation
- User who performed the operation

### Optimistic Concurrency Control (OCC)

- Allows multiple users to read and modify the same data simultaneously.
- **Checks for conflicts before committing** — if a conflict is detected, one transaction is rolled back and must be retried.

**How OCC ensures ACID properties:**

| Property | How OCC Ensures It |
|----------|-------------------|
| **Atomicity** | Transaction either succeeds completely or fails completely — conflict detection triggers a rollback, preventing partial updates. |
| **Consistency** | Conflict checks before committing maintain data validity. |
| **Isolation** | Concurrent transactions do not interfere with each other. |
| **Durability** | Transaction log + checkpointing ensure committed transactions persist even after failures. |

### `MERGE INTO` (Upsert)

> **Match → Update, No Match → Insert**

- Enables **upserts** in a single atomic statement.
- Possible in a lakehouse architecture thanks to **ACID properties** and **optimistic concurrency control**.
- Ideal for **slowly changing dimensions (SCD)** and incremental data processing.

### `OPTIMIZE` (File Compaction)

- Compacts many small files into larger ones to improve query performance.
- Recommended after every **10–20 updates/inserts** (depends on workload).
- **How it works internally**: Reads small files and writes them back as larger files through file compaction, maintaining data integrity.

### `ZORDER BY` (Data Co-location)

- Co-locates related data in the same files for **skip-friendly reads**.
- **Example**: If frequently filtering by `user_id`, `ZORDER BY user_id` allows Spark to skip irrelevant files.
- Especially useful for **multi-column filtering**.

### Indexing vs. `ZORDER BY`

| Aspect | Indexing | `ZORDER BY` |
|--------|----------|-------------|
| Purpose | Fast lookups via a data structure | Physically co-locate related data |
| Implementation | Creates a separate data structure (e.g., B-tree, hash index) | Rewrites file layout |
| Use Case | Frequently filtered columns | Multi-column / range filters |

### How Indexing Works in the Backend

1. Enabling indexing for a column creates a data structure (e.g., **B-tree** or hash index).
2. The index is built by scanning the data and creating entries for each unique value, along with pointers to the corresponding records in data files.
3. **B-tree** organizes values hierarchically — each node contains a range of values and pointers to file locations.
4. When filtering on the indexed column, Spark quickly navigates the B-tree to find relevant entries, skipping irrelevant data.

> **Best columns to index**: Columns with **higher cardinality** (more unique values) and frequently used in query filters (e.g., `user_id`). Indexing a column with unique values for every record (e.g., `transaction_id`) may offer less performance benefit compared to columns with repeated values.

### `VACUUM` (Old File Removal)

- Removes old files no longer needed for the current state.
- **Default retention**: 7 days (for time travel and recovery).
- Example: `VACUUM my_table RETAIN 3 HOURS`
- **Caution**: Once files are removed, they **cannot be recovered** — always take a backup before running `VACUUM`.

**How to ensure necessary files are not deleted:**

1. **Review the retention period** — ensure it is appropriate for your use case.
2. **Take a backup** — especially for critical data.
3. **Monitor the process** — check logs and metrics to verify the operation completes successfully.

> Tools like `VACUUM`, `OPTIMIZE`, and checkpointing are **crucial** for maintaining Delta Lake health and performance, but must be used with caution to avoid unintended data loss.

### `DESCRIBE HISTORY` (Audit)

- Retrieves the history of operations performed on a Delta Lake table.
- Shows operation type, timestamp, and user.
- Useful for **auditing**, **debugging**, and **troubleshooting**.

### Medallion Architecture

Data organized into layers with increasing levels of quality and transformation.

```
 Bronze ──► Silver ──► Gold
 (raw)     (clean)    (aggregated)
```

#### Bronze Layer (Raw Ingestion)

- **Schema-on-read**, append-only.
- Usually partitioned on `insert_date`.
- Contains raw, unprocessed data.
- **Source of truth** for reprocessing and recovery.

#### Silver Layer (Cleaned & Validated)

- Cleaned, deduplicated, validated data.
- **Schema enforced**.
- Handles missing values, removes duplicates.
- Prepared for further analysis or transformation.

#### Gold Layer (Business-Ready)

- Aggregated, business-ready, optimized for consumption.
- Additional optimizations: indexing, partitioning.
- Designed for **reporting, analytics, and downstream applications**.

> **Quality gates** are enforced between each layer.

---

## Data Modeling — SCD Types

**SCD** stands for **Slowly Changing Dimension** — a technique to manage and track changes to dimensional data over time.

| SCD Type | Behavior | History |
|----------|----------|---------|
| **Type 1** | Overwrite existing record with new values. | No history maintained. |
| **Type 2** | New row per change with start/end dates. | Full history preserved. |
| **Type 3** | Add a column to store the previous value. | Tracks previous value in same row. |
| **Type 6** | Hybrid — combination of Type 1, 2, and 3. | Flexible approach per attribute. |

> **Delta `MERGE INTO`** is the standard implementation for **Type 2 SCD**, performing upserts (updates + inserts) in a single operation.

---

## Data Quality & Anomaly Detection

### Data Quality Dimensions

| Dimension | Description |
|-----------|-------------|
| **Completeness** | Are all required fields present? Checks for nulls, missing values. |
| **Accuracy** | Does data correctly represent real-world values? Validate against known standards. |
| **Consistency** | Is data uniform and free of contradictions across datasets and over time? |
| **Timeliness** | Is data up-to-date and available when needed? Monitor data latency. |
| **Uniqueness** | Are there duplicate records? Identify and remove duplicates. |

### Tools

- **Great Expectations**
- **Deequ**

### Lakehouse Monitoring Components

| Component | Description |
|-----------|-------------|
| **Profile Metrics Table** | Summary statistics — counts, means, standard deviations, distributions per column. Used to identify missing values, outliers, and distribution changes. |
| **Drift Metrics Table** | Statistics on data drift over time — percentage of new/missing values, distribution changes. |

### Standard Deviation in Data Quality Monitoring

- Measures the **amount of variation or dispersion** in a set of values.
- **Example**: Mean = 100, Std Dev = 10 → values above 150 or below 50 are likely outliers.
- Higher standard deviation → more variance; lower std dev → more consistent data.
- Used in data quality to identify **outliers and anomalies**.

### Z-Score

> A statistical measure that quantifies **how many standard deviations** a data point is from the mean of a distribution.

### Other Important Concepts

| Concept | Description |
|---------|-------------|
| **Rolling Average** | Smooths short-term fluctuations to identify trends. Calculates the average of the last N data points. |
| **Data Drift** | Changes in data distribution over time. Can impact ML model performance — e.g., a model trained on balanced classes may produce biased predictions when input distribution becomes imbalanced. |

---

## Airflow Advanced Concepts

Apache Airflow is a powerful **workflow orchestration tool** for authoring, scheduling, and monitoring complex data pipelines. It is built in Python and known for its flexibility, scalability, and rich ecosystem of integrations.

### Five Main Components of Airflow

| Component | Description |
|-----------|-------------|
| **Webserver** | Provides the UI to view and manage workflows, monitor execution, and access logs. |
| **Scheduler** | Schedules and executes workflows based on defined DAGs and dependencies. |
| **Metadatabase** | Stores metadata about workflows, tasks, and execution history (typically PostgreSQL or MySQL). |
| **Executor** | Responsible for executing tasks. Types: `LocalExecutor`, `CeleryExecutor`, `KubernetesExecutor`. |
| **Workers** | Actually execute tasks — processes (LocalExecutor), distributed nodes (CeleryExecutor), or Kubernetes pods (KubernetesExecutor). |

### Executor Types

| Executor | Best For | Description |
|----------|----------|-------------|
| **LocalExecutor** | Small-medium workloads | Runs tasks in parallel on the same machine. Easy to set up. |
| **CeleryExecutor** | Large-scale workloads | Distributes tasks across multiple worker nodes using Celery. Better scalability and fault tolerance. |
| **KubernetesExecutor** | Cloud-native environments | Runs tasks in Kubernetes pods. Dynamic scaling, task isolation. Highest scalability. |

### MWAA (Managed Workflows for Apache Airflow)

- Fully managed AWS service for running Apache Airflow workflows.
- Automatic scaling, high availability, integration with other AWS services.
- **Backend**: Built on **Amazon EKS** (Kubernetes) + **Amazon RDS** (metadata database). Uses `KubernetesExecutor`.

### Key Airflow Concepts for Data Engineers

| # | Concept | Description |
|---|---------|-------------|
| 1 | **DAGs** | Directed Acyclic Graphs — core building blocks defining task structure and dependencies. |
| 2 | **Tasks** | Individual units of work in a DAG. |
| 3 | **XComs** | Cross-communication — pass small data payloads between tasks (`xcom_push` / `xcom_pull`). |
| 4 | **Sensors** | Wait for a condition (e.g., `S3KeySensor`, `ExternalTaskSensor`). |
| 5 | **TaskGroups** | Replace SubDAGs for better performance and maintainability. Group related tasks together. |
| 6 | **Dynamic DAGs** | Generate tasks from configuration at parse time (useful for variable numbers of tasks). |
| 7 | **Pools** | Concurrency control — limit the number of tasks that can run simultaneously for a shared resource. |
| 8 | **Operators** | Building blocks of tasks — `PythonOperator`, `BashOperator`, `EmailOperator`, `HttpOperator`, `SqlOperator`. |
| 9 | **Hooks** | Interfaces to external systems (databases, APIs). |
| 10 | **Branches** | Conditional execution based on criteria. |
| 11 | **SubDAGs** | Reusable components (deprecated — use **TaskGroups** instead). |

### Commonly Used Operators

| Operator | Use Case |
|----------|----------|
| `PythonOperator` | Execute a Python function. |
| `BashOperator` | Execute a bash command or script. |
| `EmailOperator` | Send emails (notifications, alerts). |
| `HttpOperator` | Make HTTP requests (APIs, web services). |
| `SqlOperator` | Execute SQL queries. |
| `S3KeySensor` | Wait for a specific file in S3. |
| `ExternalTaskSensor` | Wait for a task in another DAG to complete. |

### XComs in Detail

- **Purpose**: Pass small amounts of data between tasks (e.g., a file path generated by one task, consumed by another).
- **How it works**:
  - Task A pushes a value: `xcom_push(key='file_path', value='/data/output.parquet')`
  - Task B pulls the value: `xcom_pull(task_ids='task_a', key='file_path')`
- Data is stored in the Airflow metadata database.

### Pools for Concurrency Control

- Limit the number of tasks that can run simultaneously for a specific resource.
- **Example**: A database with a max of 5 connections. Create a pool of size 5.
- When a task is assigned to the pool, it runs only when a slot is available.
- **Real-world use case**: External API with rate limits — create a pool to limit concurrent API access tasks and avoid being blocked.

### TaskGroups vs. SubDAGs

| Feature | TaskGroups | SubDAGs |
|---------|------------|---------|
| Performance | Better | Worse |
| Maintainability | Easier | Harder |
| Status | **Recommended** | Deprecated |

---

## Data Storage Formats

### Parquet vs. ORC vs. Avro

| Feature | Parquet | ORC | Avro |
|---------|---------|-----|------|
| **Storage Type** | Columnar | Columnar | Row-based |
| **Best For** | Analytics (predicate pushdown, column pruning) | Hive workloads, better compression | Streaming & row-based processing |
| **Schema Evolution** | Supported | Supported | Strong support |
| **Disadvantages** | Slower writes; not ideal for streaming | Similar to Parquet | Larger file sizes; less efficient for analytics |

> All three support **Snappy** and **GZIP** compression.

### Parquet vs. ORC — Key Differences

| Aspect | Parquet | ORC |
|--------|---------|-----|
| **Adoption** | Widely supported (Spark, Hive, Impala) | Optimized for Hive |
| **Compression** | Efficient | Better compression for certain use cases |
| **Features** | Schema evolution, predicate pushdown | Predicate pushdown, column pruning |

### What Is Hive?

- A data warehousing and SQL-like query language built on the **Hadoop** ecosystem.
- Uses **HiveQL** (SQL-like syntax) to query/manage large datasets in HDFS.
- Allows users to perform analysis without writing complex MapReduce code.
- Features: schema management, partitioning, indexing.

### Amazon Athena

- **Serverless** interactive query service — analyze data in S3 using **standard SQL**.
- Built on **Presto** — a distributed SQL query engine.
- **Pricing**: Pay per byte scanned → **partition pruning is critical** for cost savings.

### Presto vs. Hive

| Aspect | Presto | Hive |
|--------|-------|------|
| **Optimized For** | Interactive querying, low-latency | Batch processing, high-throughput |
| **Use Case** | Ad-hoc analysis, reporting | ETL, data warehousing |
| **Execution Engine** | Distributed architecture (fast) | MapReduce / Tez (slower) |
| **Data Sources** | S3, HDFS, relational databases, etc. | Primarily HDFS |

> **Simple summary**: Presto = fast, interactive queries. Hive = batch-oriented, high-throughput ETL.

---

## AWS EMR Deep Dive

### What Is EMR?

**Amazon EMR** (Elastic MapReduce) is a cloud-based big data processing service that allows you to process and analyze large datasets using frameworks like Apache Spark, Hadoop, and Hive.

**How it solves big data processing:**
- Managed environment — no need to set up infrastructure.
- **Auto-scaling** — clusters adjust size based on workload.
- Integrates with S3, IAM, and other AWS services.

### EMR Cluster Components

| Component | Description |
|-----------|-------------|
| **Master Node** | Primary node — manages the cluster, schedules tasks, coordinates execution. |
| **Core Nodes** | Worker nodes — run processing frameworks (Spark, Hadoop) and store data in HDFS. |
| **Task Nodes** | Optional nodes — handle additional processing, no HDFS storage. Ideal for spot instances. |

### Cluster Modes

| Mode | Description |
|------|-------------|
| **Cluster Mode** | Cluster runs continuously until manually terminated. Suitable for long-running workloads. |
| **Step Mode** | Submit individual steps to an existing cluster without managing lifecycle. Suitable for ad-hoc tasks. |

### Cluster Types (Instance Purchasing Options)

| Type | Description | Use Case |
|------|-------------|----------|
| **On-Demand** | Billed hourly, start/stop as needed. | Variable or unpredictable workloads. |
| **Spot** | Uses spare EC2 capacity — **60–70% cost savings**. Can be interrupted (2-minute warning). | Fault-tolerant, batch processing workloads. |

### EMRFS for S3 Consistency

- **EMRFS** (EMR File System) provides a **consistent view** of data in S3.
- Addresses S3's **eventual consistency** model.
- Uses a metadata store to track file state.

### EMR Serverless

- Run big data workloads **without managing infrastructure**.
- **Automatic scaling** — resources adjust based on workload.
- Supports both **on-demand** and **spot** clusters.

### Spot Instances — Best Practices

- Use spot instances for **task nodes** (not core nodes) to save 60–70%.
- Handle interruptions with:
  - **Checkpointing** tasks.
  - Mixing on-demand (for critical tasks) + spot instances.
  - Designing fault-tolerant workloads.

---

## AWS Athena & Glue

### Athena

- **Serverless SQL** on S3, built on **Presto**.
- Pay per byte scanned — **partition pruning is critical** for cost and performance.

### Glue Catalog

- **Central metastore** for storing metadata — table definitions, schemas, partitions.
- Queries via Athena internally look up the **Glue Catalog** for table metadata.

| Feature | Description |
|---------|-------------|
| **Glue Crawlers** | Auto-discover schema from data in S3. Scan data, infer schema, create/update tables in the Catalog. |
| **CTAS** | Create Table As Select — transform or aggregate data into a new table. |
| **Partition Projection** | Define partitioning scheme without running a crawler. Skips the crawler for time-partitioned data. |

### Can a Glue Crawler Discover Schema from a Spark Job?

> **Yes**. If a Spark job writes data to S3 without a schema definition, the Glue Crawler can scan the data location, infer the schema, and update the Glue Data Catalog accordingly for querying via Athena.

### Putting It All Together

```
PySpark on EMR  ──►  S3 (Parquet/ORC)
                          │
                    Glue Crawler
                          │
                    Glue Data Catalog
                          │
                    Athena (Presto)
                          │
                   Analytics / Reporting
```

**Is Glue necessary?** While not strictly required, Glue plays a crucial role:

1. **Glue Catalog** serves as a central metadata repository.
2. **Glue Crawlers** automatically discover and update schema after Spark jobs write to S3.
3. **Athena** uses Glue Catalog metadata to efficiently query data in S3.
4. Glue can also perform **ETL** transformations before storing data in S3.
