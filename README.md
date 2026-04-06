# 🛒 Erinaldo's Mercearia API

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

> An educational backend project developed collaboratively with 2nd-semester students at CEEP.

## 📖 About the Project

This repository contains the backend infrastructure for **Mercearia do Erinaldo**. It is designed as a practical learning experience, building a robust API from scratch using modern Python frameworks and database management practices.

## 🚀 Project Roadmap

### 📍 First Stage: Core Infrastructure
- Creation of the foundational API endpoints.
- Establishing database connections and modeling data.
- Utilizing **SQLite** for local development/testing and **PostgreSQL** for a production-ready environment.

### 📍 Second Stage: Security & Authentication
- Implementing secure user authentication.
- Protecting API routes and endpoints using **JWT (JSON Web Tokens)**.

## 🛠️ Technologies & Tools

- **Language:** Python
- **Framework:** FastAPI
- **Databases:** SQLite & PostgreSQL
- **Security:** JWT Authentication

---
Complete documentation of all items created in the Grocery Store's FastAPI project.
# API — João's Grocery Store

Complete documentation of all items created in João's Grocery Store FastAPI project.

---

## Summary

1. [Core](#1-core)
   - [config.py](#11-configpy)
   - [database.py](#12-databasepy)
   - [dependencies.py](#13-dependenciespy)
   - [security.py](#14-securitypy)
2. [Users Module](#2-users-module-users)
   - [models.py](#21-modelspy)
   - [schemas.py](#22-schemaspy)
   - [repositories.py](#23-repositoriespy)
   - [services.py](#24-servicespy)
   - [routers.py](#25-routerspy)
3. [Authentication Module (Auth)](#3-authentication-module-auth)
   - [schemas.py](#31-schemaspy)
   - [routers.py](#32-routerspy)
4. [Products Module](#4-products-module-products)
   - [models.py](#41-modelspy)
   - [schemas.py](#42-schemaspy)
   - [repositories.py](#43-repositoriespy)
   - [services.py](#44-servicespy)
   - [routers.py](#45-routerspy)
5. [Orders Module](#5-orders-module-orders)
   - [models.py](#51-modelspy)
   - [schemas.py](#52-schemaspy)
   - [repositories.py](#53-repositoriespy)
   - [services.py](#54-servicespy)
   - [routers.py](#55-routerspy)
6. [Application Entry Point](#6-application-entry-point-mainpy)

---

## 1. Core

### 1.1 `config.py`

| Aspect | Detail |
|--------|--------|
| **Function** | Centralizes the application's global settings |
| **Technology** | Pydantic `BaseSettings` with `.env` support |
| **Important Points** | Defines `DATABASE_URL` (SQLite), `SECRET_KEY` (JWT), `ALGORITHM` (HS256), `ACCESS_TOKEN_EXPIRE_MINUTES`. Values can be overridden by environment variables. |

### 1.2 `database.py`

| Aspect | Detail |
|--------|--------|
| **Function** | Configures the SQLite database connection |
| **Important Points** | Creates the `engine` with `check_same_thread=False` (required for SQLite in FastAPI). Defines `SessionLocal` (session factory) and `Base` (inheritance for all ORM models). |

### 1.3 `dependencies.py`

| Aspect | Detail |
|--------|--------|
| **Function** | Injectable dependencies used by FastAPI (Dependency Injection) |
| **Important Points** | |
| — `get_db()` | Generator that opens and closes a database session per request |
| — `get_current_user()` | Decodes the JWT token, fetches the user from the database. Blocks unauthenticated access (401) |
| — `get_current_manager()` | Wraps `get_current_user` and checks whether `role == "manager"`. Blocks non-managers (403) |

### 1.4 `security.py`

| Aspect | Detail |
|--------|--------|
| **Function** | Security utilities — password hashing and JWT token generation |
| **Important Points** | Uses `passlib` with `bcrypt` for password hashing. Functions: `get_password_hash()`, `verify_password()`, `create_access_token()`. The token is signed with the `SECRET_KEY` from config. |

---

## 2. Users Module

### 2.1 `models.py`

| Aspect | Detail |
|--------|--------|
| **Function** | ORM model for the `users` table |
| **Fields** | `id`, `name`, `email` (unique), `hashed_password`, `role`, `is_active` |
| **Important Points** | `UserRole` enum: `manager`, `seller`, `customer`, `supplier`. Bidirectional relationship with `Order` via `orders = relationship("Order")`. |

### 2.2 `schemas.py`

| Aspect | Detail |
|--------|--------|
| **Function** | Pydantic validation for user input/output |
| **Schemas** | `UserBase` (common fields), `UserCreate` (with password), `UserResponse` (with id + is_active, without password) |
| **Important Points** | Uses `EmailStr` for email validation. `from_attributes=True` for ORM serialization. The default `role` is `CUSTOMER`. |

### 2.3 `repositories.py`

| Aspect | Detail |
|--------|--------|
| **Function** | Direct database access for users |
| **Methods** | `get_by_email()`, `create()`, `delete()` |
| **Important Points** | `delete` is a **soft delete** — it sets `is_active = False` instead of physically removing the record from the database. |

### 2.4 `services.py`

| Aspect | Detail |
|--------|--------|
| **Function** | Business logic for users |
| **Methods** | `create_user()`, `delete_user()` |
| **Important Points** | `create_user` checks whether the email already exists (400), applies password hashing before saving. `delete_user` raises 404 if the user is not found. |

### 2.5 `routers.py`

| Method | Route | Function | Auth |
|--------|------|--------|------|
| `POST` | `/users/` | Create user | Open |
| `GET` | `/users/me` | Get logged-in user data | `get_current_user` |
| `DELETE` | `/users/{id}` | Deactivate user (soft delete) | `get_current_manager` |

---

## 3. Authentication Module (Auth)

### 3.1 `schemas.py`

| Aspect | Detail |
|--------|--------|
| **Function** | Pydantic schema for login response |
| **Schemas** | `Token` (`access_token`, `token_type`) |

### 3.2 `routers.py`

| Aspect | Detail |
|--------|--------|
| **Function** | Login endpoint |
| **Verb** | `POST /auth/login` |
| **Input** | `OAuth2PasswordRequestForm` (email + password via Swagger’s standard form) |
| **Important Points** | Fetches the user by email, verifies the password hash. If valid, generates a JWT with `sub=user.email` and `role=user.role`. Returns `access_token` + `token_type: "bearer"`. |

### 3.3 `controllers.py`, `services.py`

Both files are **empty** (unused). The auth logic lives directly in the auth module’s `routers.py`.

---

## 4. Products Module

### 4.1 `models.py`

| Aspect | Detail |
|--------|--------|
| **Function** | ORM model for the `products` table |
| **Fields** | `id`, `name`, `description`, `price`, `stock` |
| **Important Points** | `stock` has `default=0`. `description` is nullable (optional field). |

### 4.2 `schemas.py`

| Aspect | Detail |
|--------|--------|
| **Function** | Pydantic schemas for products |
| **Schemas** | `ProductBase`, `ProductCreate`, `ProductUpdate`, `ProductResponse` |
| **Important Points** | `ProductCreate` requires all fields (`name`, `price`, `stock`). `ProductUpdate` has all optional fields (`exclude_unset=True`). |

### 4.3 `repositories.py`

| Aspect | Detail |
|--------|--------|
| **Function** | Direct CRUD for products |
| **Methods** | `create()`, `list_all()`, `get_by_id()`, `update()`, `delete()` |

### 4.4 `services.py`

| Aspect | Detail |
|--------|--------|
| **Function** | Product business logic |
| **Important Points** | `get_product` returns 404 if it does not exist. `update_product` and `delete_product` reuse `get_product` for validation. |

### 4.5 `routers.py`

| Method | Route | Function | Auth |
|--------|------|--------|------|
| `POST` | `/products/` | Create product | Open |
| `GET` | `/products/` | List all | Open |
| `GET` | `/products/{id}` | Get one | Open |
| `PUT` | `/products/{id}` | Update | Open |
| `DELETE` | `/products/{id}` | Delete | Open |
| `POST` | `/products/{id}/image` | Upload image | Open |

> The image upload saves the file to `static/images/` and updates the URL in the database.

---

## 5. Orders Module

### 5.1 `models.py`

| Aspect | Detail |
|--------|--------|
| **Function** | ORM models for the `orders` and `order_items` tables |
| **Order Fields** | `id`, `user_id` (FK → users), `status`, `total`, `notes`, `created_at` |
| **OrderItem Fields** | `id`, `order_id` (FK → orders), `product_id` (FK → products), `quantity`, `unit_price` |
| **Important Points** | `OrderItems` has cascade delete (`all, delete-orphan`). `OrderStatus` enum: `pending`, `paid`, `shipped`, `cancelled`, `delivered`. `created_at` uses `default=datetime.now`. Bidirectional relationship with `User` and `Product`. |

### 5.2 `schemas.py`

| Aspect | Detail |
|--------|--------|
| **Function** | Pydantic schemas for orders |
| **Schemas** | `OrderItemCreate`, `OrderItemResponse`, `OrderCreate`, `OrderUpdate`, `OrderResponse` |
| **Important Points** | `OrderCreate` accepts a list of `items`. `OrderResponse` includes nested items and calculates the total. `from_attributes=True`. |

### 5.3 `repositories.py`

| Aspect | Detail |
|--------|--------|
| **Function** | Direct CRUD for orders |
| **Methods** | `create()` (order + items + total calculation), `list_by_user()`, `get_by_id()`, `update_status()`, `update()`, `delete()` |
| **Important Points** | The `create()` method performs `flush()` to obtain the order ID before creating the items, ensuring referential integrity. |

### 5.4 `services.py`

| Aspect | Detail |
|--------|--------|
| **Function** | Order business logic |
| **Methods** | `create_order()`, `list_orders()`, `get_order()`, `cancel_order()`, `update_order()`, `delete_order()` |
| **Important Points** | **Stock validation** before creation: if stock is insufficient, it returns 400. On creation, stock is automatically deducted. **Cancellation**: only allowed for `pending` status — product stock is restored when the order is cancelled. |

### 5.5 `routers.py`

| Method | Route | Function | Auth |
|--------|------|--------|------|
| `POST` | `/orders/` | Create order | `get_current_user` |
| `GET` | `/orders/` | List user orders | `get_current_user` |
| `GET` | `/orders/{id}` | Get order | `get_current_user` |
| `PUT` | `/orders/{id}` | Update status/notes | `get_current_user` |
| `POST` | `/orders/{id}/cancel` | Cancel pending order | `get_current_user` |
| `DELETE` | `/orders/{id}` | Remove order | `get_current_user` |

---

## 6. Application Entry Point (`main.py`)

| Aspect | Detail |
|--------|--------|
| **Function** | FastAPI application configuration and assembly |
| **Important Points** | |
| — **Tables** | `Base.metadata.create_all(bind=engine)` creates all tables at startup |
| — **Routers** | Registers all routers: `users`, `auth`, `products`, `orders` |
| — **Static files** | Mounts the `static/` folder at `/static` to serve product images |
| — **CORS** | Allows `*` (all origins) — required for local development |
| — **Root** | `GET /` returns an API status message |

---

## Architecture Overview

```python
FastAPI (main.py)
│
├── Core
│   ├── config.py        → Global settings and .env
│   ├── database.py      → Engine, Session, ORM Base
│   ├── dependencies.py  → Dependency injection (DB, Auth)
│   └── security.py      → Password hashing + JWT
│
├── Modules
│   ├── users/           → User management (CRUD + soft delete)
│   ├── auth/            → Login and JWT token generation
│   ├── products/        → Product catalog + image upload
│   └── orders/          → Orders with stock validation
│       ├── models.py         → orders + order_items tables
│       ├── schemas.py        → Pydantic validation
│       ├── repositories.py   → SQL CRUD
│       ├── services.py       → Business rules (stock)
│       └── routers.py        → REST endpoints
│
└── static/images/       → Product images
```

---

## Technologies Used

| Technology | Use |
|------------|-----|
| **FastAPI** | API framework |
| **SQLAlchemy** | Database ORM |
| **SQLite** | Database (development) |
| **Pydantic** | Data validation and serialization |
| **JWT (PyJWT)** | Token-based authentication |
| **Passlib + Bcrypt** | Password hashing |
| **Python Enum** | Fixed types (`UserRole`, `OrderStatus`) |



*Developed by the 2nd-semester CEEP class.*

_____
