## Why large executors are not always good

Large executors increase:

* GC pause times
* memory contention
* risk of losing large amounts of work if executor fails

Also, too many cores per executor reduce parallel efficiency because tasks compete for the same JVM heap.

Typical sweet spot:

* 4–5 cores/executor instead of 16+.

---

## GC pressure in Apache Spark

GC pressure happens when JVM spends excessive time cleaning unused objects.

Causes:

* huge shuffles
* large joins
* excessive caching
* skewed partitions

Symptoms:

* high GC time
* low CPU utilization
* executor slowdown/OOM.

---

## Star vs Snowflake Schema

| Star                    | Snowflake                 |
| ----------------------- | ------------------------- |
| Denormalized dimensions | Normalized dimensions     |
| Faster queries          | Less redundancy           |
| Simpler joins           | More joins                |
| Better for analytics    | Better storage efficiency |

Star is preferred in OLAP because query performance matters more than storage savings.

---

## Spill-to-disk behavior

When Spark execution memory is insufficient during shuffle/sort/join:

* intermediate data spills from memory to disk.

Why bad:

* disk IO is much slower than RAM
* increases stage runtime heavily.

Usually caused by:

* skew
* large partitions
* insufficient memory.

---

## Surrogate vs Natural Keys

| Surrogate Key    | Natural Key         |
| ---------------- | ------------------- |
| System-generated | Business-generated  |
| Stable           | Can change          |
| Integer usually  | Real-world value    |
| Better joins     | Business meaningful |

Example:

* surrogate: customer_sk = 101
* natural: email_id

Warehouses prefer surrogate keys for SCD handling and performance.

---

## Data Marts

A data mart is a subject-specific subset of a warehouse.

Examples:

* finance mart
* marketing mart
* sales mart

Purpose:

* faster access
* domain-focused analytics
* reduced query complexity.

---

## CDC Handling (Change Data Capture)

CDC captures inserts/updates/deletes incrementally instead of full reloads.

Common methods:

* database logs
* timestamps
* Debezium/Kafka

Challenges:

* ordering
* duplicate events
* schema evolution
* exactly-once guarantees.

---

## Late Arriving Data

Data that arrives after expected processing window.

Example:

* yesterday’s events arriving today.

Handling:

* watermarking
* reprocessing windows
* upserts/merge operations
* partition overwrite strategies.

---

## Scheduler vs Executor in Apache Airflow

| Scheduler               | Executor                 |
| ----------------------- | ------------------------ |
| Decides task scheduling | Runs tasks               |
| Parses DAGs             | Executes workloads       |
| Tracks dependencies     | Handles actual execution |

Scheduler = orchestration brain.
Executor = task execution engine.

---

## Airflow Catchup vs Backfill

| Catchup                           | Backfill                |
| --------------------------------- | ----------------------- |
| Automatic historical run creation | Manual rerun            |
| Happens if DAG missed schedules   | Explicit user-triggered |
| Controlled by catchup=True        | CLI/UI initiated        |

---

## Why S3 is not a true filesystem

Amazon Web Services S3 is object storage, not block storage.

Differences:

* no true directory hierarchy
* objects instead of files
* rename = copy + delete
* high metadata/listing latency
* eventual consistency historically

This affects Spark performance and commit semantics.

---

## How Athena works internally

Amazon Athena uses:

* Presto/Trino query engine
* reads directly from S3
* schema from Glue Catalog
* distributed SQL execution

Why Parquet helps:

* columnar reads
* compression
* predicate pushdown

Athena charges per data scanned.

---

## Optimal Chunk Size Tradeoff in RAG

| Small Chunks               | Large Chunks                       |
| -------------------------- | ---------------------------------- |
| Better retrieval precision | Better context continuity          |
| May lose semantic context  | More token cost                    |
| More embeddings/storage    | Lower retrieval accuracy sometimes |

Typical production range:

* 300–1000 tokens.

No universal best size.

---

## Dense vs Sparse Retrieval

| Dense Retrieval               | Sparse Retrieval              |
| ----------------------------- | ----------------------------- |
| Embedding vectors             | Keyword matching              |
| Semantic similarity           | Exact token matching          |
| Uses transformers             | Uses BM25/TF-IDF              |
| Better semantic understanding | Better exact phrase retrieval |

Modern RAG often uses hybrid retrieval.

---

## ANN Search (Approximate Nearest Neighbor)

Used in vector DBs to avoid brute-force similarity search.

Instead of comparing against every vector:

* uses indexing structures like HNSW/IVF.

Tradeoff:

* slightly lower accuracy
* massively lower latency.

Essential for large-scale vector search.

---

## How do you productionize an LLM app?

Key components:

* prompt management
* retrieval pipeline
* caching
* observability
* evaluation framework
* guardrails
* rate limiting
* retries/fallbacks
* monitoring hallucinations
* cost optimization

Production systems are mostly infrastructure + reliability engineering, not prompting.

---

## How do you evaluate LLM quality?

Three layers:

### 1. Offline evaluation

* benchmark datasets
* precision/recall
* groundedness
* hallucination rate

### 2. Human evaluation

* relevance
* factual correctness
* coherence

### 3. Online metrics

* user satisfaction
* latency
* CTR
* conversation success rate

Evaluation is harder than model building.

---

## Users complain responses are inconsistent. What do you do?

I’d investigate in this order:

1. Retrieval quality

* inconsistent chunks retrieved

2. Prompt variability

* non-deterministic prompting

3. Temperature too high

* excessive randomness

4. Context overflow

* important info truncated

5. Hallucinations

* weak grounding

Concrete fixes:

* reduce temperature
* improve retrieval/reranking
* structured prompts
* output schema validation
* evaluation datasets
* prompt versioning
* response caching
* deterministic workflows where possible

Most “LLM inconsistency” problems are actually retrieval and context engineering failures, not model failures.
