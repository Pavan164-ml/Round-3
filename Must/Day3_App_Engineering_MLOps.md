"""
DAY 3 — APPLICATION ENGINEERING + MLOps
Interview: 26 May 2026

Topics: FastAPI, REST Design, Auth, Docker, K8s, CI/CD,
        MLflow, Feature Stores, Model Deployment, Observability
"""

# =============================================================================
# Basics of API and REST Design Principles
# =============================================================================


"""

What are fundamental concepts of API ? Why do we need them for data products?
  - API (Application Programming Interface) is a set of rules and protocols that allows different software applications to communicate with each other. 
  - For data products, APIs are essential because they provide a standardized way for clients (e.g., frontend applications, other services) to interact with the backend data and logic. 
  - APIs enable decoupling of the frontend and backend, allowing for flexibility in development and deployment. They also facilitate integration with other systems and enable scalability by allowing multiple clients to access the same data product.

Why can't frontend applications directly access databases or data sources in a data product architecture?
  - Security: Direct access to databases can expose sensitive data and increase the attack surface. 
  - APIs can implement authentication, authorization, and input validation to protect the data.
  - Abstraction: APIs provide a layer of abstraction that allows the backend to change its implementation without affecting the frontend. 
  - This means you can switch databases, optimize queries, or change data models without breaking the client applications.
  - The real world application for this is, if you have a mobile app and a web app both using the same data product, you can have a single API that serves both clients without needing to worry about how they access the data.

  To summarize, APIs are the standard , securre, and scalable way to access the underlying data and logic of a data product, while direct database access is generally not recommended due to security and maintainability concerns.

What are different types of APIs? Which one is most commonly used for data products and why?
  - REST (Representational State Transfer): 
    - A widely used architectural style that uses standard HTTP methods (GET, POST, PUT, DELETE) and stateless communication.
    - It is simple, scalable, and has broad support across programming languages and platforms.  
  - GraphQL: 
    - A query language for APIs that allows clients to request exactly the data they need, reducing over-fetching and under-fetching of data.
    - It is more flexible than REST but can be more complex to implement and may require additional tooling for caching and performance optimization. 
  - gRPC:
    - A high-performance, open-source RPC framework that uses Protocol Buffers for serialization. It is designed for low-latency, high-throughput communication between microservices.

  - For data products, REST APIs are most commonly used due to their simplicity, wide adoption, and ease of integration with various clients. 
  - REST's use of standard HTTP methods and status codes makes it straightforward for developers to understand and implement, while its stateless nature allows for better scalability and performance in distributed systems.
         

What is stateless nature in REST APIs? Why is it important?
  - Statelessness means that each API request from the client to the server must contain all the information needed to understand and process the request. 
  - The server does not store any session information about the client between requests, that means each request is independent and can be processed in isolation.
  - This is important because it allows for better scalability and reliability.
  - To put it simple APIs dont have memory of previous requests, so they can handle each request independently without relying on any stored state. 
    - This makes it easier to scale the API horizontally by adding more servers (where as scaling vertically means increasing the capacity of existing servers), as there is no need to synchronize session data across servers. 
    - It also improves reliability, as a failure in one request does not affect others.


When an API request is made, what are the differen parameters that are sent in the request? Explain each parameter with an example. How exactly would a database know which record to fetch when an API request is made?
  - Path Parameters: These are part of the URL and are used to identify specific resources.
    - Example: In the URL `GET /api/v1/segments/123`, the path parameter `123` identifies a specific segment. That means the API will look for the segment with ID 123 in the database and return it.
  - Query Parameters: These are key-value pairs appended to the URL after a `?` and are used to filter or sort results.
    - Example: In the URL `GET /api/v1/segments?customer_id=456&country=US`, the query parameters filter segments for a specific customer in a specific country.
  - Headers: These contain **metadata** about the request, such as authentication tokens or content type information.
    - Example: `Authorization: Bearer <token>` or `Content-Type: application/json`.
      - The Authorization header would be used by the API to validate the client's identity and permissions before processing the request.
      - The Content-Type header would inform the API about the format of the request body, allowing it to parse the data correctly.
  - Request Body: This contains the data sent by the client to the server (for POST/PUT requests).
    - Example: A JSON payload containing customer_id, country, and as_of_date for segment computation.

What is a bearer token? How is it used in API authentication?
  - A bearer token is a type of access token that is used in API authentication to grant access to protected resources.
  - It is called a "bearer" token because the client must "bear" the token in order to access the resource. 
  - The token is typically included in the Authorization header of the HTTP request in the format: `Authorization: Bearer <token>`. 

What are the important key words to know for API authentication?
  - Bearer Token: A type of access token used in API authentication to access protected resources.
  - JWT (JSON Web Token): A compact, URL-safe token format that contains claims and is often used for authentication and authorization.
  - OAuth 2.0: An authorization framework that allows third-party applications to access resources on behalf of a user.
  - API Key: A simple token that is used to authenticate a client, often included in headers or query parameters.
  - Header: A key-value pair sent in the HTTP request that can contain authentication information, such as a bearer token or API key.
  - Authentication: The process of verifying the identity of a client or user.
  - Authorization: The process of determining whether an authenticated client has permission to access a resource. That is determined based on the claims in the token (e.g., user role, permissions) and the access control rules defined in the API.
  - Claims: Information contained within a token (e.g., user ID, role, permissions) that can be used for authorization decisions.

What are the must pass parameters for an API request? Why are they important?
  - The must pass parameters for an API request depend on the specific endpoint and its requirements, but generally include:
    - API Key: Required for client authentication.
    - Authorization Header: Contains the bearer token for accessing protected resources.
    - Request Body Parameters: Data needed to perform the requested operation (e.g., customer_id, country, as_of_date).

What is the difference between API Key and Bearer Token?
  - API Key is a simple token that is used to authenticate a client, often included in headers or query parameters. It is typically static and does not contain any information about the user or permissions.    
  - Bearer Token is a type of access token used in API authentication to access protected resources. It is typically generated by an authentication server and contains claims about the user or application (claims means information about the user or application whether they have the necessary permissions).

What are different components of a REST API? Explain each component with an example.
  - Endpoint: A specific URL that represents a resource or action.
    - Example: GET /api/v1/segments/{customer_id} retrieves the segments for a specific customer.
  - HTTP Methods: Define the type of operation to perform on the resource.
    - Example: POST /api/v1/segments/compute triggers the computation of segments for a customer.
  - Request Body: The data sent by the client to the server (for POST/PUT
    - Example: A JSON payload containing customer_id, country, and as_of_date for segment computation.
  - Response: The data sent back by the server to the client, often in JSON format.
    - Example: A JSON object containing segment_id, segment_name, confidence_score, and generated
      timestamp.
  - Status Codes: Indicate the result of the HTTP request (e.g., 200 OK, 404 Not Found, 422 Unprocessable Entity).
    - Example: Returning 404 if the customer_id does not exist in the database.

What does resource mean in REST API design? How do you identify resources in a data product context?
  - In REST API design, a resource is an object or representation of data that can be accessed and manipulated via the API. 
  - Resources are typically identified by unique URLs (endpoints) and can represent entities such as customers, segments, products, etc.
  - In a data product context, you identify resources based on the key entities in your domain model. For example, if you have a data product that provides customer segmentation, your resources might include:
    - Customer: /api/v1/customers/{customer_id}
    - Segment: /api/v1/segments/{segment_id}
    - Computation Job: /api/v1/segments/compute

If you have to explain a data engineer of how the API interacts with the backend table or data source, how would you explain it?
  - The API acts as an intermediary layer between the client applications and the backend data sources (e.g., databases, data lakes).
  - When a client makes a request to an API endpoint, the API receives the request and processes it according to the defined logic. This often involves:
    1. Validating the request parameters and body.
    2. Authenticating and authorizing the request to ensure the client has permission to access the resource.
    3. Querying the backend data source (e.g., using SQL to query a Postgres database or using a data access layer to query a Delta Lake).
    4. Processing the data as needed (e.g., applying business logic, formatting the response, updating the records or deleting the records in the database).
    5. Returning the response to the client, which may include the requested data or a status message.
  - For example, if a client requests GET /api/v1/segments/{customer_id}, the API would:
    - Extract the customer_id from the URL.
    - Validate that the customer_id is in the correct format.
    - Query the backend database to retrieve the segments associated with that customer_id.
    - Format the retrieved data into a JSON response.
    - Send the response back to the client.

  - To put it simply, the API is like a waiter in a restaurant. 
    - The client (customer) pleces an order (API request)
    - The waiter (API) takes the order to the kitchen (backend data source),
    - The kitchen prepares the food (processes the data)
    - And then the waiter brings the food back to the customer (API response).    

What are various HTTP Methods and their significance in REST API design?
  - POST is used to create a new resource. It is not idempotent, meaning that calling it multiple times may result in multiple resources being created.
    - It is like inserting a new record in the database. If you run it again and again it may cause duplicate records in the database.
  - PUT is used to update an existing resource or create it if it does not exist. It is idempotent, meaning that calling it multiple times will have the same effect as calling it once.
    - It is like updating a record in the database. If you run it again and again it will update the same record with the same data, so it will not cause duplicate records in the database.
  - PATCH is used to partially update an existing resource. It is idempotent, meaning that calling it multiple times will have the same effect as calling it once.
    - It is like updating specific fields of a record in the database. If you run it again and again with the same data, it will update the same fields of the same record, so it will not cause duplicate records in the database.
  - GET is used to retrieve data from the server. It is a safe and idempotent method, meaning it does not modify data and can be called multiple times without side effects.
    - It is like querying a record from the database. If you run it again and again it will return the same record without modifying it.
  - DELETE is used to remove a resource from the server. It is idempotent, meaning that calling it multiple times will have the same effect as calling it once.
    - It is like deleting a record from the database. If you run it again and again it will delete the same record without causing any issues.


Usually is the API hosted and how does it sclae when the number of input requests increases?
  - APIs are typically hosted on web servers (e.g., Nginx, Apache) or cloud platforms (e.g., AWS, Azure, GCP) that provide the necessary infrastructure to handle incoming requests.
  - To scale an API when the number of input requests increases, you can use techniques such as:
    - Horizontal Scaling: Adding more instances of the API server behind a load balancer to distribute incoming traffic.
    - Vertical Scaling: Increasing the resources (CPU, memory) of the existing server to handle more requests.
    - Caching: Implementing caching strategies (e.g., in-memory caches like Redis) to reduce the load on the backend data sources and improve response times for frequently accessed data.
    - Rate Limiting: Implementing rate limiting to prevent abuse and ensure fair usage of the API.

What is the difference between synchronous and asynchronous API calls? When would you use one over the other?
  - Synchronous API calls block the client until a response is received from the server. The client waits for the server to process the request and return a response before it can continue with other tasks.
    - Common use case involve simple CRUD operations where the client needs an immediate response to proceed (e.g., form submission, data retrieval).
  - Asynchronous API calls allow the client to continue with other tasks while waiting for the server to process the request. The client can receive a response at a later time, often through callbacks, promises, or async/await patterns.     
    - Common use case involve long-running operations (e.g., data processing, machine learning model training) where the client does not need an immediate response and can check back later for the results.


In general, what is the differnce between Horizontal and Vertical Scaling? Which one is more commonly used for APIs and why?
  - Horizontal Scaling (Scaling Out): Involves adding more instances of the API server to distribute the load. 
    - This is typically done using a load balancer to route incoming requests to multiple servers. 
    - It allows for better fault tolerance and can handle a larger number of concurrent requests.    
    - For example, if you have an API running on a single server and you start receiving more traffic than it can handle, you can add more servers to the pool and use a load balancer to distribute the traffic across those servers.
  - Vertical Scaling (Scaling Up): Involves increasing the resources (CPU, memory) of the existing server to handle more requests.
    - This can be limited by the maximum capacity of the server and may lead to downtime during scaling.
    - For example, if you have an API running on a server with 4 CPU cores and 16 GB of RAM, and you start receiving more traffic than it can handle, you can upgrade the server to one with 8 CPU cores and 32 GB of RAM to improve its capacity.

  Usually Horizontal Scaling is more commonly used for APIs because it provides better fault tolerance and can handle a larger number of concurrent requests.

What is the difference between idempotent and non-idempotent HTTP methods? Why is it important to understand this distinction when designing APIs?
  - Idempotent HTTP methods are those that can be called multiple times without changing the result beyond the initial application. Examples include GET, PUT, PATCH, and DELETE.
  - Non-idempotent HTTP methods are those that can produce different results when called multiple times. Examples include POST.
  - Understanding this distinction is important because it affects how clients interact with the API and how the server handles requests. Idempotent methods can be safely retried, while non-idempotent methods should be used with caution.
  
What are decorators? Why are they important in Python? What are some common use cases for decorators in Python?
  - Decorators are a powerful feature in Python that allow you to modify the behavior of a function or class without changing its source code. 
  - They are important because they enable code reuse, separation of concerns, and can help keep your code clean and DRY (Don't Repeat Yourself).
  - Common use cases for decorators include:
    - API route definitions (e.g., @app.get(), @app.post() in FastAPI)
      - They allow you to easily define the HTTP method and route for an API endpoint.

Explain me in simple terms how decorators play are in API? And how exactly do we use the same class/function for multiple API endpoints using decorators?
  - In the context of APIs, decorators are used to define the routes and HTTP methods for your API endpoints. 
    - For example, in FastAPI, you can use decorators like @app.get() or @app.post() to specify that a particular function should handle GET or POST requests to a specific URL path.
    - Even though they perform different operations (e.g., GET for retrieving data, POST for creating data), you can use the same underlying function or class to handle both types of requests by applying different decorators to it.
    - But the question is how can we use the same function for multiple endpoints?
      - You can define a function that contains the core logic for handling the request, and then apply different decorators to it to create multiple endpoints.
      - For example you can have a standalone function that checks the authentication and authorization logic across all endpoints (different endpoints for different resources) and then you can use that function as a dependency in all your API endpoints using the Depends() function in FastAPI.

Are there any other important concepts related to API design that I should be aware of apart from the ones we've discussed?
  - Error Handling: Properly handling errors and returning meaningful error messages with appropriate HTTP status codes is crucial for a good API design.
  - Versioning: Implementing API versioning allows you to make changes to your API without breaking existing clients. This can be done through URL versioning (e.g., /api/v1/segments) or header versioning.
  - Documentation: Providing clear and comprehensive documentation (e.g., using OpenAPI/Swagger) helps developers understand how to use your API effectively.
  - Security: Implementing security best practices (e.g., authentication, authorization, input validation) is essential to protect your API and the data it handles.
  
  
# =============================================================================
# PART 1: FASTAPI — FULL EXAMPLE
# =============================================================================

FASTAPI IS THE INTERVIEW STANDARD FOR PYTHON APIs.



Is Fast API a REST API framework? What are the advantages of using FastAPI for building APIs?
  - Yes, FastAPI is a REST API framework.
  - It provides automatic generation of OpenAPI/Swagger documentation.
  - It leverages Python's type hints for validation and editor support.
  - It offers high performance with async support.

What is OpenAPI/Swagger documentation? Why is it important for APIs?
  - OpenAPI (formerly Swagger) is a specification for building APIs that includes a standard way to describe the structure of your API, including endpoints, request/response formats, and authentication methods.
  - Swagger UI is a tool that automatically generates interactive API documentation based on the OpenAPI specification. It allows developers to explore and test API endpoints directly from the documentation.
  - Having OpenAPI/Swagger documentation is important because it provides a clear and standardized way for developers to understand how to use your API, what endpoints are available, what parameters are required, and what responses to expect. It also facilitates easier integration with client applications and can improve developer experience.

  - So with FastAPI, you get automatic generation of OpenAPI/Swagger documentation, which means that as you define your API endpoints and their parameters using FastAPI's decorators and type hints, the documentation is automatically created and updated. This makes it easier for developers to understand and use your API without needing to manually write documentation.

What is hinting in Python in simple terms? How does FastAPI leverage type hints for validation and editor support?
  - Type hinting in Python is a way to indicate the expected data types of variables, function parameters, and return values. So it is a way to provide additional information about the types of data that your code is working with.
    - Does this help the developer to write better code? Yes, it does. It can help catch type-related errors during development and improve code readability.
    - So essentially the schema of underlying data is defined using type hints, which allows for better validation and editor support. This way we make sure API is developed with the correct data types and it also helps the developers to understand what kind of data they should be sending in the request and what kind of data they can expect in the response.
  - FastAPI leverages type hints to automatically validate incoming request data and generate API documentation. When you define an API endpoint with FastAPI, you can use type hints to specify the expected types of query parameters, request bodies, and response models. FastAPI will then use this information to validate incoming requests and ensure that they conform to the specified types. Additionally, the type hints are used to generate accurate OpenAPI/Swagger documentation, which helps developers understand how to interact with the API.  

What is FastAPI? And why do we use it?
  - FastAPI is a modern, fast (high-performance) web framework for building APIs.
  - FastAPI is designed to be easy to use, with automatic generation of OpenAPI/Swagger documentation, and it leverages Python's type hints for validation and editor support.
  - It is ideal for building data products and ML model serving APIs due to its speed, ease of development, and robust features.

The core functionality of FastAPI includes:
  - Defining API endpoints (endpoints means routes which are the URLs for the API, you can hit and get the response data) with Python functions and decorators (decorators are a way to modify the behavior of a function or class. 
    - In FastAPI, we use decorators like @app.get(), @app.post() to define API routes and their HTTP methods.
    
KEY FEATURES:
  - Auto-generated OpenAPI/Swagger docs
  - Async support (uvicorn + asyncio)
  - Request/Response validation via Pydantic
  - Dependency injection (auth, DB sessions, rate limiting)
  - Type hints → automatic validation/docs
"""

