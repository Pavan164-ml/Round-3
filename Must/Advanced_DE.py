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



What is a checkpoint in Spark and why is it important?
    - A checkpoint in Spark is a mechanism for saving the state of an RDD or DataFrame to a reliable storage system (e.g., HDFS) at a specific point in time.
    - Checkpointing is important because it provides fault tolerance in Spark applications. If a node fails during the execution of a Spark job, the checkpointed data can be used to recover the lost data and continue processing without having to start from scratch.
    - Checkpointing is particularly important for long-running Spark applications or applications that involve complex transformations, as it helps ensure that the application can recover from failures and continue processing without losing significant progress.

What is the difference between a checkpoint and a cache/persist in Spark?
    - A checkpoint is a mechanism for saving the state of an RDD or DataFrame to a reliable storage system
    - While cache/persist is a mechanism for storing data in memory for faster access.
    - Checkpointing is used for fault tolerance and recovery, while caching/persisting is used for performance optimization.
    - Checkpointing involves writing data to disk, which can be slower than caching/persisting data in memory. However, checkpointing provides durability and allows for recovery from failures, while caching/persisting does not provide durability and may lead to data loss if the application fails.

What is checkpointing in delta? What does it store and why is it important?
    - Checkpointing in Delta Lake is a mechanism for saving the state of the Delta Lake at a specific point in time.
    - It stores the state of the Delta Lake, including the metadata and data changes, allowing for efficient recovery and time travel.
    - Checkpointing saves the memory overhead of 1000s of JSON files in the transaction log by consolidating them into a single checkpoint file, which can be read more efficiently during recovery and time travel operations. 
    - This helps improve performance and reduces the time required to recover from failures or access historical data in the Delta Lake.

Do users need to manage the checkpoints in the lakehouse architecture? 
    - No, users do not need to manage the checkpoints in the lakehouse architecture.
    - Delta Lake automatically manages the checkpoints for you, creating them at regular intervals based on the number of transactions or the amount of data changes.
    - Users can configure the checkpointing behavior (e.g., how often to create checkpoints), but they do not need to manually create or manage the checkpoints themselves.

What are the contents of JSON file in delta log?
    - The JSON files in the Delta Lake transaction log contain metadata about the operations performed on the Delta Lake, such as the type of operation (e.g., insert, update, delete), the timestamp of the operation, and the user who performed the operation.
    - These JSON files are used to track the history of changes made to the Delta Lake and provide information about the operations that have been performed on the data.

What is Optimistic concurrency control in Delta Lake and how does it ensure ACID properties?
    - Optimistic concurrency control is a technique used in Delta Lake to manage concurrent updates to the same data by multiple users or processes.
    - It works by allowing multiple users to read and modify the same data simultaneously, but it checks for conflicts before committing the changes. 
        - If a conflict is detected (e.g., two users trying to update the same record), one of the transactions will be rolled back, and the user will need to retry their operation.
    - This approach helps ensure the table is in valid state and maintains the ACID properties (Atomicity, Consistency, Isolation, Durability) of the data in Delta Lake, even in the presence of concurrent updates.
    - Atomicity: ensures that a transaction is treated as a single unit of work, which either succeeds completely or fails completely. 
        - If a conflict is detected, the transaction will be rolled back, ensuring that partial updates do not occur.
    - Consistency: ensures that the data remains in a valid state after a transaction is committed.
        - By checking for conflicts before committing changes, optimistic concurrency control helps maintain the consistency of the data in Delta Lake.
    - Isolation: ensures that concurrent transactions do not interfere with each other.
        - By allowing multiple users to read and modify the same data simultaneously, optimistic concurrency control helps maintain isolation between transactions.
    - Durability: ensures that once a transaction is committed, it will persist even in the event of a failure.
        - By using a transaction log and checkpointing, Delta Lake ensures that committed transactions are durable and can be recovered in the event of a failure.


what is MERGE INTO in lakehouse architecture ?
    - upsert (match → update, no match → insert).
    - This is internally possible by using lakehouse becuase of the ACID properties and optimistic concurrency control provided by Delta Lake, which allows for concurrent updates and ensures data integrity during the merge operation.
    - MERGE INTO is a powerful operation that allows you to perform both updates and inserts in a single statement, making it easier to manage and maintain your data in a lakehouse architecture. It is particularly useful for scenarios such as slowly changing dimensions, where you need to update existing records while also inserting new records based on certain conditions.
 
