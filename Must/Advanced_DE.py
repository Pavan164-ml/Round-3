I have an advanced Data Engineer interview coming up, and I want to prepare by reviewing key concepts related to Apache Spark.
For all the topics listed below, please provide a concise explanation of each concept that I can quickly review before my interview.

Apache Spark	
Spark Execution Model	

- Driver: coordinates execution, maintains metadata, and handles job scheduling. Runs the main program and creates SparkContext.
- Executors: run tasks and store data.
- Tasks: units of work sent to executors.
- Stages: sets of tasks that can be executed in parallel.
- DAG: Directed Acyclic Graph representing the execution plan.
- Lazy evaluation: transformations build a plan but are not executed immediately.
- Actions: trigger execution of the plan.
- Catalyst optimizer: rewrites logical plan for optimization.
- Tungsten: optimizes memory and CPU usage for better performance.

Debugging a slow EMR job: check DAG in Spark UI to find the stage causing shuffle spill, not just the final action.
    - Use Spark UI to identify stages with shuffle spill and optimize those stages to improve performance.
    - Consider optimizing data partitioning, reducing data shuffling, and tuning Spark configurations to mitigate shuffle spill issues.


Hash / range / custom partitioning. Partition pruning. Skew: one executor processes 80% of data. Fix: salting (add random prefix to key), repartition(), coalesce(). AQE skew join hint.
- Hash partitioning: distributes data based on the hash of the key.
    - Custom partitioning: allows users to define their own partitioning logic. For example, customer_id can be partitioned by hashing the customer_id or by using a custom function that assigns partitions based on specific criteria.
    - This partiton makes sure that the data is distributed evenly across partitions, which can help improve performance and reduce data skew.
    - The problem with hash partitioning is that it does not work well with range queries, as it does not preserve the order of the data. This can lead to inefficient queries and increased latency.
- Range partitioning: distributes data based on a range of key values. 
    - This type of partitioning is useful for range queries, as it preserves the order of the data. For example, if you have a timestamp column, you can partition the data by date ranges (e.g., daily, monthly) to optimize queries that filter by date.
    - However, range partitioning can lead to data skew if the data is not evenly distributed across the ranges. For example, if most of the data falls into a few ranges, it can lead to some partitions being much larger than others, which can cause performance issues.
- Custom partitioning: allows users to define their own partitioning logic. For example, you can create a custom partitioner that assigns partitions based on specific criteria, such as geographic location or customer segment. This can help improve performance by ensuring that related data is stored together and reducing data shuffling.

Partition pruning: 
    - It is a technique that allows Spark to skip reading unnecessary partitions when executing a query.
    - This can significantly improve query performance by reducing the amount of data that needs to be processed.
    - For example, if you have a table partitioned by date and your query filters for a specific date range, Spark can prune the partitions that do not fall within that range, resulting in faster query execution.

Skew: 
    - Data skew occurs when one or more partitions contain significantly more data than others, leading to uneven workload distribution and performance degradation.
    - For example, if one executor is processing 80% of the data while others are idle, it can lead to long execution times and resource inefficiency.
    - Fixes for data skew include 
        - Salting (adding a random prefix to the key)
        - Repartitioning (internally repartitioning works by redistributing data across partitions making sure the data is evenly distributed)
        - Coalescing - This is a technique that reduces the number of partitions in a DataFrame. It is often used to optimize performance by reducing the overhead of managing too many small partitions. Coalescing can help mitigate data skew by combining smaller partitions into larger ones, which can lead to more balanced workloads across executors. 
        - Enabling Adaptive Query Execution (AQE) skew join hints.
            - AQE is a query optimization technique in Spark that allows the query execution plan to be dynamically adjusted based on runtime statistics.
            - For skewed joins, AQE can automatically detect skewed keys and apply optimizations such as splitting the skewed key into multiple partitions or using a different join strategy to improve performance. 
            - This helps mitigate the impact of data skew on join operations and can lead to faster query execution.
            - Alternatively, AQE also allows you to provide skew join hints, which can help Spark optimize the join operation by providing information about the skewed keys. This can further improve performance by allowing Spark to make informed decisions about how to handle the skewed data during the join process.
            - Following are the list of optimizations that AQE can apply overall for better performance:
                - Dynamically coalescing shuffle partitions based on the size of the data.
                - Dynamically optimizing skewed joins by splitting skewed keys into multiple partitions or using a different join strategy.
                - Dynamically optimizing join strategies based on runtime statistics, such as switching from a sort-merge join to a broadcast join when appropriate.
                - Dynamically optimizing aggregate operations by adjusting the number of reducers based on the size of the data.


Spark Shuffle & Performance Tuning:

Shuffle triggered by: groupBy, join, repartition. 
    - GroupBy: when you perform a groupBy operation, Spark needs to shuffle the data to group the records based on the specified key. This involves redistributing the data across the cluster, which can lead to performance issues if not optimized properly.
        - This can be optimized by using techniques such as reducing the number of shuffle partitions
        - Using combiners (combiners are basically functions that combine multiple values into a single value) to reduce the amount of data shuffled, and ensuring that the data is properly partitioned before the groupBy operation to minimize shuffling.
    - Join: when you perform a join operation, Spark may need to shuffle the data to align the keys from both datasets. This can be particularly expensive if the datasets are large or if there is data skew.
        - By default, Spark uses a sort-merge join for large datasets, which can lead to significant shuffling. The reason for using SMJ is that it is efficient for large datasets and can handle data that does not fit in memory. However, it can lead to performance issues due to the shuffle.
        - However, if one of the datasets is small enough to fit in memory, Spark can use a broadcast join, which avoids shuffling by broadcasting the smaller dataset to all executors. This can significantly improve performance for certain join operations.
        - Apart from the default join strategies, Spark also provides other join types such as shuffle hash join (SHJ works by partitioning the data based on the join key and then performing a hash join within each partition) and broadcast hash join (BHJ works by broadcasting the smaller dataset to all partitions of the larger dataset and then performing a hash join), which can be used to optimize performance based on the size of the datasets and the presence of data skew.
    - Repartition: explicitly repartitioning a DataFrame triggers a shuffle to redistribute the data across the specified number of partitions.
        - This option is chosen when you want to increase the number of partitions to improve parallelism or when you want to change the partitioning scheme (e.g., from hash partitioning to range partitioning).
        - However, it can lead to performance issues if not used judiciously, as it involves shuffling all the data across the cluster.

Tune: spark.sql.shuffle.partitions (default 200, set to 2-3x the number of cores)
    - The above configuration controls the number of partitions used for shuffle operations. 
    - By default, it is set to 200, which may not be optimal for all workloads.
    - Setting it to 2-3 times the number of cores in your cluster can help improve performance by allowing for better parallelism during shuffle operations. 
    - However, the optimal value can vary based on the specific workload and cluster configuration, so it may require some experimentation to find the best setting for your use case.

AQE (adaptive.enabled=true)
    - By default in spark 3.0 and above, AQE is enabled, which allows Spark to dynamically optimize query execution plans based on runtime statistics.
    - The major difference between AQE and Catalyst optimizer is that AQE can make adjustments to the execution plan during runtime based on the actual data characteristics, while the Catalyst optimizer performs static optimizations based on the logical plan before execution.
    - So AQE can optimize for scenarios such as skewed joins, dynamically coalescing shuffle partitions, and optimizing join strategies based on runtime statistics, which can lead to improved performance for certain workloads.

Kryo serialization
    - Serialization is the process of converting data into a byte format that can be easily transmitted over the network or stored on disk. 
    - In Spark, serialization is used during shuffle operations to transfer data between executors.
    - Kryo serialization is a more efficient serialization format compared to the default Java serialization, which can help improve performance by reducing the amount of data transferred during shuffles.
    - Without proper serialization, Spark jobs can suffer from high memory usage and slow performance due to the overhead of converting data to and from a less efficient format.

Why do spark require JVM to be run on and how does it impact performance?
    - Spark is built on top of the Java Virtual Machine (JVM) because it was originally developed in Scala, which runs on the JVM.
    - The JVM provides a platform-independent environment for running Spark applications, allowing them to run on various operating systems and hardware configurations without modification.
    - However, running on the JVM can impact performance due to factors such as garbage collection, memory management, and the overhead of the JVM itself.
    - For example, garbage collection can lead to pauses in the execution of a Spark application, which can impact performance, especially for long-running jobs or jobs with large memory requirements. Additionally, the JVM's memory management can lead to issues such as OutOfMemory errors if not properly configured, which can also impact performance. 
    - Overall, while the JVM provides benefits in terms of portability and ease of development, it can also introduce performance challenges that need to be addressed through proper configuration and optimization techniques.

What is garbage collection and why do we do it in spark?
    - Garbage collection is the process of automatically freeing up memory that is no longer being used by the application.
    - In Spark, garbage collection is important because it helps manage memory usage and prevent OutOfMemory errors.
    - Spark applications can consume a large amount of memory, especially when processing large datasets or performing complex operations. 
    - If memory is not properly managed, it can lead to performance issues and application failures.
    - By performing garbage collection, Spark can free up memory that is no longer needed, allowing the application to continue running smoothly and efficiently.

Spark Join Types