# =============================================================================
# PART 2: REST API DESIGN PRINCIPLES
# =============================================================================

"""
HTTP VERBS & MEANING:
  GET    → Read (safe, idempotent): /api/v1/customers/123
  POST   → Create (non-idempotent): /api/v1/customers --> created duplicates if called multiple times
  PUT    → Replace (idempotent): PUT /api/v1/customers/123
  PATCH  → Partial update (idempotent): PATCH /api/v1/customers/123
  DELETE → Remove (idempotent): DELETE /api/v1/customers/123

Except for POST , all other HTTP methods are idempotent, meaning that making the same request multiple times will have the same effect as making it once.  
  
STATUS CODE QUICK REFERENCE:
  200 OK           → Successful GET, PUT, PATCH
  201 Created      → Successful POST
  202 Accepted     → Async job started (background task)
  204 No Content   → Successful DELETE
  400 Bad Request  → Malformed request body
  401 Unauthorized → Missing/invalid auth
  403 Forbidden    → Auth valid but insufficient permissions
  404 Not Found    → Resource doesn't exist
  422 Unprocessable → Pydantic validation failure
  429 Too Many Requests → Rate limit exceeded
  500 Server Error → Unhandled exception

PAGINATION:
  - Offset-based: GET /items?offset=0&limit=20 (issues with concurrent writes)
  - Cursor-based: GET /items?cursor=abc123&limit=20 (stable, preferred)
  - Keyset pagination: GET /items?after_id=100&limit=20 (efficient with index)

VERSIONING:
  - URL path: /api/v1/segments (most common)
  - Header: Accept: application/vnd.company.v1+json
  - Query param: /api/segments?version=1
"""