OPTIMIZE: compacts small files.
    - As we perform updates and inserts in a Delta Lake, it can lead to the creation of many small files, which can degrade performance over time.
    - The OPTIMIZE command is used to compact these small files into larger files, which can improve query performance by reducing the number of files that need to be read during query execution.
    - Ideally we perform optimize after every 10-20 updates/inserts, but the optimal frequency can vary based on the specific workload and data characteristics. 
    - How does it work internally?
        - The OPTIMIZE command works by reading the small files and writing them back as larger files. 
        - It uses a process called file compaction, which involves merging the small files into larger files while maintaining the integrity of the data.

ZORDER BY: co-locate related data for skip-friendly reads.
    - ZORDER BY is a technique used in Delta Lake to co-locate related data for skip-friendly reads.
    - This is especially useful for optimizing query performance when filtering on specific columns, as it allows Spark to skip over irrelevant data and read only the relevant data for the query.
    - For example, if you have a large Delta Lake table and you frequently filter on a specific column (e.g., user_id), you can use ZORDER BY to co-locate the data based on that column. 
    - This allows Spark to skip over irrelevant data and read only the relevant data for the query, improving performance.

How is indexing different than ZORDER BY in Delta Lake?
    - Indexing is a technique used to improve query performance by creating a data structure that allows for faster lookups based on specific columns. 
    - ZORDER BY, on the other hand, is a technique used to co-locate related data (that means physically placing related data together in the same files) for skip-friendly reads, which can also improve query performance but does not involve creating a separate data structure like an index.
    - While both techniques can help improve query performance, they serve different purposes and are implemented differently in Delta Lake. 
        - Indexing typically involves creating a separate data structure that allows for fast lookups based on specific columns, while ZORDER BY involves physically co-locating related data in the same files to optimize read performance.

How does indexing work in the backend when we enable indexing for a column? Can I index a column which is unique to each record in a table?
    - When you enable indexing for a column in Delta Lake, it creates a data structure (such as a B-tree or hash index) that allows for faster lookups based on the values in that column.
    - The index is built by scanning the data in the Delta Lake and creating entries in the index for each unique value in the indexed column, along with pointers to the corresponding records in the data files.
    - If you index a column that is unique to each record in a table (e.g., a primary key), it can still be beneficial for query performance, as it allows for fast lookups based on that unique column.
    - However, the performance benefits may be less pronounced compared to indexing a column with more duplicate values, as the index will have fewer entries and may not provide as much of a performance boost for queries that filter on that unique column.
    - It is generally more beneficial to index columns that have a higher cardinality (i.e., more unique values) and are frequently used in query filters, as this can provide more significant performance improvements for those queries.
        - For example, you can index a column like user_id, which may have many duplicate values, to improve query performance when filtering on that column. 
        - On the other hand, indexing a column like transaction_id, which is unique for each record, may not provide as much of a performance boost for queries that filter on that column.
        - Also for columns like country_name, which may have a limited number of unique values, indexing can still be beneficial for improving query performance when filtering on that column.

How exactly does the B-tree help in faster lookups when we enable indexing for a column in Delta Lake?
    - A B-tree is a self-balancing tree data structure that maintains sorted data and allows for efficient insertion, deletion, and search operations.
    - When you enable indexing for a column in Delta Lake, it creates a B-tree index for that column. 
    - The B-tree index organizes the unique values of the indexed column in a hierarchical structure, where each node contains a range of values and pointers to the corresponding records in the data files.
    - When you perform a query that filters on the indexed column, Spark can use the B-tree index to quickly navigate through the tree structure to find the relevant entries for the filter condition. 
    - This allows Spark to skip over irrelevant data and read only the relevant data for the query, resulting in faster query performance compared to scanning the entire dataset.
    - So does B-tree have some kind of meta data about the column values and their corresponding file locations? 
        - Yes, the B-tree index contains metadata about the unique values in the indexed column and their corresponding file locations. 
        - Each entry in the B-tree index includes the unique value from the indexed column and a pointer to the location of the corresponding records in the data files. 
        - This allows Spark to quickly navigate through the B-tree structure to find the relevant entries for a given filter condition, improving query performance by reducing the amount of data that needs to be read during query execution.

VACUUM: remove old files (default 7-day retention).
    - The VACUUM command in Delta Lake is used to remove old files that are no longer needed for the current state of the data.
    - By default, Delta Lake retains old files for 7 days to allow for time travel and recovery from accidental deletes or updates. 
    - However, if you want to free up storage space and remove old files that are no longer needed, you can use the VACUUM command to specify a retention period (e.g., VACUUM my_table RETAIN 3 HOURS) to remove files that are older than the specified retention period.
    - It is important to note that once files are removed using the VACUUM command, they cannot be recovered, so it is recommended to use this command with caution and ensure that you have a backup of your data before running it.