What is a hash join and when is it used?
    - A hash join is a type of join operation that uses a hash function to partition the data based on the join key.
    - It is typically used when one of the tables is small enough to fit in memory, allowing for a more efficient join operation.
    - The hash join works by creating a hash table for the smaller table and then probing the hash table with the larger table to find matching rows.
    - This can be more efficient than a sort-merge join for certain workloads, especially when there is data skew or when the join keys are not sorted.
    - Internally hashing is a technique where given a key, a hash function is applied to it to generate a hash value. This hash value is then used to determine the partition or bucket where the data associated with that key will be stored. This allows for efficient data retrieval and join operations, as the hash function can quickly determine the location of the data based on the join key.
        - This is applied to both smaller table and larger table in a hash join. The smaller table is hashed to create a hash table, and the larger table is hashed to determine which partition or bucket to probe in the hash table for matching rows.

Broadcast Hash Join (small table fits in memory, no shuffle). 
    - This join type is used when one of the tables is small enough to fit in memory.
    - Spark broadcasts the smaller table to all executors, allowing for a hash join to be performed without shuffling the larger table.

Is there any difference between Broadcast Hash Join and Broadcast Nested Loop Join?
    - Yes, there is a difference between Broadcast Hash Join and Broadcast Nested Loop Join. 
    - Broadcast Hash Join is more efficient when the smaller table can fit in memory, as it allows for a hash join to be performed without shuffling the larger table. 
    - On the other hand, Broadcast Nested Loop Join is used when the smaller table cannot fit in memory, and it performs a nested loop join by iterating over each row of the larger table and comparing it with each row of the smaller table. 
    - This can be less efficient than a hash join, especially for larger datasets.


Sort-Merge Join (both sides sorted + shuffled, default for large-large). 
    - This join type is used when both tables are large and need to be shuffled to align the keys.
    - Spark sorts both tables by the join key and then performs a merge operation to combine the matching rows.
    - This can be efficient for large datasets, but it can lead to performance issues due to the shuffle and sort operations involved.


Shuffle Hash Join. Use /*+ BROADCAST(t) */ hint or autoBroadcastJoinThreshold.	
    - This join type is used when one of the tables is small enough to fit in memory, but the other table is too large to be broadcasted.
    - Spark partitions the larger table based on the join key and then performs a hash join within each partition.
    - This can be more efficient than a sort-merge join for certain workloads, especially when there is data skew.

Two large tables joining on user_id: SMJ used by default. 
    - When two large tables are joined on a common key such as user_id, Spark will typically use a Sort-Merge Join (SMJ) by default.

Add salting when user_id is skewed (power users).
    - If the user_id is skewed, meaning that a small number of user_ids are responsible for a large portion of the data (e.g., power users), it can lead to performance issues during the join operation.
    - To mitigate this, you can add salting to the user_id by adding a random prefix to the key. This helps distribute the data more evenly across partitions and reduces the impact of skew on the join performance.
    - For example, you can create a new column called salted_user_id by concatenating a random prefix with the original user_id, and then use this salted_user_id for the join operation instead of the original user_id. This can help improve performance by ensuring that the data is more evenly distributed across partitions during the join.


Streaiming
- Streaming is a continuous flow of data, while batch processing is a finite set of data. 
- Streaming allows for real-time processing and analysis of data as it arrives, while batch processing is typically used for processing large volumes of data at rest.

In a general streaming application, following are the key components:
- Source: This is where the streaming data originates from. It can be a variety of sources such as Kafka, Kinesis, or a file system.
- Stream processing engine: This is the component that processes the streaming data. It can be a framework like Apache Spark Structured Streaming, Apache Flink, or Apache Storm. 
    - The stream processing engine is responsible for performing transformations, aggregations, and other operations on the streaming data in real-time.
- Sink: This is where the processed streaming data is written to. It can be a variety of sinks such as a database, a file system, or another messaging system.
- Sharding and partitioning: In a streaming application, it is important to consider how the data will be partitioned and distributed across the processing nodes.
    - This can help improve performance and scalability by allowing for parallel processing of the streaming data.
    - Sharding refers to the process of dividing the streaming data into smaller chunks (shards) that can be processed independently. This can help improve performance by allowing for parallel processing of the data across multiple nodes.
        - For example, if you are processing streaming data from Kafka, you can shard the data based on the Kafka partition, allowing each shard to be processed by a different node in the cluster.
    - Partitioning refers to the process of dividing the streaming data into partitions based on a specific key or criteria. This can help improve performance by ensuring that related data is stored together and can be processed more efficiently.


Following are the important concepts related to streaming:
- Micro-batch processing: Spark Structured Streaming processes data in small batches, allowing for near real-time processing while still providing fault tolerance and scalability.
- Continuous processing: Spark Structured Streaming also supports continuous processing, which allows for even lower latency by processing data as it arrives without the need for micro-batches. This can be useful for applications that require real-time processing with minimal delay.
- Watermarking: This is a technique used to handle late data in streaming applications. By specifying a watermark, you can define how long to wait for late data before considering it as late and discarding it. 
    - For example, using .withWatermark('ts', '10 minutes') allows you to specify that any data arriving more than 10 minutes after the event time should be considered late and not included in the results.