# =============================================================================
# PART 3: AUTHENTICATION & AUTHORIZATION
# =============================================================================

"""
JWT STRUCTURE: header.payload.signature
  - Header: {"alg": "HS256", "typ": "JWT"}
  - Payload: {"sub": "user123", "role": "admin", "iat": 1700000000, "exp": 1700086400}
  - Signature: HMACSHA256(base64(header) + "." + base64(payload), secret)

OAUTH 2.0 FLOWS:
  - Authorization Code: Web apps (most secure)
  - Client Credentials: Server-to-server (machine accounts)
  - Implicit: SPA apps (deprecated, use PKCE instead)
  - Device Code: CLI/TV devices

FASTAPI AUTH:
  from fastapi.security import HTTPBearer
  - Extracts Bearer token from Authorization header
  - Can wrap with custom JWT validation
"""


# =============================================================================
# PART 5: KUBERNETES KEY CONCEPTS
# =============================================================================

"""
K8S OBJECTS:
  - Pod: Smallest deployable unit (1+ containers)
  - Deployment: Desired state (replicas, strategy, image)
  - Service: Stable network endpoint to a set of pods
    - ClusterIP: Internal only (default)
    - NodePort: Expose on each node's IP
    - LoadBalancer: Cloud LB provisioned
  - ConfigMap: Non-sensitive config (env vars, files)
  - Secret: Sensitive data (base64 encoded, use external secrets manager in prod)
  - Ingress: HTTP/HTTPS routing to services
  - Namespace: Logical isolation for environments

HPA (Horizontal Pod Autoscaler):
  apiVersion: autoscaling/v2
  kind: HorizontalPodAutoscaler
  spec:
    scaleTargetRef:
      apiVersion: apps/v1
      kind: Deployment
      name: data-api
    minReplicas: 2
    maxReplicas: 10
    metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70

PROBES:
  - Liveness: Is the container alive? Restart if fails.
  - Readiness: Is the container ready to serve traffic? Remove from Service if fails.
  - Startup: For slow-starting apps. Disables liveness until succeeds.
"""