How do we ensure we do not delete necessary files when we run VACUUM in Delta Lake?
    - To ensure that you do not delete necessary files when running the VACUUM command in Delta Lake, you can take the following precautions:
        - Review the retention period: Before running the VACUUM command, review the retention period you are specifying to ensure that it is appropriate for your use case. 
            - For example, if you have a retention period of 7 days, make sure that you do not have any files that are still needed for time travel or recovery that are older than 7 days.
        - Take a backup: It is always a good practice to take a backup of your data before running the VACUUM command, especially if you are unsure about the retention period or if you have critical data that cannot be easily recovered.
        - Monitor the VACUUM process: After running the VACUUM command, monitor the process to ensure that it is completing successfully and that no necessary files are being deleted. 
            - You can check the logs and metrics to verify that the VACUUM operation is proceeding as expected and that no errors or issues are occurring during the process.

The tools like VACUUM, OPTIMIZE and Checkpointing in Delta Lake are crucial for maintaining the health and performance of your Delta Lake tables. 
    - They help manage storage, improve query performance, and ensure data integrity, but they should be used with caution to avoid unintended consequences such as data loss or performance degradation. 
    - Always review the documentation and best practices before using these tools in a production environment.

DESCRIBE HISTORY for audit.
    - The DESCRIBE HISTORY command in Delta Lake is used to retrieve the history of operations performed on a Delta Lake table. 
    - It provides information about the operations such as the type of operation (e.g., insert, update, delete), the timestamp of the operation, and the user who performed the operation.
    - This command is useful for auditing purposes, as it allows you to track changes made to the Delta Lake table over time and identify who made those changes. 
    - It can also be helpful for debugging and troubleshooting issues with the data, as it provides a record of all operations performed on the table.

Medallion Arcitecture: data organized into layers (Bronze, Silver, Gold) with increasing levels of quality and transformation.

Bronze: raw ingestion (schema-on-read, append-only). 
    - Usually partitioned on insert_date 
    - Contains raw, unprocessed data
    - This layer is typically used for initial data ingestion and storage, where the data is stored in its raw form without any transformations or cleaning applied.
    - This can be schema or read (meaning the data is stored without a predefined schema and can be read with different schemas as needed) and is often append-only, meaning that new data is added to the existing data without modifying or deleting existing records.
    - Source of truth for data, used for reprocessing and recovery in case of issues with downstream layers. 

Silver: cleaned, deduplicated, validated (schema enforced).
    - This layer contains cleaned, deduplicated, and validated data.
    - The data in this layer has been processed to remove duplicates, handle missing values, and ensure that it adheres to a predefined schema.
    - This layer is typically used for intermediate processing and transformation of the data, where the data is prepared for further analysis or consumption.

Gold: aggregated, business-ready, optimized for consumption. Quality gates between each layer.
    - This layer contains aggregated, business-ready data that is optimized for consumption.
    - The data in this layer has been transformed and aggregated to meet specific business requirements and is typically used for reporting, analytics, and other downstream applications.
    - This layer is optimized for performance and may include additional optimizations such as indexing or partitioning to improve query performance.


Data Modeling	

SCD Types in Delta Lake	

SCD stands for Slowly Changing Dimension, which is a common data modeling technique used to manage and track changes to dimensional data over time. 
In Delta Lake, there are several types of SCDs that can be implemented:

Type 1: overwrite (no history). 
    - In this type, when a change occurs to a record, the existing record is overwritten with the new values, and no history of the previous values is maintained.
Type 2: new row per change with start/end dates — full history. 
    - In this type, when a change occurs to a record, a new row is created with the new values, and the previous row is marked with an end date to indicate that it is no longer active. 
    - This allows for maintaining a full history of changes to the data.
Type 3: add column for previous value. 
    - In this type, when a change occurs to a record, a new column is added to store the previous value of the changed attribute. 
    - This allows for tracking the previous value while still maintaining the current value in the same row.
Type 6: hybrid. 
    - In this type, a combination of Type 1, Type 2, and Type 3 is used to manage changes to the data. 
    - For example, you might use Type 2 to maintain a full history of changes for certain attributes, while using Type 1 for other attributes that do not require history, and Type 3 for attributes where you want to track the previous value without creating a new row.

Delta MERGE INTO is the standard implementation for Type 2.
    - This command allows you to perform upserts (updates and inserts) in a single operation, making it ideal for managing slowly changing dimensions in Delta Lake.


Data Quality	

Data Quality & Anomaly Detection	

