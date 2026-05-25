# DAY 3 — Application Engineering + MLOps

> **Interview:** 26 May 2026
>
> **Topics:** FastAPI, REST Design, Auth, Docker, Kubernetes, CI/CD, MLflow, Feature Stores, Model Deployment, Observability

---

## Table of Contents

1. [API Fundamentals](#1-api-fundamentals)
   - 1.1 [What is an API & Why for Data Products](#11-what-is-an-api--why-for-data-products)
   - 1.2 [API Types — REST vs GraphQL vs gRPC](#12-api-types--rest-vs-graphql-vs-grpc)
   - 1.3 [Stateless Nature of REST](#13-stateless-nature-of-rest)
   - 1.4 [API Request Parameters](#14-api-request-parameters)
   - 1.5 [Bearer Tokens & API Authentication](#15-bearer-tokens--api-authentication)
   - 1.6 [API Key vs Bearer Token](#16-api-key-vs-bearer-token)
   - 1.7 [REST API Components (Endpoint, Methods, Body, Response, Status Codes)](#17-rest-api-components)
   - 1.8 [Resources in REST](#18-resources-in-rest)
   - 1.9 [API-Backend Interaction Flow](#19-api-backend-interaction-flow)
   - 1.10 [HTTP Methods — POST, PUT, PATCH, GET, DELETE](#110-http-methods)
   - 1.11 [API Hosting & Scaling](#111-api-hosting--scaling)
   - 1.12 [Synchronous vs Asynchronous APIs](#112-synchronous-vs-asynchronous-apis)
   - 1.13 [Horizontal vs Vertical Scaling](#113-horizontal-vs-vertical-scaling)
   - 1.14 [Idempotent vs Non-Idempotent Methods](#114-idempotent-vs-non-idempotent-methods)
   - 1.15 [Python Decorators in APIs](#115-python-decorators-in-apis)
   - 1.16 [Additional API Design Concepts](#116-additional-api-design-concepts)
2. [FastAPI — Full Example](#2-fastapi--full-example)
   - 2.1 [Is FastAPI a REST Framework? Advantages](#21-is-fastapi-a-rest-framework-advantages)
   - 2.2 [OpenAPI/Swagger Documentation](#22-openapiswagger-documentation)
   - 2.3 [Type Hinting in Python & FastAPI](#23-type-hinting-in-python--fastapi)
3. [REST API Design Principles](#3-rest-api-design-principles)
   - 3.1 [HTTP Verbs Quick Reference](#31-http-verbs-quick-reference)
   - 3.2 [Status Code Quick Reference](#32-status-code-quick-reference)
   - 3.3 [Pagination Strategies](#33-pagination-strategies)
   - 3.4 [API Versioning](#34-api-versioning)
4. [Authentication & Authorization](#4-authentication--authorization)
   - 4.1 [JWT Structure](#41-jwt-structure)
   - 4.2 [OAuth 2.0 Flows](#42-oauth-20-flows)
   - 4.3 [FastAPI Auth Implementation](#43-fastapi-auth-implementation)
5. [Containerization & Docker](#5-containerization--docker)
   - 5.1 [Docker Fundamentals](#51-docker-fundamentals)
   - 5.2 [Key Docker Concepts](#52-key-docker-concepts)
   - 5.3 [Docker in DE & GenAI](#53-docker-in-de--genai)
6. [Kubernetes (K8s) — Orchestration](#6-kubernetes-k8s--orchestration)
   - 6.1 [Kubernetes Fundamentals](#61-kubernetes-fundamentals)
   - 6.2 [K8s Objects Reference](#62-k8s-objects-reference)
   - 6.3 [Horizontal Pod Autoscaler (HPA)](#63-horizontal-pod-autoscaler-hpa)
   - 6.4 [Probes — Liveness, Readiness, Startup](#64-probes--liveness-readiness-startup)
   - 6.5 [K8s in DE & GenAI](#65-k8s-in-de--genai)
7. [CI/CD Pipeline](#7-cicd-pipeline)
   - 7.1 [CI/CD Fundamentals](#71-cicd-fundamentals)
   - 7.2 [Sample GitHub Actions Workflow](#72-sample-github-actions-workflow)
   - 7.3 [Testing in Data Pipelines](#73-testing-in-data-pipelines)
8. [CAP Theorem](#8-cap-theorem)
   - 8.1 [CAP Theorem Fundamentals](#81-cap-theorem-fundamentals)
   - 8.2 [CAP in Practice — Database Choices](#82-cap-in-practice--database-choices)
   - 8.3 [Interview Take on CAP](#83-interview-take-on-cap)
9. [MLOps — MLflow](#9-mlops--mlflow)
   - 9.1 [MLOps Fundamentals](#91-mlops-fundamentals)
   - 9.2 [MLflow Components](#92-mlflow-components)
   - 9.3 [Model Promotion Workflow](#93-model-promotion-workflow)
10. [Feature Stores & Model Deployment](#10-feature-stores--model-deployment)
    - 10.1 [Feature Store Fundamentals](#101-feature-store-fundamentals)
    - 10.2 [Feature Store Concepts](#102-feature-store-concepts)
    - 10.3 [Model Deployment Patterns](#103-model-deployment-patterns)
    - 10.4 [Model Monitoring — Drift & Degradation](#104-model-monitoring--drift--degradation)
11. [Observability — Three Pillars](#11-observability--three-pillars)
    - 11.1 [Observability Fundamentals](#111-observability-fundamentals)
    - 11.2 [Metrics (Prometheus + Grafana)](#112-metrics-prometheus--grafana)
    - 11.3 [Logging (ELK / CloudWatch)](#113-logging-elk--cloudwatch)
    - 11.4 [Tracing (OpenTelemetry + Jaeger)](#114-tracing-opentelemetry--jaeger)
    - 11.5 [FastAPI Metrics Example](#115-fastapi-metrics-example)
12. [Microservices Architecture](#12-microservices-architecture)
    - 12.1 [Microservices Fundamentals](#121-microservices-fundamentals)
    - 12.2 [Monolith vs Microservices](#122-monolith-vs-microservices)
    - 12.3 [Microservices in DE & GenAI](#123-microservices-in-de--genai)

---

# 1. API Fundamentals

## 1.1 What is an API & Why for Data Products

> **API (Application Programming Interface)** is a set of rules and protocols that allows different software applications to communicate with each other.

**Why APIs for data products?**
- **Standardized access** — clients (frontend apps, other services) interact with backend data/logic through a uniform interface
- **Decoupling** — frontend and backend can evolve independently
- **Security** — APIs implement auth, authorization, and input validation (direct DB access exposes data)
- **Abstraction** — backend can switch databases, optimize queries, or change data models without breaking clients
- **Multi-client support** — one API serves mobile app, web app, and third-party integrations

**Why not let frontend access the database directly?**

| Direct DB Access | API Layer |
|-----------------|-----------|
| Exposes sensitive data | Authentication & authorization enforced |
| Tight coupling — DB changes break frontend | Abstraction — backend changes invisible to clients |
| No rate limiting — abuse possible | Rate limiting, throttling, monitoring |
| Security vulnerabilities exposed | Input validation, sanitization |

> **Summary:** APIs are the **standard, secure, and scalable** way to access data products. Direct DB access is a security and maintainability risk.

---

## 1.2 API Types — REST vs GraphQL vs gRPC

| Type | Description | Best For |
|------|-------------|----------|
| **REST** | Architectural style using standard HTTP methods (GET, POST, PUT, DELETE) and stateless communication | **Most common for data products** — simple, scalable, broad support |
| **GraphQL** | Query language allowing clients to request exactly the data they need — reduces over/under-fetching | Flexible data queries, complex nested relationships |
| **gRPC** | High-performance RPC framework using Protocol Buffers for serialization | Low-latency, high-throughput microservice communication |

> **REST is the default for data products** due to simplicity, wide adoption, and easy integration. HTTP methods and status codes are universal — every developer understands them.

---

## 1.3 Stateless Nature of REST

**Q: What is statelessness in REST APIs? Why is it important?**

> **Statelessness** means each API request must contain **all information** needed to understand and process it. The server does **not** store any session information between requests.

**Why it matters:**
- **Horizontal scaling** — no session data to synchronize across servers, just add more instances behind a load balancer
- **Reliability** — failure in one request doesn't affect others; any server can handle any request
- **Simplicity** — server doesn't need to manage session state

> **Key insight:** REST APIs have **no memory** of previous requests. Each request is independent and self-contained.

---

## 1.4 API Request Parameters

**Q: What parameters are sent in an API request? How does the DB know which record to fetch?**

| Parameter Type | Description | Example |
|----------------|-------------|---------|
| **Path Parameters** | Part of the URL — identifies a specific resource | `GET /api/v1/segments/`**`123`** → fetches segment with ID 123 |
| **Query Parameters** | Key-value pairs after `?` — filter/sort results | `GET /api/v1/segments?`**`customer_id=456&country=US`** |
| **Headers** | Metadata about the request — auth tokens, content type | `Authorization: Bearer <token>` ; `Content-Type: application/json` |
| **Request Body** | Data sent by client (for POST/PUT requests) | JSON: `{"customer_id": 456, "country": "US"}` |

**How the DB knows which record:**
1. API extracts identifiers from path or query params
2. Validates the parameters (format, type)
3. Constructs a database query using those identifiers (e.g., `SELECT * FROM segments WHERE id = 123`)
4. Returns the result

---

## 1.5 Bearer Tokens & API Authentication

**Q: What is a bearer token?**

> A **bearer token** is an access token where the client must "bear" (carry) it to access protected resources. It's included in the `Authorization` header: `Authorization: Bearer <token>`

**Key authentication terms:**

| Term | Description |
|------|-------------|
| **Bearer Token** | Access token in `Authorization: Bearer <token>` header |
| **JWT** (JSON Web Token) | Compact, URL-safe token format containing claims (user ID, role, permissions) |
| **OAuth 2.0** | Authorization framework for third-party access on behalf of a user |
| **API Key** | Simple static token for client identification |
| **Authentication** | Verifying **who** the client is |
| **Authorization** | Verifying **what** the client is allowed to do (based on claims in token) |
| **Claims** | Information inside a token (user ID, role, permissions) used for authorization decisions |

---

## 1.6 API Key vs Bearer Token

| Aspect | **API Key** | **Bearer Token** |
|--------|-------------|------------------|
| **Type** | Static, simple token | Dynamic, generated by auth server |
| **Contains** | Just an identifier | Claims about user/permissions |
| **Expiry** | Typically long-lived | Short-lived with refresh tokens |
| **Use case** | Simple client identification | User authentication with permissions |

---

## 1.7 REST API Components

**Q: What are the components of a REST API?**

| Component | Description | Example |
|-----------|-------------|---------|
| **Endpoint** | URL representing a resource or action | `GET /api/v1/segments/{customer_id}` |
| **HTTP Method** | Type of operation (GET, POST, PUT, PATCH, DELETE) | `POST /api/v1/segments/compute` |
| **Request Body** | Data sent by client (POST/PUT) | `{"customer_id": 456, "country": "US"}` |
| **Response** | Data returned by server (usually JSON) | `{"segment_id": 1, "segment_name": "High Value"}` |
| **Status Code** | Result indicator of the request | `200 OK`, `404 Not Found`, `422 Unprocessable Entity` |

---

## 1.8 Resources in REST

**Q: What does "resource" mean in REST? How to identify them in a data product?**

> A **resource** is an object or data representation that can be accessed/manipulated via the API. Resources are identified by unique URLs (endpoints).

**In a customer segmentation data product:**
| Resource | Endpoint |
|----------|----------|
| **Customer** | `/api/v1/customers/{customer_id}` |
| **Segment** | `/api/v1/segments/{segment_id}` |
| **Computation Job** | `/api/v1/segments/compute` |

---

## 1.9 API-Backend Interaction Flow

**Q: How does an API interact with the backend database?**

> Think of the API as a **waiter in a restaurant**: the client places an order (API request), the waiter takes it to the kitchen (backend), the kitchen prepares the food (processes data), and the waiter brings it back (API response).

**Step-by-step flow:**
1. **Validate** request parameters and body
2. **Authenticate & authorize** — ensure client has permission
3. **Query backend** — e.g., SQL query on Postgres or data access layer on Delta Lake
4. **Process data** — apply business logic, format response, update/delete records
5. **Return response** — JSON data or status message

**Example:** `GET /api/v1/segments/{customer_id}`
- Extract `customer_id` from URL → validate format → query DB: `SELECT * FROM segments WHERE customer_id = 456` → format as JSON → return

---

## 1.10 HTTP Methods

| Method | Action | Idempotent? | DB Analogy | Behavior on Repeat |
|--------|--------|-------------|------------|-------------------|
| **POST** | Create | **No** | `INSERT` | Creates duplicate records |
| **PUT** | Replace/Create | **Yes** | `UPDATE` (or INSERT if not exists) | Same effect — no duplicates |
| **PATCH** | Partial Update | **Yes** | `UPDATE specific fields` | Same effect — updates same fields |
| **GET** | Read | **Yes** (safe) | `SELECT` | Returns same data — no modification |
| **DELETE** | Remove | **Yes** | `DELETE` | Deletes same record — no issue |

> **Idempotent** = calling multiple times produces the **same result** as calling once. Safe to retry. POST is **not** idempotent — retrying may create duplicates.

---

## 1.11 API Hosting & Scaling

**Q: Where is an API hosted and how does it scale?**

APIs are hosted on:
- **Web servers** — Nginx, Apache
- **Cloud platforms** — AWS (EC2, ECS, Lambda), Azure, GCP

**Scaling techniques:**
| Technique | Description |
|-----------|-------------|
| **Horizontal Scaling** | Add more API server instances behind a load balancer |
| **Vertical Scaling** | Increase CPU/memory of existing server |
| **Caching** | In-memory caches (Redis) reduce backend load for frequent data |
| **Rate Limiting** | Prevent abuse, ensure fair usage |

---

## 1.12 Synchronous vs Asynchronous APIs

| Aspect | **Synchronous** | **Asynchronous** |
|--------|-----------------|------------------|
| **Behavior** | Client blocks until response received | Client continues working; response comes later |
| **Use case** | Simple CRUD — needs immediate response | Long-running operations (ML training, data processing) |
| **Example** | Form submission, data retrieval | Submit job → receive job ID → poll for results later |

---

## 1.13 Horizontal vs Vertical Scaling

| Aspect | **Horizontal (Scaling Out)** | **Vertical (Scaling Up)** |
|--------|------------------------------|---------------------------|
| **How** | Add more server instances | Increase CPU/RAM of existing server |
| **Fault tolerance** | ✅ High — one server fails, others continue | ❌ Low — single point of failure |
| **Limit** | Theoretically unlimited | Physical capacity of the machine |
| **Downtime** | Zero-downtime (add instances live) | May require downtime |
| **Common for APIs?** | **✅ Yes** — de facto standard | ❌ No |

> **Horizontal scaling is preferred for APIs** because it provides fault tolerance and handles more concurrent requests. Load balancers distribute traffic across instances.

---

## 1.14 Idempotent vs Non-Idempotent Methods

| Type | Methods | Can Retry Safely? |
|------|---------|-------------------|
| **Idempotent** | GET, PUT, PATCH, DELETE | ✅ Yes — same result every time |
| **Non-idempotent** | POST | ❌ No — may create duplicates |

> **Design implication:** Clients can safely retry idempotent requests on network failure. POST requests need idempotency keys or deduplication logic.

---

## 1.15 Python Decorators in APIs

**Q: What are decorators? How are they used in APIs?**

> **Decorators** modify the behavior of a function/class without changing its source code. They enable **code reuse** and **separation of concerns**.

**In FastAPI:** Decorators define routes and HTTP methods:
```python
@app.get("/api/v1/segments/{customer_id}")
def get_segments(customer_id: int):
    # logic here
    return {"customer_id": customer_id}

@app.post("/api/v1/segments/compute")
def compute_segments(payload: SegmentRequest):
    # logic here
    return {"status": "processing"}
```

**Reusing logic across endpoints:** Use FastAPI's **dependency injection** (`Depends()`):
```python
from fastapi import Depends

async def verify_token(auth: str = Header(...)):
    # validate JWT, return user info
    return user

@app.get("/api/v1/segments")
async def get_segments(user = Depends(verify_token)):
    # user is now authenticated — no need to repeat auth logic
    return {"user": user.id, "segments": [...]}
```

---

## 1.16 Additional API Design Concepts

| Concept | Description |
|---------|-------------|
| **Error Handling** | Return meaningful error messages with appropriate HTTP status codes |
| **Versioning** | `/api/v1/segments` — allows changes without breaking existing clients |
| **Documentation** | OpenAPI/Swagger — auto-generated, interactive API docs |
| **Security** | Auth, authorization, input validation, rate limiting |

---

# 2. FastAPI — Full Example

## 2.1 Is FastAPI a REST Framework? Advantages

> **Yes, FastAPI is a modern REST API framework for Python.** It's the **interview standard** for Python-based data product APIs.

**Advantages:**
| Feature | Benefit |
|---------|---------|
| Auto-generated OpenAPI/Swagger docs | Documentation is automatic, always in sync |
| Python type hints | Request validation + editor autocomplete |
| Async support (uvicorn + asyncio) | High performance, non-blocking I/O |
| Pydantic models | Request/response validation |
| Dependency injection | Auth, DB sessions, rate limiting — reusable across endpoints |

---

## 2.2 OpenAPI/Swagger Documentation

> **OpenAPI** (formerly Swagger) is a specification for describing API structure — endpoints, request/response formats, authentication methods.

**Swagger UI** automatically generates interactive API documentation from the OpenAPI spec. Developers can explore and **test endpoints directly** from the browser.

> **Key point:** FastAPI auto-generates this — as you define endpoints with decorators and type hints, the docs stay **automatically updated**. No manual documentation needed.

---

## 2.3 Type Hinting in Python & FastAPI

**Q: What is type hinting? How does FastAPI use it?**

> **Type hints** indicate expected data types for variables, function parameters, and return values. They catch type-related errors during development and improve code readability.

**FastAPI leverages type hints to:**
1. **Validate** incoming request data against specified types
2. **Generate** accurate OpenAPI/Swagger documentation
3. **Provide** editor support (autocomplete, type checking)

```python
from pydantic import BaseModel

class SegmentRequest(BaseModel):
    customer_id: int        # type hint → FastAPI validates this is an int
    country: str            # type hint → validates this is a string
    as_of_date: str         # type hint → validates format

@app.post("/api/v1/segments/compute")
def compute(payload: SegmentRequest):  # FastAPI auto-validates the body
    return {"customer_id": payload.customer_id}
```

---

# 3. REST API Design Principles

## 3.1 HTTP Verbs Quick Reference

| Verb | Action | Idempotent? | URL Example |
|------|--------|-------------|-------------|
| **GET** | Read | ✅ Yes (safe) | `GET /api/v1/customers/123` |
| **POST** | Create | ❌ No | `POST /api/v1/customers` |
| **PUT** | Replace | ✅ Yes | `PUT /api/v1/customers/123` |
| **PATCH** | Partial update | ✅ Yes | `PATCH /api/v1/customers/123` |
| **DELETE** | Remove | ✅ Yes | `DELETE /api/v1/customers/123` |

> **Rule:** All HTTP methods except POST are idempotent — same request multiple times = same effect as once.

## 3.2 Status Code Quick Reference

| Code | Meaning | When |
|------|---------|------|
| **200** OK | Successful GET, PUT, PATCH | Data returned |
| **201** Created | Successful POST | Resource created |
| **202** Accepted | Async job started | Background task |
| **204** No Content | Successful DELETE | Resource removed |
| **400** Bad Request | Malformed request body | Client error |
| **401** Unauthorized | Missing/invalid auth | No token |
| **403** Forbidden | Valid auth but insufficient permissions | Access denied |
| **404** Not Found | Resource doesn't exist | Wrong ID |
| **422** Unprocessable | Pydantic validation failure | Wrong data type |
| **429** Too Many Requests | Rate limit exceeded | Back off |
| **500** Server Error | Unhandled exception | Bug |

## 3.3 Pagination Strategies

| Strategy | How It Works | Best For |
|----------|-------------|----------|
| **Offset-based** | `GET /items?offset=0&limit=20` | Simple, but issues with concurrent writes (duplicate/skip) |
| **Cursor-based** | `GET /items?cursor=abc123&limit=20` | **Preferred** — stable pagination |
| **Keyset** | `GET /items?after_id=100&limit=20` | Efficient with indexed primary key |

> **Cursor-based pagination** is preferred because it handles concurrent writes gracefully — new records don't shift the page boundaries.

## 3.4 API Versioning

| Method | Example | Notes |
|--------|---------|-------|
| **URL path** | `/api/v1/segments` | **Most common** — clear, simple |
| **Header** | `Accept: application/vnd.company.v1+json` | Clean URLs, harder to test |
| **Query param** | `/api/segments?version=1` | Simple but clutters URLs |

> **Best practice:** URL path versioning (`/api/v1/`) — it's explicit, cacheable, and easy to route.

---

# 4. Authentication & Authorization

## 4.1 JWT Structure

> **JWT (JSON Web Token)** — format: `header.payload.signature`

| Part | Content | Example |
|------|---------|---------|
| **Header** | Algorithm & token type | `{"alg": "HS256", "typ": "JWT"}` |
| **Payload** | Claims (user info, permissions, expiry) | `{"sub": "user123", "role": "admin", "iat": 1700000000, "exp": 1700086400}` |
| **Signature** | Verifies token wasn't tampered with | `HMACSHA256(base64(header) + "." + base64(payload), secret)` |

---

## 4.2 OAuth 2.0 Flows

| Flow | Use Case |
|------|----------|
| **Authorization Code** | Web apps — **most secure** (uses redirect + auth code) |
| **Client Credentials** | Server-to-server (machine accounts, no user involved) |
| **Implicit** | SPA apps (**deprecated** — use PKCE instead) |
| **Device Code** | CLI/TV devices with limited input capability |

---

## 4.3 FastAPI Auth Implementation

```python
from fastapi.security import HTTPBearer

security = HTTPBearer()  # Extracts Bearer token from Authorization header

@app.get("/api/v1/segments")
async def get_segments(token = Depends(security)):
    # Custom JWT validation here
    # token.credentials contains the JWT string
    user = validate_jwt(token.credentials)
    return {"user": user.id}
```

---

# 5. Containerization & Docker

## 5.1 Docker Fundamentals

> **What is Docker?** A platform for packaging applications and their dependencies into **containers** — lightweight, portable, isolated environments that run consistently across any system.

**The problem Docker solves:** *"It works on my machine"* — applications behave differently across developer laptops, testing servers, and production due to different OS, library versions, and configurations.

**How it works:**
| Concept | Description |
|---------|-------------|
| **Image** | A read-only template with the app + all dependencies (OS, libraries, code) |
| **Container** | A running instance of an image |
| **Dockerfile** | Recipe that defines how to build the image |
| **Registry** | Repository for storing/publishing images (Docker Hub, ECR, ACR) |

**Why Docker matters for data engineering & GenAI:**
- **Reproducibility** — Spark jobs, ML training, API servers all run identically in dev/test/prod
- **Isolation** — different projects can use conflicting library versions on the same machine
- **Portability** — same container runs on laptop, on-prem server, or cloud (ECS, EKS, AKS)
- **Microservices** — each service (API, model server, data pipeline) runs in its own container

---

## 5.2 Key Docker Concepts

| Concept | Description |
|---------|-------------|
| **Dockerfile** | Instructions to build an image (FROM, RUN, COPY, CMD) |
| **Image** | Immutable snapshot (OS + app + dependencies) |
| **Container** | Running instance of an image (has its own filesystem, network) |
| **Volume** | Persistent storage that survives container restarts |
| **Network** | Connects containers to each other and the outside world |
| **docker-compose** | Define and run multi-container applications |

**Sample Dockerfile for a FastAPI app:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

---

## 5.3 Docker in DE & GenAI

| Use Case | How Docker Helps |
|----------|-----------------|
| **Spark jobs** | Package PySpark + dependencies in container; run consistently on EMR or K8s |
| **ML model serving** | Containerize model + inference code; deploy as REST API |
| **Data pipelines** | Each pipeline stage (extract, transform, load) runs in isolated containers |
| **Development** | Local environment matches production exactly |

---

# 6. Kubernetes (K8s) — Orchestration

## 6.1 Kubernetes Fundamentals

> **What is Kubernetes?** An **orchestration platform** for automating deployment, scaling, and management of containerized applications.

**The problem Kubernetes solves:**
- Running a single container is easy (Docker). Running **100 containers** across **10 servers**, handling failures, scaling up/down, rolling updates, and networking — that's **hard**.
- K8s does this automatically.

**Key benefits:**
- **Auto-scaling** — automatically add/remove containers based on CPU/memory usage
- **Self-healing** — restart failed containers, replace unhealthy ones
- **Rolling updates** — update apps with zero downtime
- **Service discovery** — containers find each other automatically
- **Load balancing** — distribute traffic across containers

**Simple analogy:**
> Docker is like having individual shipping containers. **Kubernetes is the crane operator and logistics system** that decides where to place each container, what to do if one falls, and how to route cargo between them.

---

## 6.2 K8s Objects Reference

| Object | Description | Purpose |
|--------|-------------|---------|
| **Pod** | Smallest deployable unit (1+ containers) | Runs your application |
| **Deployment** | Declares desired state (replicas, strategy, image) | Manages pod lifecycle |
| **Service** | Stable network endpoint to a set of pods | Enables communication between services |
| **ConfigMap** | Non-sensitive configuration (env vars, files) | Decouples config from code |
| **Secret** | Sensitive data (base64 encoded — use external secrets manager in prod) | Passwords, API keys |
| **Ingress** | HTTP/HTTPS routing to services | External access to your app |
| **Namespace** | Logical isolation for environments | Separate dev/staging/prod |

**Service types:**
- **ClusterIP** — Internal only (default)
- **NodePort** — Expose on each node's IP
- **LoadBalancer** — Cloud LB provisioned automatically

---

## 6.3 Horizontal Pod Autoscaler (HPA)

> **HPA automatically scales the number of pods** based on CPU/memory utilization or custom metrics.

```yaml
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
```

> **What this does:** If the `data-api` deployment's CPU averages >70%, K8s adds more pods (up to 10). When usage drops, it scales down (minimum 2).

---

## 6.4 Probes — Liveness, Readiness, Startup

| Probe | Purpose | Failure Action |
|-------|---------|---------------|
| **Liveness** | Is the container alive? (not deadlocked/hung) | **Restart** the container |
| **Readiness** | Is the container ready to serve traffic? | **Remove from Service** (no traffic sent) |
| **Startup** | For slow-starting apps — disables liveness until succeeds | Delays other probes until app is ready |

---

## 6.5 K8s in DE & GenAI

| Use Case | How K8s Helps |
|----------|---------------|
| **Model serving at scale** | Deploy model API with HPA; scale based on inference request volume |
| **Data pipeline orchestration** | Run Spark jobs as K8s pods; auto-scale worker nodes |
| **Feature store serving** | Deploy Feast or similar with Service + HPA |
| **CI/CD target** | Deploy new container versions with rolling updates (zero downtime) |
| **Batch inference** | Run batch jobs as K8s Jobs/CronJobs |

---

# 7. CI/CD Pipeline

## 7.1 CI/CD Fundamentals

> **CI/CD (Continuous Integration / Continuous Deployment)** automates the process of testing and deploying code changes.

| Stage | What Happens | Problem Solved |
|-------|-------------|----------------|
| **CI (Continuous Integration)** | Code changes are automatically tested (unit tests, linting, type checks) | Catches bugs before they reach production |
| **CD (Continuous Deployment/Delivery)** | Tested code is automatically deployed to staging/production | Manual deployment is slow and error-prone |

**Why CI/CD matters for data engineering:**
- **Data pipelines** — test SQL transformations, PySpark jobs, dbt models before deploying
- **ML models** — validate model performance metrics as part of CI before promoting to production
- **APIs** — run integration tests against actual databases before deploying

---

## 7.2 Sample GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
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
```

**Flow:** `git push → run tests → build Docker image → push to ECR → deploy to EKS`

---

## 7.3 Testing in Data Pipelines

| Test Type | Tools | What It Tests |
|-----------|-------|---------------|
| **Unit tests** | `pytest` with small sample DataFrames (100 rows) | Individual transformation functions |
| **Integration tests** | Test against actual DB/Kafka | End-to-end pipeline correctness |
| **dbt tests** | `not null`, `unique`, `referential integrity` | SQL transformation quality |
| **Great Expectations** | Data quality validation | Row-level expectations at pipeline stages |

---

# 8. CAP Theorem

## 8.1 CAP Theorem Fundamentals

> **CAP Theorem** states that a distributed data store can only provide **two of three** guarantees simultaneously:

| Guarantee | Description | Analogy |
|-----------|-------------|---------|
| **C — Consistency** | Every read receives the **most recent write** or an error | All users see the same data at the same time |
| **A — Availability** | Every request receives a **non-error response** (without guarantee it's the latest data) | The system always responds, even if data is stale |
| **P — Partition Tolerance** | The system continues to operate despite **network failures** between nodes | Messages between servers can be lost, but the system keeps working |

**The key insight:** In a distributed system, **network partitions WILL happen** (it's not a matter of if, but when). So you must choose between **CP** (Consistency + Partition Tolerance) or **AP** (Availability + Partition Tolerance).

> **You cannot have all three at once.** When a network failure splits your database nodes, you must choose: stop accepting writes to stay consistent (CP), or keep accepting writes knowing nodes may disagree (AP).

---

## 8.2 CAP in Practice — Database Choices

| Database | Tradeoff | Real-World Use |
|----------|----------|----------------|
| **PostgreSQL** | **CP** — prefers consistency over availability during partitions | Bank transactions, order management — must be consistent |
| **Cassandra** | **AP** — prefers availability over consistency | Time-series data, IoT — stale data is acceptable, downtime is not |
| **MongoDB** | **CP** (default) — strong consistency | Document stores where consistency matters |
| **DynamoDB** | **AP** — eventually consistent (with optional strong consistency reads) | High-traffic web apps, session management |
| **Redis** | **CP** (single-node) or **AP** (cluster mode) | Caching — eventual consistency is acceptable |

**Interview take:**
> "In data engineering, most transactional systems (OLTP) are **CP** — you need accurate account balances. Most analytical systems (OLAP, data lakes) lean **AP** — eventual consistency is acceptable because you're doing batch processing."

---

## 8.3 Interview Take on CAP

> **When asked about CAP:** Acknowledge that in distributed systems, **partition tolerance is mandatory** (networks will fail). The real choice is between **CP and AP**:
> - **CP** for systems where accuracy is critical (payments, inventory)
> - **AP** for systems where uptime is critical (user-facing dashboards, recommendations)

---

# 9. MLOps — MLflow

## 9.1 MLOps Fundamentals

> **MLOps** is the application of DevOps principles to machine learning — automating the ML lifecycle from experimentation to production.

**The problem MLOps solves:** ML models are **not just code** — they involve data, training, evaluation, deployment, and monitoring. Without MLOps:
- Models are manually deployed (error-prone)
- No tracking of which model version is in production
- Model performance degrades silently over time (drift)
- Training is not reproducible

---

## 9.2 MLflow Components

| Component | Description |
|-----------|-------------|
| **Tracking** | Log parameters, metrics, and artifacts per training run |
| **Model Registry** | Version models, promote stages (Staging → Production) |
| **Model Serving** | Deploy models as REST API |
| **Projects** | Package ML code for reproducibility |

---

## 9.3 Model Promotion Workflow

```
1. Run experiments → compare in MLflow UI
2. Register best model → version 1
3. Move to Staging → validate in staging environment
4. Move to Production → serve real traffic
5. Monitor → rollback if performance degrades
```

---

# 10. Feature Stores & Model Deployment

## 10.1 Feature Store Fundamentals

> **What is a Feature Store?** A centralized system for storing, managing, and serving machine learning **features** (input variables for models).

**The problem it solves:** Without a feature store, data scientists:
- Recompute the same features across different projects (waste)
- Use inconsistent feature definitions (training vs inference mismatch)
- Can't serve features in real-time for production models
- Can't do point-in-time correct joins for training data

---

## 10.2 Feature Store Concepts

| Concept | Description |
|---------|-------------|
| **Online store** | Low-latency feature serving (Redis, DynamoDB) — for real-time inference |
| **Offline store** | Batch feature computation (S3, Delta, Parquet) — for training |
| **Point-in-time correct joins** | Ensures training data doesn't include future information (crucial for time-series models) |
| **Feature serving** | Get features at inference time via API |

**Example — Customer churn prediction:**
1. **Offline** — compute features daily in Spark → store in Feast offline store (S3)
2. **Online** — at prediction time, fetch features via Feast API from Redis
3. **Point-in-time** — for training, join features as they existed on that specific date

---

## 10.3 Model Deployment Patterns

| Pattern | Description | Best For |
|---------|-------------|----------|
| **Batch inference** | Score all customers daily, write predictions to Delta | Non-urgent decisions, large-scale scoring |
| **Real-time inference** | API endpoint calls model in memory | Fraud detection, recommendations (low-latency) |
| **Shadow mode** | New model runs in parallel but doesn't serve results | Safe testing of new model in production |
| **Canary** | Gradual rollout (5% → 20% → 100%) | Minimize blast radius of bad model |
| **A/B testing** | Route % traffic to each model variant | Compare performance metrics |

---

## 10.4 Model Monitoring — Drift & Degradation

| Type | What It Detects | Detection Method |
|------|----------------|------------------|
| **Data drift** | Input distribution changes over time | KS-test, Population Stability Index (PSI) |
| **Prediction drift** | Model output distribution changes | Track prediction mean/median over time |
| **Model degradation** | Accuracy drops over time | Compare predictions to ground truth (delayed feedback) |

---

# 11. Observability — Three Pillars

## 11.1 Observability Fundamentals

> **Observability** is the ability to understand what's happening inside a system by examining its **outputs** — without having to add new code to debug it.

**The three pillars:**

| Pillar | What It Answers | Tooling |
|--------|----------------|---------|
| **Metrics** | Is the system healthy? (latency, error rate, throughput) | Prometheus + Grafana |
| **Logging** | What exactly happened? (structured events with timestamps) | ELK (Elasticsearch, Logstash, Kibana) / CloudWatch |
| **Tracing** | Where is the slowness/failure? (end-to-end request flow) | OpenTelemetry + Jaeger |

> **Why it matters:** In a microservices architecture, a single user request touches 5+ services. Observability lets you trace that request end-to-end and pinpoint exactly which service failed or was slow.

---

## 11.2 Metrics (Prometheus + Grafana)

| Metric | What It Tracks |
|--------|----------------|
| `request_count` | Volume of API requests |
| `latency_p99` | 99th percentile response time (worst-case latency) |
| `error_rate` | Percentage of failed requests |
| `throughput` | Requests per second |
| `pipeline_row_count` | Data pipeline volume |
| `data_latency` | Time from data ingestion to availability |

---

## 11.3 Logging (ELK / CloudWatch)

> **Structured JSON logging** — every log entry is a machine-parseable JSON object:

```json
{"timestamp": "2026-05-25T16:00:00Z", "level": "ERROR", "pipeline": "orders", "error": "Connection timeout"}
```

**Log levels:** `DEBUG < INFO < WARNING < ERROR < CRITICAL`

**Best practice:** Ship all logs to a **centralized searchable store** (Elasticsearch, CloudWatch Logs) so you can search across all services from one place.

---

## 11.4 Tracing (OpenTelemetry + Jaeger)

> **Tracing** follows a single request across multiple services. Each unit of work is a **span**; the full path is a **trace**.

**Why it's essential for microservices:**
- A user request → API Gateway → Auth Service → Data Service → Model Service → Database
- Without tracing, if the request is slow, you don't know which service is the bottleneck
- With tracing, you see: "Auth took 2ms, Data took 500ms, Model took 3s" → **Model is the problem**

---

## 11.5 FastAPI Metrics Example

```python
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)

# Automatically provides /metrics endpoint with:
# - http_requests_total (counter by method, endpoint, status)
# - http_request_duration_seconds (histogram)
# - http_request_size_bytes (summary)
```

---

# 12. Microservices Architecture

## 12.1 Microservices Fundamentals

> **Microservices** is an architectural style where an application is built as a collection of **small, independent services**, each owning its own data and business logic, communicating via APIs.

**The problem microservices solve:** In a **monolith**, all code is in one application — a small change requires deploying the entire app, scaling is all-or-nothing, and a bug in one feature can crash everything.

**Key characteristics:**
| Feature | Description |
|---------|-------------|
| **Single responsibility** | Each service does one thing well |
| **Independent deployment** | Deploy services independently without affecting others |
| **Own data** | Each service has its own database (no shared DB) |
| **API contract** | Services communicate via well-defined APIs (REST/gRPC) |
| **Polyglot** | Different services can use different languages/technologies |

---

## 12.2 Monolith vs Microservices

| Aspect | **Monolith** | **Microservices** |
|--------|-------------|-------------------|
| **Deployment** | One deploy for everything | Independent deploys per service |
| **Scaling** | Scale entire app | Scale only the service that needs it |
| **Fault isolation** | One bug crashes everything | One service failing doesn't crash others |
| **Development speed** | Slows down as codebase grows | Teams work independently, faster |
| **Complexity** | Simple initially | More complex (networking, data consistency, observability) |

> **When NOT to use microservices:** Small teams, early-stage products, simple CRUD apps. **Start with a monolith, split when it hurts** — premature microservices add complexity without benefit.

---

## 12.3 Microservices in DE & GenAI

| Service | Responsibility |
|---------|----------------|
| **Data ingestion service** | Ingests data from sources (Kafka, API) |
| **Feature computation service** | Computes and serves ML features |
| **Model inference service** | Hosts ML model as REST API |
| **Training service** | Manages training jobs on Spark/K8s |
| **Monitoring service** | Tracks data drift, model degradation |
| **API Gateway** | Routes requests to appropriate services, handles auth |

---

> **Topics covered:** FastAPI, REST Design, Auth (JWT, OAuth), Docker, Kubernetes, CI/CD, CAP Theorem, MLOps (MLflow), Feature Stores, Model Deployment, Observability, Microservices