# =============================================================================
# PART 6: CI/CD PIPELINE
# =============================================================================

"""
=== .github/workflows/deploy.yml ===
name: Deploy Data API
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest tests/ --cov=app --cov-fail-under=80
  
  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker image
        run: docker build -t data-api:${{ github.sha }} .
      
      - name: Push to ECR
        run: |
          aws ecr get-login-password | docker login --username AWS --password-stdin ${{ secrets.AWS_ACCOUNT }}.dkr.ecr.${{ secrets.AWS_REGION }}.amazonaws.com
          docker tag data-api:${{ github.sha }} ${{ secrets.ECR_REPO }}:${{ github.sha }}
          docker push ${{ secrets.ECR_REPO }}:${{ github.sha }}
      
      - name: Deploy to EKS
        run: |
          aws eks update-kubeconfig --region ${{ secrets.AWS_REGION }} --name data-platform
          kubectl set image deployment/data-api api=${{ secrets.ECR_REPO }}:${{ github.sha }}
          kubectl rollout status deployment/data-api

TESTING IN DATA PIPELINES:
  - Unit tests: pytest with small sample DataFrames (100 rows)
  - Integration tests: test against actual DB/Kafka
  - dbt tests: test SQL transformations (not null, unique, referential)
  - Great Expectations: validate data quality at pipeline stages
"""