Data quality is crucial for ensuring the reliability and accuracy of data in a lakehouse architecture.
It involves assessing and improving the quality of data based on various dimensions such as completeness, accuracy, consistency, timeliness, and uniqueness.

Dimensions: 
    1. completeness
        - Completeness refers to the extent to which all required data is present in the dataset. It involves checking for missing values, nulls, or incomplete records that may impact the quality of the data and the insights derived from it.
    2. accuracy
        - Accuracy refers to the extent to which the data correctly represents the real-world values or events it is intended to model. It involves validating the data against known standards or reference data to ensure correctness.
    3. consistency
        - Consistency refers to the extent to which the data is uniform and free from contradictions across different datasets or within the same dataset over time. It involves checking for discrepancies and ensuring that data follows defined rules and formats.
    4. timeliness
        - Timeliness refers to the extent to which the data is up-to-date and available when needed. It involves monitoring data latency and ensuring that data is delivered within acceptable timeframes for decision-making.
    5. uniqueness
        - Uniqueness refers to the extent to which each record in the dataset is distinct and not duplicated. It involves identifying and removing duplicate records to maintain data integrity.

Tools: 
    - Great Expectations 
    - Deequ
   

Anomaly detection: 

What are the key components of Lahkehouse Monitoring?
- Lakehouse monitoring provides the data profiling using 2 main components:
    1. Profile Metrics Table
        - contains summary statistics of the data, such as counts, means, standard deviations, and distributions for each column.
        - This can be used to identify data quality issues, such as missing values, outliers, or changes in data distribution over time.
    2. Drift Metrics Table
        - contains statistics related to the data’s drift over time.
        - This can include metrics such as the percentage of new values in a column, the percentage of missing values, or changes in the distribution of values for a column.

What is standard deviation and how is it used in data quality monitoring?
    - Standard deviation is a measure of the amount of variation or dispersion in a set of values. It quantifies how much the values in a dataset deviate from the mean (average) value.
        - For example, if you have a dataset of test scores with a mean of 100 and a standard deviation of 5, it means that most of the scores are within 5 points of the mean (i.e., between 95 and 105). 
        - A higher standard deviation would indicate that the scores are more spread out, while a lower standard deviation would indicate that the scores are more clustered around the mean.
        - Higher the standard deviation more the variance in the data, and lower the standard deviation more consistent the data is.
        - Always standard deviation is interpreted with a particular data point comparing to the whole mean of the data.
        - In data quality monitoring, standard deviation can be used to identify outliers or anomalies in the data. 
            - For example, if a column has a mean value of 100 and a standard deviation of 10, any value that is significantly higher or lower than 100 (e.g., 150 or 50) may be considered an outlier and may indicate a potential data quality issue that needs to be investigated further.

What is z-score?
    - Z-score is a statistical measure that quantifies how many standard deviations a data point is from the mean of a distribution.

Other important concepts in data quality monitoring:
    - Rolling average: This is a technique used to smooth out short-term fluctuations in data and identify trends over time. 
        - It involves calculating the average of a specific number of data points (e.g., the last 7 days) and updating it as new data points are added.
    - Data drift: This refers to changes in the distribution of data over time, which can impact the performance of machine learning models and the accuracy of insights derived from the data.
        - For example, if you have a dataset of customer demographics and the distribution of age groups changes significantly over time, it may indicate data drift that could affect the performance of a model trained on that data.
        - As the model was trained with balanced class distribution previously, therefore the weights and bias were adjusted accordingly, but now the distribution has changed and become imbalanced, it may lead to biased predictions and reduced accuracy of the model.

Airflow Advanced Concepts

- Airflow is a powerful workflow orchestration tool that allows you to programmatically author, schedule, and monitor complex data pipelines.
- It is a very popular choice of workflow orchestration tool in the data engineering community due to its flexibility, scalability, and rich ecosystem of integrations with various data sources and processing frameworks.
- It is natively built in Python, which makes it easy to use and extend for data engineering tasks.
- The power of Airflow lies in its ability to manage complex dependencies between tasks, handle retries and failures gracefully, and provide a rich set of features for monitoring and logging the execution of workflows.


Following are some of the advanced concepts in Airflow that are important for data engineers to understand:
There are 5 main components of Airflow:
    - Webserver : This is the component that provides the user interface for Airflow, allowing you to view and manage your workflows, monitor their execution, and access logs and other information about your tasks.
    - Scheduler: This is the component that is responsible for scheduling and executing your workflows based on the defined DAGs (Directed Acyclic Graphs) and their dependencies.
    - Metadatabase: This is the component that stores the metadata about your workflows, tasks, and their execution history. It is typically a relational database such as PostgreSQL or MySQL.
    - Executor: This is the component that is responsible for executing the tasks in your workflows. Airflow supports different types of executors, such as LocalExecutor, CeleryExecutor, and KubernetesExecutor, which allow you to run tasks on different types of infrastructure.
    - Workers : These are the components that actually execute the tasks in your workflows. Depending on the executor you choose, workers can be processes running on the same machine (LocalExecutor), distributed workers running on multiple machines (CeleryExecutor), or containers running in a Kubernetes cluster (KubernetesExecutor).