- Triggers: Spark Structured Streaming provides different trigger options to control when the streaming query should be executed.
    - processingTime: triggers the query at regular intervals (e.g., every 10 seconds).
    - once: triggers the query to run only once and then stops.
    - availableNow: triggers the query to process all available data and then stops.
- Checkpointing: This is a mechanism for fault tolerance in streaming applications. By enabling checkpointing, Spark can save the state of the streaming query at regular intervals, allowing it to recover from failures and continue processing from where it left off.   


Spark Structured Streaming
- The problem that Spark Structured Streaming solves is the need for a unified API that can handle both batch and streaming data processing.
- Structured Streaming provides a high-level API for processing streaming data in a way that is consistent with batch processing, allowing developers to write code that can handle both types of workloads without needing to learn different APIs or frameworks.

- Structured Streaming allows you to process streaming data using the same APIs as batch processing, making it easier to build and maintain streaming applications.
    - This is possible because Structured Streaming treats streaming data as an unbounded table that is continuously updated as new data arrives.
    - This allows you to use familiar DataFrame and Dataset APIs to perform transformations and actions on streaming data, just as you would with batch data.

Micro-batch (default) vs continuous. Watermarking: handle late data — .withWatermark('ts', '10 minutes'). Triggers: processingTime, once, availableNow. Checkpointing for fault tolerance. Stateful ops: mapGroupsWithState.    

Spark Memory Management	

Explain the important components of an EMR.
    - EMR is a fully managed service that allows you to run Spark jobs on a cluster of machines.
    - The main components of an EMR cluster are:
        - Master node: This is the node that manages the cluster and coordinates the work of the worker nodes.
        - Worker nodes: These are the nodes that run the Spark jobs.
        - Job tracker: This is the component that tracks the progress of the Spark jobs and manages the resources allocated to the jobs.
        - Task tracker: This is the component that tracks the progress of the tasks within a job and manages the resources allocated to the tasks.
        - Hadoop Distributed File System (HDFS): This is the distributed file system that is used to store the data for the Spark jobs.
            - We use HDFS because it is a distributed file system that is designed to handle large amounts of data and is scalable and fault-tolerant.
            - S3 on the other hand is a object storage service that is not designed to handle large amounts of data and is not scalable and fault-tolerant.
        - YARN: This is the resource manager that is used to manage the resources allocated to the Spark jobs.


How does Spark categorize storage?
    - Spark categorizes storage into two main types: on-heap and off-heap memory.
    - On-heap memory is the memory that is managed by the Java Virtual Machine (JVM) 
        - It is used for storing objects and data structures that are created during the execution of a Spark application. 
        - This includes things like RDDs, DataFrames, and other intermediate data structures.
    - Off-heap memory, on the other hand, is memory that is allocated outside of the JVM heap. 
        - It is used for storing data that is not managed by the JVM, such as serialized data or data that is used for shuffle operations.
    
    Both these types of memory are part of the RAM and are important for the performance of a Spark application, and understanding how they are used can help you optimize your Spark jobs and avoid issues such as OutOfMemory errors.

What is unified Memory Management in Spark?
    - Unified Memory Management is a feature in Spark that allows for dynamic allocation of memory between execution and storage.
    - With unified memory management, Spark can automatically adjust the amount of memory allocated for execution (e.g., for shuffling, sorting, and aggregations) and storage (e.g., for caching and persisting data) based on the workload and available resources.
    - This helps improve performance and resource utilization by allowing Spark to make better use of the available memory and avoid issues such as OutOfMemory errors.
    - There are mainly two types of memory management in Spark: unified memory management and static memory management. 
        - Unified memory management allows for dynamic allocation of memory between execution and storage, while static memory management requires manual configuration of memory allocation for execution and storage.

On-heap vs off-heap memory 
spark.memory.fraction (0.6 default) splits heap into execution + storage.
OOM fixes: increase executor memory, reduce cache, use persist(MEMORY_AND_DISK), check for data skew causing spill.	
EMR job OOM: executor logs show spill to disk → increase spark.executor.memory from 8g to 16g + enable off-heap.


Transaction log (_delta_log):
    - JSON + Parquet checkpoint files record every operation.
        - JSON files store metadata about the operations performed on the Delta Lake, such as the type of operation (e.g., insert, update, delete), the timestamp of the operation, and the user who performed the operation.
        - Parquet checkpoint files store the actual data changes that have been made to the Delta Lake. 
        - These files are used to efficiently store and manage the data changes, allowing for fast reads and writes to the Delta Lake.
    - ACID via optimistic concurrency control. 
    - Snapshot isolation for concurrent reads/writes. 
    - Time travel via log replay.