# =============================================================================
# PART 7: MLOps — MLflow
# =============================================================================

"""
MLFLOW COMPONENTS:
  - Tracking: Log params, metrics, artifacts per run
  - Model Registry: Version models, promote stages (Staging → Production)
  - Model Serving: Deploy models as REST API
  - Projects: Package ML code for reproducibility

MODEL PROMOTION:
  1. Run experiments → compare in MLflow UI
  2. Register best model → version 1
  3. Move to Staging → validate in staging environment
  4. Move to Production → serve real traffic
  5. Monitor → rollback if performance degrades
"""


# =============================================================================
# PART 8: FEATURE STORES & MODEL DEPLOYMENT
# =============================================================================

"""
FEATURE STORE CONCEPTS:
  - Online store: Low-latency feature serving (Redis, DynamoDB)
  - Offline store: Batch feature computation (S3, Delta, Parquet)
  - Point-in-time correct joins: Ensure training data doesn't include future info
  - Feature serving: Get features at inference time
  
  Example: Customer churn prediction
  - Offline: compute features daily in Spark → store in Feast offline store
  - Online: at prediction time, fetch features via Feast API
  - Point-in-time: for training, join features as they existed on that date

MODEL DEPLOYMENT PATTERNS:
  - Batch inference: Score all customers daily, write predictions to Delta
    - Best for: Non-urgent decisions, large-scale scoring
  - Real-time inference: API endpoint calls model in memory
    - Best for: Fraud detection, recommendation (low-latency)
  - Shadow mode: New model runs in parallel but doesn't serve results
    - Safe way to test new model in production
  - Canary: Gradual rollout (5% → 20% → 100%)
    - Minimize blast radius of bad model
  - A/B testing: Route % traffic to each model variant
    - Compare performance metrics

MODEL MONITORING:
  1. Data drift: input distribution changes over time
     - Detect via: KS-test, Population Stability Index (PSI)
  2. Prediction drift: model output distribution changes
     - Detect via: track prediction mean/median over time
  3. Model degradation: accuracy drops over time
     - Requires ground truth labels (delayed feedback)
"""


# =============================================================================
# PART 9: OBSERVABILITY — Three Pillars
# =============================================================================

"""
1. METRICS (Prometheus + Grafana):
   - Track: request_count, latency_p99, error_rate, throughput
   - Custom: pipeline_row_count, data_latency, file_age
  
2. LOGGING (ELK/CloudWatch):
   - Structured JSON logs: {"timestamp": "...", "level": "ERROR", "pipeline": "orders", "error": "..."}
   - Log levels: DEBUG < INFO < WARNING < ERROR < CRITICAL
   - Centralized: ship all logs to a single searchable store
  
3. TRACING (OpenTelemetry + Jaeger):
   - Trace a single request across multiple services
   - Span: unit of work within a trace
   - Key for microservices: understand which service is slow/failing

FASTAPI METRICS EXAMPLE:
  from prometheus_fastapi_instrumentator import Instrumentator
  
  app = FastAPI()
  Instrumentator().instrument(app).expose(app)
  
  # Auto-provides: /metrics endpoint with:
  # - http_requests_total (counter by method, endpoint, status)
  # - http_request_duration_seconds (histogram)
  # - http_request_size_bytes (summary)
"""

print("=== END OF DAY 3 — APP ENGINEERING + MLOps ===")