What are different executors in airflow and when to choose them?
    - LocalExecutor: This executor runs tasks in parallel on the same machine. It is suitable for small to medium-sized workloads and is easy to set up and use.
    - CeleryExecutor: This executor distributes tasks across multiple worker nodes using Celery, a distributed task queue. It is suitable for large-scale workloads and provides better scalability and fault tolerance.
    - KubernetesExecutor: This executor runs tasks in Kubernetes pods, allowing for dynamic scaling and isolation of tasks. It is suitable for cloud-native environments and provides the highest level of scalability and resource management.

What is MWAA?
    - MWAA stands for Managed Workflows for Apache Airflow, which is a fully managed service provided by Amazon Web Services (AWS) that allows you to run Apache Airflow workflows in the cloud without having to manage the underlying infrastructure.
    - MWAA provides a scalable and secure environment for running Airflow workflows, with features such as automatic scaling, high availability, and integration with other AWS services.
    - With MWAA, you can focus on developing and managing your Airflow workflows while AWS takes care of the operational aspects of running and maintaining the Airflow environment.

How does Amazon host Airflow (MWAA) work in the backend?
    - MWAA is built on top of Amazon Elastic Kubernetes Service (EKS) and uses Amazon RDS for the Airflow metadata database.
    - When you create an MWAA environment, AWS provisions the necessary infrastructure, including the Kubernetes cluster and RDS instance, and sets up Airflow on top of it.
    - MWAA uses the KubernetesExecutor to run Airflow tasks in Kubernetes pods, allowing for dynamic scaling and isolation of tasks.

What are important concepts in Airflow code for data engineers?
    1. DAGs (Directed Acyclic Graphs): These are the core building blocks of Airflow workflows, representing the structure and dependencies of tasks in a workflow.
    2. Tasks: These are the individual units of work in a DAG, representing a single operation or step in the workflow.
    3. XComs: These are used to pass data between tasks (small payloads only).
    4. Sensors: These wait for a condition to be met (e.g., S3KeySensor, ExternalTaskSensor). 
    5. TaskGroups: These replace SubDAGs. 
    6. Dynamic DAGs: These generate tasks from configuration at parse time.
    7. Pools: These are used for concurrency control.
    8. Operators: These are the building blocks of tasks, representing specific actions to be performed (e.g., PythonOperator, BashOperator, etc.).
    9. Hooks: These are interfaces to external systems (e.g., databases, APIs) that allow tasks to interact with those systems.
    10. Branches: These allow for conditional execution of tasks based on certain conditions or criteria.
    11. SubDAGs: These are used to create reusable components within a DAG, allowing you to encapsulate a set of tasks and their dependencies into a single unit that can be reused across multiple DAGs. However, it is recommended to use TaskGroups instead of SubDAGs for better performance and maintainability.

Explain more on XComs in airflow? Why do we need them and how do they work?
    - XComs (short for "cross-communication") are a feature in Airflow that allows tasks to exchange small amounts of data between each other. 
    - They are used to pass information between tasks in a DAG, such as the output of one task that needs to be used as input for another task.
    - XComs work by allowing tasks to push and pull data to and from a shared storage mechanism (e.g., the Airflow metadata database).
    - A task can push a value to an XCom using the `xcom_push` method, and another task can retrieve that value using the `xcom_pull` method.
    - For example, if you have a task that generates a file path as output, you can push that file path to an XCom, and another task can pull that file path from the XCom to read the file in a subsequent step of the workflow.

Explain different types of operators available in airflow:
    - PythonOperator: This operator allows you to execute a Python function as a task in your DAG. It is commonly used for tasks that involve data processing, transformations, or any custom logic that can be implemented in Python.
    - BashOperator: This operator allows you to execute a bash command or script as a task in your DAG. It is useful for tasks that involve running shell commands, scripts, or interacting with the operating system.
    - EmailOperator: This operator allows you to send an email as a task in your DAG. It is commonly used for sending notifications or alerts based on the outcome of other tasks in the workflow.
    - HttpOperator: This operator allows you to make HTTP requests as a task in your DAG. It is useful for tasks that involve interacting with APIs or web services.
    - SqlOperator: This operator allows you to execute SQL queries as a task in your DAG. It is commonly used for tasks that involve querying databases or performing database operations.
    - S3KeySensor: This sensor waits for a specific key (file) to be present in an S3 bucket before allowing downstream tasks to proceed. It is useful for workflows that depend on the availability of files in S3.
    - ExternalTaskSensor: This sensor waits for a specific task in another DAG to complete before allowing downstream tasks to proceed. It is useful for coordinating workflows across multiple DAGs.

