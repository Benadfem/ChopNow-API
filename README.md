# ChopNow-API 🚀

ChopNow-API is a production-ready, asynchronous backend gateway designed to handle real-world food delivery and logistics workflows. Inspired by traditional e-commerce and pizza delivery application patterns, this project scales those core mechanics into an enterprise-grade infrastructure. 

Instead of relying on simple, synchronous CRUD operations that freeze under heavy loads, ChopNow-API is architected to handle complex business processes—such as user authentication, order lifecycle management, and transactional database integrity—with maximum efficiency. It serves as a robust, high-performance foundation built specifically to support scalable web architectures and future intelligent orchestration layers.

---

## 🏗️ System Architecture & Design Decisions

### 1. Relational Database: PostgreSQL
* **The Choice:** PostgreSQL was selected as the primary relational database management system (RDBMS).
* **The Architecture Reason:** Food delivery ecosystems rely heavily on data integrity, strict relations (Users -> Orders -> Deliveries), and ACID compliance. PostgreSQL ensures that transactions (like placing an order and updating stock concurrently) are bulletproof, avoiding race conditions.

### 2. Database Evolution: Alembic Migrations
* **The Choice:** Schema version control is fully managed via Alembic.
* **The Architecture Reason:** In a live environment, altering database models directly can corrupt production data. Alembic ensures every database schema change (e.g., tracking user session state or adding specific order constraints) is documented as a step-by-step, reviewable migration script that can be safely rolled forward or backward.

### 3. Asynchronous Task Queue: Celery & Redis
* **The Choice:** Distributed task processing via Celery with Redis acting as the in-memory message broker.
* **The Architecture Reason:** Heavy operations—such as processing third-party payments, calculating delivery logistics, or handling background notification routines—introduce massive latency. ChopNow-API offloads these workflows to background worker nodes using an asynchronous event-driven loop. The API instantly returns a `202 Accepted` status along with a task ID, keeping the HTTP layer fast and responsive.

### 4. Rigid Data Contracts: Pydantic & FastAPI
* **The Choice:** Strict request/response validation using FastAPI dependencies and Pydantic models.
* **The Architecture Reason:** Incoming payloads must be heavily sanitized. Pydantic serves as a zero-trust gateway, forcing data into strict formats before it touches database queries, laying a clean foundation for structured data ingestion and verification.

---

## 📂 Project Directory Structure

```text
chopnow-api/                 # Root Repository Directory
│
├── .venv/                  # Isolated local virtual environment (untracked)
├── .gitignore              # Git ignore rules
├── .env                    # Local environment secrets (untracked)
├── README.md               # Project documentation
├── requirements.txt        # Project dependencies
├── alembic.ini             # Alembic migration configurations
│
├── src/                    # Application source code
│   ├── __init__.py
│   ├── main.py             # FastAPI application entry point
│   ├── config.py           # Pydantic settings management
│   │
│   ├── auth/               # Authentication & Security Module
│   │   ├── __init__.py
│   │   ├── router.py       
│   │   ├── service.py      
│   │   └── schemas.py      
│   │
│   ├── orders/             # Core Business Module (Orders Workflow)
│   │   ├── __init__.py
│   │   ├── router.py       
│   │   ├── models.py       
│   │   ├── service.py      
│   │   └── schemas.py      
│   │
│   ├── db/                 # Database Session Management
│   │   ├── __init__.py
│   │   ├── session.py      
│   │   └── base.py         
│   │
│   └── celery_tasks/       # Background Worker Orchestration
│       ├── __init__.py
│       ├── worker.py       
│       └── tasks.py        
│
├── migrations/             # Automatically generated Alembic migration versions
└── tests/                  # Automated Testing Suite (Pytest)
    ├── __init__.py
    ├── conftest.py         # Testing fixtures and isolated mock DB configurations
    ├── test_auth.py        
    └── test_orders.py