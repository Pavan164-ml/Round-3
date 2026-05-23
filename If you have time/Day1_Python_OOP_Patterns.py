"""
DAY 1 — PYTHON OOP, GENERATORS, DECORATORS, ASYNC
Interview: 26 May 2026 | Data Engineering + AI

Topics: Classes, Inheritance, Dunders, Dataclasses, ABC,
        Generators, Decorators, Context Managers, Async, Error Handling
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
import time
import asyncio
import logging
from typing import Dict, List, Optional, Any

# =============================================================================
# PART 1: DATACLASSES — Clean config/data objects
# =============================================================================

@dataclass
class PipelineConfig:
    """Configuration for a data pipeline step.
    
    Using dataclass gives us __init__, __repr__, __eq__ for free.
    """
    name: str
    source_path: str
    target_path: str
    partitions: List[str] = field(default_factory=lambda: ["date"])
    write_mode: str = "overwrite"
    
    def __post_init__(self):
        """Validate after initialization."""
        valid_modes = {"overwrite", "append", "ignore", "error"}
        if self.write_mode not in valid_modes:
            raise ValueError(f"Invalid write_mode: {self.write_mode}. Must be one of {valid_modes}")

# Usage
config = PipelineConfig(
    name="daily_orders",
    source_path="s3://raw/orders/",
    target_path="s3://gold/orders/"
)
print(f"Config: {config}")


# =============================================================================
# PART 2: ABSTRACT BASE CLASS — Pipeline Interface
# =============================================================================

class BasePipeline(ABC):
    """Abstract base class that all pipelines must implement.
    
    This enforces a consistent interface across all pipeline types.
    """
    
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def extract(self) -> Any:
        """Extract data from source."""
        pass
    
    @abstractmethod
    def transform(self, data: Any) -> Any:
        """Transform the data."""
        pass
    
    @abstractmethod
    def load(self, data: Any) -> None:
        """Load data to target."""
        pass
    
    def run(self) -> None:
        """Template method defining the pipeline execution order."""
        self.logger.info(f"Starting pipeline: {self.config.name}")
        data = self.extract()
        transformed = self.transform(data)
        self.load(transformed)
        self.logger.info(f"Pipeline complete: {self.config.name}")


class OrdersPipeline(BasePipeline):
    """Concrete implementation for orders pipeline."""
    
    def extract(self) -> List[Dict]:
        self.logger.info("Extracting orders from S3...")
        # Simulate extraction
        return [{"order_id": 1, "amount": 100.0}]
    
    def transform(self, data: List[Dict]) -> List[Dict]:
        self.logger.info("Transforming orders...")
        return [{"order_id": d["order_id"], "amount_usd": d["amount"] * 1.1} for d in data]
    
    def load(self, data: List[Dict]) -> None:
        self.logger.info(f"Loading {len(data)} records to Delta...")


# =============================================================================
# PART 3: MRO (Method Resolution Order) — Know for interviews
# =============================================================================

class A:
    def process(self):
        return "A"

class B(A):
    def process(self):
        return f"B -> {super().process()}"

class C(A):
    def process(self):
        return f"C -> {super().process()}"

class D(B, C):
    def process(self):
        return f"D -> {super().process()}"

# MRO: D -> B -> C -> A
print(f"\nMRO: {[cls.__name__ for cls in D.__mro__]}")
print(f"Result: {D().process()}")  # D -> B -> C -> A


# =============================================================================
# PART 4: GENERATORS — Memory-efficient streaming
# =============================================================================

def read_large_file_in_batches(file_path: str, batch_size: int = 1000):
    """Generator that yields batches of lines from a large file.
    
    Instead of loading entire file into memory, yields batches on demand.
    """
    import csv
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        batch = []
        for row in reader:
            batch.append(row)
            if len(batch) >= batch_size:
                yield batch
                batch = []
        if batch:  # Don't forget the last partial batch
            yield batch

# Interview trick: Generator expression vs list comprehension
nums = range(1_000_000)
# This uses O(1) memory:
sum_of_squares = sum(x**2 for x in nums)
# This uses O(n) memory and will OOM:
# sum_of_squares = sum([x**2 for x in nums])  # DON'T DO THIS!


# =============================================================================
# PART 5: DECORATORS — Pipeline timing & retry
# =============================================================================

def timer(func):
    """Decorator that logs execution time of any function."""
    @wraps(func)  # Preserves function metadata (name, docstring)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIMER] {func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator with parameters — retry on failure with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    print(f"[RETRY] {func.__name__} failed (attempt {attempt}/{max_attempts}): {e}")
                    time.sleep(delay * (2 ** (attempt - 1)))  # Exponential backoff
            return None
        return wrapper
    return decorator

@timer
@retry(max_attempts=3)
def fetch_data_from_api(url: str) -> Dict:
    """Simulate an API call that may fail."""
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise ConnectionError("Simulated network timeout")
    return {"status": "ok", "data": [1, 2, 3]}

# Stacked decorators execute bottom-up: retry wraps fetch, then timer wraps retry
print(f"\nResult: {fetch_data_from_api('https://api.example.com/data')}")


# =============================================================================
# PART 6: CONTEXT MANAGERS — DB connections, file handles
# =============================================================================

class SparkSessionContext:
    """Context manager for Spark sessions — ensures cleanup."""
    
    def __init__(self, app_name: str):
        self.app_name = app_name
        self.spark = None
    
    def __enter__(self):
        # from pyspark.sql import SparkSession
        # self.spark = SparkSession.builder.appName(self.app_name).getOrCreate()
        print(f"[CONTEXT] Opening Spark session: {self.app_name}")
        self.spark = {"session": "spark_mock", "name": self.app_name}
        return self.spark
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"[CONTEXT] Closing Spark session: {self.app_name}")
        # self.spark.stop()
        if exc_type:
            print(f"[CONTEXT] Exception occurred: {exc_val}")
        return False  # Don't suppress exceptions

# Usage
with SparkSessionContext("my_pipeline") as spark:
    print(f"  Working with: {spark}")
    # raise ValueError("Something went wrong")  # Exception handled by exit

# Simpler version using contextlib
from contextlib import contextmanager

@contextmanager
def db_connection(connection_string: str):
    """Context manager using contextlib — simpler syntax."""
    print(f"[DB] Connecting to: {connection_string[:30]}...")
    conn = {"connected": True, "conn_str": connection_string}
    try:
        yield conn  # This is what the 'with' block receives
    finally:
        print("[DB] Closing connection")
        conn["connected"] = False


# =============================================================================
# PART 7: ASYNC PYTHON — I/O bound concurrency
# =============================================================================

async def fetch_order(order_id: int) -> Dict:
    """Simulate an async API call to fetch order details."""
    await asyncio.sleep(0.5)  # Simulate network latency
    return {"order_id": order_id, "status": "delivered", "amount": 100.0}

async def send_notification(user_email: str, message: str) -> None:
    """Simulate async notification sending."""
    await asyncio.sleep(0.3)
    print(f"[NOTIFY] Sent to {user_email}: {message[:30]}...")

async def process_orders_concurrently(order_ids: List[int]):
    """Process multiple orders in parallel using asyncio.gather.
    
    10 orders × 0.5s each = 5s sequential → 0.5s with gather!
    """
    print(f"Processing {len(order_ids)} orders concurrently...")
    
    # Run all fetches in parallel
    orders = await asyncio.gather(*[fetch_order(oid) for oid in order_ids])
    
    # Send all notifications in parallel
    notif_tasks = [
        send_notification(f"user{oid}@example.com", f"Order {oid} processed")
        for oid in order_ids
    ]
    await asyncio.gather(*notif_tasks)
    
    return orders

# Run async function
async def main():
    start = time.perf_counter()
    result = await process_orders_concurrently([101, 102, 103, 104, 105])
    elapsed = time.perf_counter() - start
    print(f"Processed {len(result)} orders in {elapsed:.2f}s (vs ~{len(result)*0.8}s sequential)")


# =============================================================================
# PART 8: ERROR HANDLING — Structured logging
# =============================================================================

# Custom exception hierarchy
class PipelineError(Exception):
    """Base exception for all pipeline errors."""
    def __init__(self, message: str, error_code: str = "PIPELINE_ERROR"):
        self.error_code = error_code
        super().__init__(message)

class PipelineValidationError(PipelineError):
    """Data validation failure."""
    def __init__(self, message: str, table: str):
        self.table = table
        super().__init__(message, error_code="VALIDATION_ERROR")

class PipelineConnectionError(PipelineError):
    """External connection failure."""
    def __init__(self, message: str, service: str):
        self.service = service
        super().__init__(message, error_code="CONNECTION_ERROR")

def structured_error_handler():
    """Demonstrate proper error handling pattern."""
    
    logging.basicConfig(
        level=logging.INFO,
        format='{"time": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
    )
    logger = logging.getLogger("PipelineExecutor")
    
    try:
        # Simulate pipeline step
        logger.info("Starting transform step")
        
        # Validate
        if True:  # Some validation fails
            raise PipelineValidationError(
                "Null values found in customer_id column",
                table="silver.orders"
            )
        
    except PipelineValidationError as e:
        logger.error(f"Validation failed on {e.table}: {e} (code={e.error_code})")
        # Re-raise if fatal
        raise
    except PipelineConnectionError as e:
        logger.error(f"Connection failed to {e.service}: {e}")
        # Retry logic here
    except PipelineError as e:
        logger.error(f"Pipeline error: {e} (code={e.error_code})")
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
    finally:
        logger.info("Cleanup: closing connections")
    print()


# =============================================================================
# SUMMARY: Interview Talking Points
# =============================================================================
"""
KEY INTERVIEW POINTS FOR PYTHON:

1. OOP:
   - dataclasses give you __init__, __repr__, __eq__ for free
   - ABCs enforce interface contracts via abstractmethod
   - MRO (Method Resolution Order) follows C3 linearization: D → B → C → A
   - super() delegates to next class in MRO

2. Generators:
   - Use yield for memory-efficient iteration over large datasets
   - Generator expressions (x**2 for x in range(1M)) use O(1) memory
   - List comprehensions [x**2 for x in range(1M)] use O(n) memory

3. Decorators:
   - @wraps(func) preserves __name__, __doc__ of decorated function
   - Stacked decorators execute bottom-to-top (closest to function first)
   - Parametric decorators: def retry(max_attempts=3): → def decorator(func): → def wrapper(...)

4. Context Managers:
   - Class-based: __enter__/__exit__ for resource management
   - contextlib.contextmanager for simpler generator-based approach
   - __exit__ receives exc_type, exc_val, exc_tb; return True to suppress

5. Async:
   - Use asyncio.gather for concurrent I/O bound tasks
   - Async is NOT for CPU-bound work (use multiprocessing)
   - Three I/O parallelism options: async (single thread), threading (GIL-limited), multiprocessing (true parallel)

6. Error Handling:
   - Custom exception hierarchy inheriting from Exception
   - try/except/finally for predictable cleanup
   - never use bare except: (catches SystemExit, KeyboardInterrupt too!)
"""

if __name__ == "__main__":
    # Run async main
    asyncio.run(main())