TaskGroups: replace SubDAGs for better performance and maintainability.
    - TaskGroups are a feature in Airflow that allows you to group related tasks together within a DAG, providing better organization and readability of your workflows.
    - They replace the older SubDAGs feature, which was used to create reusable components within a DAG but had performance and maintainability issues.
    - TaskGroups allow you to encapsulate a set of tasks and their dependencies into a single unit that can be reused across multiple DAGs, while also providing better performance and easier maintenance compared to SubDAGs.
    - With TaskGroups, you can define a group of tasks with a specific name and then reference that group in your DAG, making it easier to manage and maintain complex workflows with multiple related tasks.

Dynamic DAGs: 
    - Generate tasks from config at parse time.
    - Dynamic DAGs are a feature in Airflow that allows you to generate tasks dynamically based on a configuration or input at the time of parsing the DAG.
    - This is useful for scenarios where the number of tasks or their parameters may not be known until runtime, such as when processing a variable number of files or when the tasks need to be generated based on external data.
    
Explain the concept of Pools in Airflow and how they are used for concurrency control in very simple terms:
    1. Pools are a way to limit the number of tasks that can run at the same time for a specific resource.
        - For example, if you have a database that can only handle a certain number of connections, you can create a pool for that database and limit the number of tasks that can access it concurrently.
    2. When a task is assigned to a pool, it will only run if there are available slots in that pool. If the pool is full, the task will wait until a slot becomes available.
    3. This helps to manage resources and ensure that critical tasks do not overwhelm the system or interfere with other tasks that require shared resources.
    4. A real world use case of this is when you have a task that interacts with an external API that has rate limits. You can create a pool for that API and limit the number of concurrent tasks that can access it, ensuring that you do not exceed the rate limits and avoid getting blocked by the API provider.
        - When the number of tasks trying to access the API exceeds the limit defined in the pool, the excess tasks will be queued and will only run when a slot becomes available in the pool, allowing you to manage the concurrency of tasks and avoid overwhelming the API.

Data Engineering Data storage formats

Parquet vs ORC vs Avro	
    - Parquet: columnar that means data is stored column-wise, which allows for better compression and faster query performance for analytical workloads. 
        - Best for analytics (predicate pushdown, column pruning)
        - Disadvantages: not ideal for streaming or row-based processing, and may have slower write performance compared to row-based formats.
    - ORC: columnar, better compression, Hive-native
        - Best for Hive workloads, similar advantages to Parquet but with better compression and performance for certain use cases.
        - Disadvantages: similar to Parquet, not ideal for streaming or row-based processing, and may have slower write performance compared to row-based formats.
    - Avro: row-based, schema evolution support, ideal for Kafka streaming
        - Best for streaming and row-based processing, with strong support for schema evolution and compatibility.
        - Disadvantages: not as efficient for analytical workloads compared to columnar formats like Parquet and ORC, and may have larger file sizes due to row-based storage.
    - All support Snappy/GZIP compression.

What is the difference between Parquet and ORC ?
    - Parquet and ORC are both columnar storage formats that are optimized for analytical workloads, but they have some differences in terms of their features and performance characteristics.
    - Parquet is a widely used columnar storage format that is supported by many big data processing frameworks, including Apache Spark, Apache Hive, and Apache Impala. 
        - It provides efficient compression and encoding techniques, which can lead to smaller file sizes and faster query performance for analytical workloads. 
        - Parquet also supports schema evolution, allowing you to add or modify columns without breaking existing data.
    - ORC (Optimized Row Columnar) is another columnar storage format that is optimized for Hive workloads. 
        - It provides better compression and performance for certain use cases compared to Parquet, especially when working with large datasets in Hive. 
        - ORC also supports advanced features such as predicate pushdown and column pruning, which can further improve query performance.

What is Hive ?
    - Hive is a data warehousing and SQL-like query language that is built on top of the Hadoop ecosystem. 
    - It provides a high-level interface for querying and managing large datasets stored in Hadoop Distributed File System (HDFS) using a SQL-like syntax called HiveQL.
    - Hive allows users to perform data analysis and querying on large datasets without having to write complex MapReduce code, making it easier for data analysts and data scientists to work with big data.
    - It also provides features such as schema management, partitioning, and indexing to optimize query performance on large datasets.

What is Athena in AWS? What is the sql it uses ?
    - Amazon Athena is a serverless interactive query service provided by AWS that allows you to analyze data stored in Amazon S3 using standard SQL. 
    - It is built on top of the Presto distributed SQL query engine and provides a simple and cost-effective way to query large datasets without having to manage any infrastructure.
    - Athena uses ANSI SQL, which is a standard SQL syntax that is widely supported across different database systems. 
    - This means that you can use familiar SQL syntax to query your data in S3, making it easy for data analysts and data scientists to work with their data without having to learn a new query language. 
    - The backend on Athena is Presto, which is a distributed SQL query engine that allows for fast querying of large datasets across multiple data sources, including S3, HDFS, and relational databases.

How is Presto different from Hive in simple words?
    - Presto and Hive are both SQL query engines that are used for querying large datasets, but they have some key differences in terms of their architecture and performance characteristics.
    - Presto is a distributed SQL query engine that is designed for interactive querying of large datasets across multiple data sources. It is optimized for low-latency queries and provides fast performance for ad-hoc analysis and reporting. 
        - Presto can query data from various sources, including S3, HDFS, and relational databases, making it a versatile choice for querying data in a lakehouse architecture.
    - Hive, on the other hand, is a data warehousing and SQL-like query language that is built on top of the Hadoop ecosystem. It is designed for batch processing of large datasets and is optimized for high-throughput queries. 
        - Hive is typically used for ETL processes and data warehousing workloads, where the focus is on processing large volumes of data rather than low-latency querying. 
        - Hive queries are executed using MapReduce or Tez, which can result in longer query execution times compared to Presto's distributed architecture.

    So to simply put, Presto is optimized for interactive querying and low-latency performance and useful for ad-hoc analysis, while Hive is optimized for batch processing and high-throughput workloads useful for ETL and data warehousing.


AWS EMR Deep Dive

What is an EMR and how does it solve the big data processing problem?
    - Amazon EMR (Elastic MapReduce) is a cloud-based big data processing service provided by AWS that allows you to process and analyze large datasets using popular big data frameworks such as Apache Spark, Apache Hadoop, and Apache Hive.
    - EMR provides a scalable and flexible environment for running big data workloads, allowing you to easily provision and manage clusters of virtual machines (EC2 instances) to process your data.
    - EMR solves the big data processing problem by providing a managed environment for running big data frameworks, which eliminates the need for you to set up and manage your own infrastructure. 
    - It also provides features such as auto-scaling, which allows your cluster to automatically adjust its size based on the workload, and integration with other AWS services, such as S3 for storage and IAM for security, making it easier to build and manage end-to-end big data processing pipelines in the cloud.

What are the important components of an EMR cluster?
    - An EMR cluster consists of several components that work together to process and analyze big data workloads. The key components of an EMR cluster include:
    - Master node: This is the primary node in the cluster that manages the cluster and coordinates the execution of tasks. It runs the cluster management software and is responsible for scheduling and monitoring tasks across the cluster.
    - Core nodes: These are the worker nodes in the cluster that run the big data processing frameworks (e.g., Spark, Hadoop) and execute the tasks assigned by the master node. They also store data on local disks and can be used for HDFS storage.
    - Task nodes: These are optional nodes that can be added to the cluster to handle additional processing tasks. They do not store data in HDFS and are typically used for transient workloads or spot instances.
    
There are different cluster modes in EMR: 
    - Cluster mode: In this mode, the EMR cluster is provisioned and runs continuously until it is manually terminated. This mode is suitable for long-running workloads or when you need to maintain a persistent cluster for ongoing data processing tasks.
    - Step mode: In this mode, you can submit individual steps (tasks) to an existing EMR cluster without having to manage the cluster lifecycle. This is useful for running ad-hoc tasks or when you want to run specific jobs on an existing cluster without having to start and stop the cluster for each job.

There are different types of cluster types in EMR:
    - On-Demand Clusters: These clusters are provisioned and billed on an hourly basis, and you can start and stop them as needed. They provide flexibility and are suitable for workloads with variable or unpredictable usage patterns.
    - Spot Clusters: These clusters use spare EC2 capacity and are available at a significantly lower cost compared to on-demand clusters. However, they can be interrupted by AWS with a two-minute warning if the capacity is needed for other purposes.
    - Spot clusters are ideal for fault-tolerant workloads that can handle interruptions, such as batch processing or data analysis tasks.

EMRFS for S3 consistency:
    - EMRFS (EMR File System) is a component of Amazon EMR that provides a consistent view of data stored in Amazon S3. 
    - It is designed to address the eventual consistency model of S3, which can lead to issues when processing data in S3 using big data frameworks like Spark or Hadoop.
    - EMRFS uses a metadata store to track the state of files in S3 and provides a consistent view of the data, ensuring that tasks running on the EMR cluster can access the most up-to-date data in S3 without encountering consistency issues.

EMR Serverless for autoscaling? Which cluster type provided Autoscaling is it on-demand or spot?
    - EMR Serverless is a deployment option for Amazon EMR that allows you to run big data workloads without having to manage the underlying infrastructure. 
    - It provides automatic scaling of resources based on the workload, allowing you to focus on developing and running your big data applications without worrying about cluster management.
    - EMR Serverless is available for both on-demand and spot clusters, providing flexibility in terms of cost and resource management. 
    - With EMR Serverless, you can take advantage of the cost savings of spot instances while still benefiting from the automatic scaling and managed environment provided by EMR.
 
Spot instances for 60-70% cost saving on task nodes with interruption handling
    - Spot instances are a cost-effective option for running workloads on Amazon EMR, as they can provide significant cost savings compared to on-demand instances. 
    - By using spot instances for task nodes in your EMR cluster, you can save up to 60-70% on your compute costs.
    - However, it is important to note that spot instances can be interrupted by AWS with a two-minute warning if the capacity is needed for other purposes. 
    - To handle interruptions when using spot instances, you can implement strategies such as checkpointing your tasks, using a combination of on-demand and spot instances, or designing your workloads to be fault-tolerant and able to handle interruptions gracefully.


AWS Athena & Glue	

Athena: serverless SQL on S3
    - Amazon Athena is a serverless interactive query service that allows you to analyze data stored in Amazon S3 using standard SQL. 
    - It is built on top of the Presto distributed SQL query engine and provides a simple and cost-effective way to query large datasets without having to manage any infrastructure.
    - Pay per byte scanned — partition pruning is critical as it can significantly reduce the amount of data scanned and improve query performance, which can lead to cost savings when using Athena.
    

Glue Catalog: The main goal of Glue Catalog is to provide a central metastore for storing metadata about your data, such as table definitions, schemas, and partitions.
    - Central metastore for storing metadata about your data.
    - Glue Crawlers: auto-discover schema.
        - Glue Crawlers are a feature of AWS Glue that automatically discover and catalog the schema of your data stored in Amazon S3.
        - They can crawl your data sources, such as S3 buckets, and create or update tables in the Glue Data Catalog based on the discovered schema.
    - CTAS: create table from query result
        - CTAS (Create Table As Select) is a feature in AWS Glue that allows you to create a new table based on the result of a query. 
        - This can be useful for transforming or aggregating data before storing it in a new table.
    - Partition projection: skip crawler for time-partitioned data.
        - Partition projection is a feature in AWS Glue that allows you to define the partitioning scheme for your data without having to run a crawler to discover the partitions.

Suppose we use a spark job to write to a table without specifiying its schema would cralwer be able to discover the schema of the new table?
    - Yes, if you use a Spark job to write to a table in Amazon S3 without specifying its schema, the Glue Crawler can be configured to automatically discover the schema of the new table. 
    - When you run the crawler, it will scan the data in the specified S3 location and infer the schema based on the structure of the data. 
    - The crawler will then create or update the corresponding table in the Glue Data Catalog with the discovered schema, allowing you to query and analyze the data using services like Athena or Redshift Spectrum.


My Data is present in S3 processed using pyspark through EMR orchestrated using Airflow  queried though athena how does it all tie together with Glue? The question is if Glue is even necessary in this case ?
    - In this case, Glue can play a crucial role in managing the metadata and schema of your data stored in S3.
    - Glue Catalog can serve as a central repository for storing metadata about your data, such as table definitions, schemas, and partitions.
    - When you process your data using PySpark on EMR, you can write the output to S3 in a structured format (e.g., Parquet) and then use Glue Crawlers to automatically discover the schema of the new data and update the Glue Data Catalog accordingly.
    - This allows you to easily query and analyze the data using Athena, as Athena can leverage the metadata stored in the Glue Catalog to understand the structure of the data and optimize query performance.
        - So whenever a table is queried using athena, it internally looks up the Glue Catalog to get the metadata information about the table, such as its schema and partitions, which allows it to efficiently query the data stored in S3.
    - Additionally, Glue can also be used to perform ETL (Extract, Transform, Load) operations on your data, allowing you to transform and prepare your data for analysis before storing it in S3.
