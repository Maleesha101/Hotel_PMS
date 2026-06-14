<div align="center">

# 🏨 Hotel Property Management System

### A production-grade microservices platform covering the complete guest journey - from room booking through housekeeping, maintenance, and final billing.

[![License: Private](https://img.shields.io/badge/License-Private-red.svg)]()
[![Architecture: Microservices](https://img.shields.io/badge/Architecture-Microservices-blue.svg)]()
[![API: REST](https://img.shields.io/badge/API-RESTful-green.svg)]()
[![Auth: JWT RS256](https://img.shields.io/badge/Auth-JWT%20RS256-orange.svg)]()
[![Docs: Swagger](https://img.shields.io/badge/Docs-Swagger%20UI-85EA2D.svg)]()

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Services](#-services)
  - [Auth & User Service](#1--auth--user-service)
  - [Reservation Service](#2--reservation-service)
  - [Housekeeping & Inventory Service](#3--housekeeping--inventory-service)
  - [Maintenance Service](#4--maintenance-service)
  - [Invoice & Billing Service](#5--invoice--billing-service)
- [Complete Workflow](#-complete-guest-journey-workflow)
- [Tech Stack](#-tech-stack-at-a-glance)
- [Event-Driven Architecture](#-event-driven-architecture-kafka)
- [API Reference](#-api-reference)
- [Role-Based Access Control](#-role-based-access-control)
- [Getting Started](#-getting-started)
- [Port Reference](#-port-reference)
- [Database Seeding](#-database-seeding)
- [Project Structure](#-project-structure)

---

## 🌐 Overview

The **Hotel Property Management System (Hotel PMS)** is a full-featured, cloud-ready backend platform that digitises and automates the core operations of a hotel. It is built as a suite of **five independent microservices**, each responsible for a single bounded business domain, communicating through **REST APIs** and **Apache Kafka** events.

The system tracks the complete guest lifecycle:

```
Room Setup → Booking → Check-In → Stay → Check-Out
     → Housekeeping → Maintenance → Invoice → Room Ready
```

Every step of this journey is managed by a dedicated service with its own database, API, and business logic — ensuring clean separation, independent scalability, and resilience.

---

## 🏗️ System Architecture

```
                          ┌─────────────────────────────────────┐
                          │           API Gateway (Kong)         │
                          │  TLS · Rate Limiting · JWT Pre-auth  │
                          └──────────────┬──────────────────────┘
                                         │
              ┌──────────────────────────┼───────────────────────────┐
              │                          │                           │
     ┌────────▼────────┐      ┌──────────▼──────────┐    ┌──────────▼──────────┐
     │  Auth & User    │      │    Reservation       │    │  Housekeeping &     │
     │    Service      │      │      Service         │    │  Inventory Service  │
     │  Node.js/TS     │      │    Node.js/TS        │    │     Python          │
     │  Express        │      │    NestJS            │    │     FastAPI         │
     │  PostgreSQL     │      │    PostgreSQL         │    │    PostgreSQL       │
     │  Redis          │      │    Redis             │    │    Redis            │
     │  Port: 8081     │      │    Port: 8089        │    │    Port: 8082       │
     └────────┬────────┘      └──────────┬──────────┘    └──────────┬──────────┘
              │                          │                           │
              │              ┌───────────▼──────────────────────────▼───────┐
              │              │              Apache Kafka                      │
              │              │   hotel.booking.checkout                       │
              │              │   hotel.booking.checkin                        │
              │              │   hotel.housekeeping.completed                 │
              │              │   hotel.housekeeping.damage-reported           │
              │              │   hotel.maintenance.completed                  │
              │              │   hotel.maintenance.charge                     │
              └──────────────┴───────────┬──────────────────────────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
     ┌────────▼────────┐      ┌──────────▼──────────┐             │
     │   Maintenance   │      │  Invoice & Billing  │             │
     │     Service     │      │      Service        │             │
     │  Java           │      │   Node.js/TS        │             │
     │  Spring Boot    │      │   NestJS            │             │
     │  PostgreSQL     │      │   PostgreSQL        │             │
     │  Port: 8083     │      │   Port: 3001        │             │
     └─────────────────┘      └─────────────────────┘             │
                                                                   │
                          ┌────────────────────────────────────────▼──┐
                          │              Redis (Shared)                │
                          │  Token Blocklist · Room Status Pub/Sub     │
                          └────────────────────────────────────────────┘
```

### Key architectural decisions

| Decision | Rationale |
|---|---|
| **RS256 asymmetric JWT** | Auth Service alone holds the private key. All other services verify tokens with the public key only — a compromised downstream service cannot forge tokens |
| **Database per service** | No shared databases. Each service owns its data entirely — enabling independent schema changes and preventing cross-service data coupling |
| **Kafka for cross-service events** | Checkout triggers Housekeeping + Invoice simultaneously without tight coupling. If Invoice is briefly unavailable, the event waits in Kafka — checkout is not blocked |
| **Redis pub/sub for room status** | Front-desk dashboards receive live room status updates without polling the database on every screen refresh |
| **Polyglot persistence** | MySQL/PostgreSQL for relational transactional data; Redis for ephemeral caching and pub/sub; chosen per domain's actual needs |

---

## 🔧 Services

### 1 🔐 Auth & User Service

> **The trust root of the entire platform**

| | |
|---|---|
| **Runtime** | Node.js 20 LTS + TypeScript 5 |
| **Framework** | Express.js 4.x + Passport.js |
| **Database** | PostgreSQL 15 + Redis 7 |
| **Port** | `8081` |
| **Swagger UI** | http://localhost:8081/swagger-ui.html |

Every microservice in this system validates JWT tokens signed by this service. The Auth Service is the **only** holder of the RSA private key. All other services receive the public key to verify tokens locally — zero network calls on each request.

**What it does:**
- Issues RS256 JWT access tokens (15 min TTL) and rotating refresh tokens (7 day TTL)
- Blocklists revoked tokens in Redis with exact TTL matching remaining token lifetime
- Detects refresh token **reuse attacks** — immediately revokes all sessions for the user
- Manages staff accounts: create, update, suspend, deactivate
- Enforces 5 hotel staff roles: `ADMIN` · `FRONT_DESK` · `HOUSEKEEPING` · `MAINTENANCE` · `ACCOUNTANT`
- Maintains a tamper-evident **audit log** of every login, logout, and admin action

**Key endpoints:**

```
POST   /api/v1/auth/login              → Authenticate, receive token pair
POST   /api/v1/auth/refresh            → Rotate refresh token
POST   /api/v1/auth/logout             → Revoke token (Redis blocklist)
POST   /api/v1/auth/verify             → Verify token (called by other services)
GET    /api/v1/auth/me                 → Get own profile
POST   /api/v1/users                   → Create staff user (ADMIN)
GET    /api/v1/users                   → List all users (ADMIN)
PATCH  /api/v1/users/:id               → Update user (ADMIN)
POST   /api/v1/users/:id/suspend       → Suspend + revoke all sessions (ADMIN)
GET    /api/v1/audit                   → View audit log (ADMIN)
```

---

### 2 🏨 Reservation Service

> **The calendar and booking engine**

| | |
|---|---|
| **Runtime** | Node.js 20 LTS + TypeScript 5 |
| **Framework** | NestJS 10.x |
| **Database** | PostgreSQL 15 + Redis 7 |
| **Port** | `8089` |
| **Swagger UI** | http://localhost:8089/swagger-ui.html |

The operational core of the PMS. Owns the room catalogue, date-range availability calendar, and the complete booking lifecycle. Publishes `checkout` and `checkin` events consumed by Housekeeping and Invoice services.

**What it does:**
- Manages the **room catalogue**: type, floor, bed config, pricing, status, facilities
- Serves a **date-range availability calendar** cached in Redis for fast queries
- Creates reservations with guest details, advance payment, booking source, and agreement confirmation
- Handles **booking amendments**: date changes, room swaps, guest count updates with full history
- Executes **check-in** (room → OCCUPIED) and **check-out** (room → DIRTY, publishes Kafka events)
- Manages **cancellations** with fee recording and refund status

**Key endpoints:**

```
POST   /api/v1/rooms                   → Add room (ADMIN)
GET    /api/v1/rooms/availability      → Calendar availability grid
POST   /api/v1/bookings                → Create reservation
PATCH  /api/v1/bookings/:id            → Amend booking
POST   /api/v1/bookings/:id/checkin    → Check in guest
POST   /api/v1/bookings/:id/checkout   → Check out → triggers downstream events
POST   /api/v1/bookings/:id/cancel     → Cancel with fee
GET    /api/v1/bookings/:id/amendments → Amendment history
```

---

### 3 🧹 Housekeeping & Inventory Service

> **Room readiness and stock control**

| | |
|---|---|
| **Runtime** | Python 3.12 |
| **Framework** | FastAPI 0.111 + Uvicorn |
| **Database** | PostgreSQL 15 + Redis 7 |
| **Port** | `8082` |
| **Swagger UI** | http://localhost:8082/swagger-ui.html |

Triggered automatically by `checkout` Kafka events. Manages the room's transition from DIRTY back to CLEAN — including task assignment, supply tracking, and damage reporting.

**What it does:**
- Tracks **live room status** (CLEAN / DIRTY / OCCUPIED / UNDER_MAINTENANCE / OUT_OF_ORDER)
- Auto-creates `CHECKOUT_CLEAN` tasks when a checkout event arrives from Kafka
- Manages **housekeeping task lifecycle**: pending → assigned → in-progress → completed
- Deducts **inventory stock atomically** when a task is completed
- Maintains **room supply standards** per room type (auto-used on task completion)
- Records **damaged / missing items** and routes them to Maintenance or Invoice
- Broadcasts live room status to Redis pub/sub channel `hotel:room-status`
- Runs a **daily 07:00 low-stock check** via APScheduler and publishes alerts

**Key endpoints:**

```
GET    /api/v1/rooms/status            → Live status of all rooms
PATCH  /api/v1/rooms/status/{room_id}  → Update room status (enforces valid transitions)
GET    /api/v1/rooms/status/dashboard  → Count of rooms per status
POST   /api/v1/tasks                   → Create cleaning task
POST   /api/v1/tasks/{id}/complete     → Complete task + deduct supplies
GET    /api/v1/inventory/low-stock     → Items below minimum stock level
POST   /api/v1/inventory/{id}/restock  → Add stock
POST   /api/v1/damage                  → Report damaged/missing item
POST   /api/v1/damage/{id}/send-to-maintenance  → Route to Maintenance Service
POST   /api/v1/damage/{id}/send-to-invoice      → Route charge to Invoice Service
```

---

### 4 🔧 Maintenance Service

> **Repair lifecycle and equipment management**

| | |
|---|---|
| **Runtime** | Java 17 |
| **Framework** | Spring Boot 3.3 |
| **Database** | PostgreSQL 15 |
| **Port** | `8083` |
| **Swagger UI** | http://localhost:8083/swagger-ui.html |

Receives damage reports from Housekeeping and complaints from the front desk. Manages technician assignment, repair tracking, equipment records, and a preventive maintenance scheduler.

**What it does:**
- Records **guest complaints** with urgency classification (LOW / MEDIUM / HIGH / CRITICAL)
- Forwards complaints to maintenance with auto-creation of `MaintenanceRequest`
- Manages **repair lifecycle**: PENDING → ASSIGNED → IN_PROGRESS → COMPLETED
- Tracks **estimated vs actual repair costs** per request
- Maintains an **equipment register** with serial numbers, warranty dates, and service history
- Runs a **daily 08:00 preventive scheduler** via Spring `@Scheduled` — auto-creates tasks for overdue equipment
- Publishes `maintenance.completed` and `maintenance.charge` events on repair completion
- Blocks rooms from new bookings during CRITICAL repairs via `room-blocked` Kafka event

**Key endpoints:**

```
POST   /api/v1/complaints              → Record guest complaint
POST   /api/v1/complaints/:id/forward  → Forward to maintenance (creates request)
POST   /api/v1/requests                → Create maintenance request
PATCH  /api/v1/requests/:id            → Assign technician / update status
POST   /api/v1/requests/:id/complete   → Complete repair + publish events
GET    /api/v1/equipment               → List equipment register
GET    /api/v1/equipment/:id/history   → Service history for equipment
GET    /api/v1/schedules/upcoming      → Preventive schedules due in 30 days
POST   /api/v1/schedules               → Create preventive schedule
```

---

### 5 🧾 Invoice & Billing Service

> **The financial ledger**

| | |
|---|---|
| **Runtime** | Node.js 20 LTS + TypeScript 5 |
| **Framework** | NestJS 10.x |
| **Database** | PostgreSQL 15 |
| **Port** | `8084` |
| **Swagger UI** | http://localhost:8084/swagger-ui.html |

Aggregates all chargeable events across the system into a single invoice per booking. Consumes damage charge and maintenance charge events from Kafka and adds them as line items automatically.

**What it does:**
- Auto-initialises an invoice when a booking is created
- Aggregates **room tariff, inventory usage, guest-chargeable damages, and maintenance charges** as line items
- Allows staff to add/edit/remove **manual charge line items**
- Applies **percentage, fixed, or seasonal discounts** with admin approval
- Calculates **subtotal, tax, and balance due** dynamically on demand
- Records **payments** (cash, card, transfer, online, advance) and tracks outstanding balance
- **Finalizes and locks** invoices on checkout; generates **PDF receipts**

**Key endpoints:**

```
GET    /api/v1/invoices/booking/:bookingId  → Get/create invoice for booking
POST   /api/v1/invoices/:id/items           → Add charge line item
DELETE /api/v1/invoices/:id/items/:itemId   → Remove line item
POST   /api/v1/invoices/:id/discounts       → Apply discount
GET    /api/v1/invoices/:id/calculate       → Live total preview
POST   /api/v1/invoices/:id/finalize        → Lock invoice
POST   /api/v1/invoices/:id/payments        → Record payment
GET    /api/v1/invoices/:id/pdf             → Download PDF receipt
```

---

## 🔄 Complete Guest Journey Workflow

```
1. ROOM SETUP
   Admin registers rooms via Reservation Service
   (room number, type, floor, bed config, price, facilities)
                    │
                    ▼
2. BOOKING CREATION
   Front desk creates booking with guest details,
   dates, advance payment, agreement confirmation
                    │
                    ▼
3. CHECK-IN
   ┌─ Reservation Service → room status: OCCUPIED
   └─ Invoice Service ← starts tracking room charge
                    │
                    ▼
4. CHECKOUT
   ┌─ Reservation Service → booking: CHECKED_OUT
   ├─ Kafka: hotel.booking.checkout
   │         │
   │         ├──▶ Housekeeping Service
   │         │    └─ Creates CHECKOUT_CLEAN task
   │         │    └─ Room status → DIRTY
   │         │
   │         └──▶ Invoice Service
   │              └─ Invoice moves to final billing stage
                    │
                    ▼
5. HOUSEKEEPING INSPECTION
   Staff assigned → starts task → inspects room
   ├─ Replaces supplies → inventory deducted automatically
   ├─ No damage found → room status: CLEAN
   │  └─ Kafka: hotel.housekeeping.completed
   │            └──▶ Reservation Service (room unblocked)
   │
   └─ Damage found → records damage report
      ├─ Requires repair?
      │  └─ POST /damage/:id/send-to-maintenance
      │     └─ Kafka: hotel.housekeeping.damage-reported
      │               └──▶ Maintenance Service (auto-creates request)
      │                    └─ room status: UNDER_MAINTENANCE
      │
      └─ Guest-chargeable?
         └─ POST /damage/:id/send-to-invoice
            └─ Kafka: hotel.housekeeping.charge
                       └──▶ Invoice Service (adds line item)
                    │
                    ▼
6. MAINTENANCE WORK  (if repair needed)
   Technician assigned → inspects → repairs
   └─ POST /requests/:id/complete
      └─ Kafka: hotel.maintenance.completed
                └──▶ Reservation Service (room → CLEAN/VACANT)
      └─ Kafka: hotel.maintenance.charge  (if guest-chargeable)
                └──▶ Invoice Service (adds repair cost line item)
                    │
                    ▼
7. FINAL INVOICE
   Accountant reviews:
   ├─ Room charges (auto-calculated)
   ├─ Extra service charges
   ├─ Damage charges (admin approved)
   ├─ Maintenance charges (admin approved)
   ├─ Discounts applied
   └─ Tax calculated
   → POST /invoices/:id/finalize → PDF generated → Payment recorded
                    │
                    ▼
8. ROOM AVAILABLE
   Room status: CLEAN + VACANT
   Available for new bookings on the calendar ✓
```

---

## 🛠️ Tech Stack at a Glance

| Service | Language | Framework | Database | Cache/Msg | Port |
|---|---|---|---|---|---|
| Auth & User | Node.js + TypeScript | Express.js | PostgreSQL 15 | Redis 7 | 8080 |
| Reservation | Node.js + TypeScript | NestJS | PostgreSQL 15 | Redis 7 | 8081 |
| Housekeeping | Python 3.12 | FastAPI | PostgreSQL 15 | Redis 7 | 8082 |
| Maintenance | Java 21 | Spring Boot 3.3 | PostgreSQL 15 | — | 8083 |
| Invoice | Node.js + TypeScript | NestJS | PostgreSQL 15 | — | 8084 |
| **Shared** | — | — | — | **Apache Kafka** | 9092 |

### Why these choices?

| Choice | Reason |
|---|---|
| **NestJS** for Reservation + Invoice | Strong TypeScript support, modular architecture, built-in validation, shared DTOs between services |
| **Express.js** for Auth | Minimal overhead for a focused service; full control over middleware chain (JWT filter, rate limiter, audit hooks) |
| **FastAPI** for Housekeeping | Async-native for high-frequency room status queries; native Pydantic validation; excellent aiokafka integration |
| **Spring Boot** for Maintenance | Mature `@Scheduled` job infrastructure for the preventive maintenance cron; Spring Data JPA handles the complaint → request → equipment relational tree cleanly |
| **PostgreSQL everywhere** | ACID guarantees for financial data (Invoice), booking conflicts (Reservation), and audit logs (Auth); advanced indexing; battle-tested at scale |
| **Redis** for Auth + Housekeeping | O(1) token blocklist lookups with auto-expiring keys; pub/sub for live room status broadcast to front-desk dashboards |
| **Apache Kafka** | Decouples checkout workflow — Housekeeping and Invoice process events independently; resilient to downstream slowness; replay-able |

---

## 📨 Event-Driven Architecture (Kafka)

Services communicate asynchronously via Kafka topics. This ensures that a slow Invoice Service never blocks a guest's checkout, and events are not lost if a consumer is temporarily unavailable.

| Kafka Topic | Publisher | Consumer(s) | Trigger |
|---|---|---|---|
| `hotel.booking.checkout` | Reservation | Housekeeping, Invoice | Guest checks out |
| `hotel.booking.checkin` | Reservation | Housekeeping | Guest checks in |
| `hotel.housekeeping.completed` | Housekeeping | Reservation | Room cleaned and ready |
| `hotel.housekeeping.damage-reported` | Housekeeping | Maintenance | Damage needs repair |
| `hotel.housekeeping.charge` | Housekeeping | Invoice | Guest-chargeable damage |
| `hotel.housekeeping.low-stock` | Housekeeping | Management | Daily stock alert |
| `hotel.maintenance.completed` | Maintenance | Reservation | Room repaired and ready |
| `hotel.maintenance.charge` | Maintenance | Invoice | Repair cost charged to guest |
| `hotel.maintenance.room-blocked` | Maintenance | Reservation | Critical repair — block room |

---

## 📋 API Reference

All services expose Swagger UI during development. JWT Bearer auth is pre-configured in each Swagger instance — log in once, copy the token, and test all endpoints interactively.

| Service | Swagger UI | OpenAPI JSON |
|---|---|---|
| Auth & User | http://localhost:8080/swagger-ui.html | http://localhost:8080/v3/api-docs |
| Reservation | http://localhost:8081/swagger-ui.html | http://localhost:8081/v3/api-docs |
| Housekeeping | http://localhost:8082/swagger-ui.html | http://localhost:8082/v3/api-docs |
| Maintenance | http://localhost:8083/swagger-ui.html | http://localhost:8083/v3/api-docs |
| Invoice | http://localhost:8084/swagger-ui.html | http://localhost:8084/v3/api-docs |

---

## 👥 Role-Based Access Control

Five roles are defined in the system. Every JWT token carries the user's role claim; each service enforces permissions independently without calling back to the Auth Service.

| Endpoint Domain | ADMIN | FRONT_DESK | HOUSEKEEPING | MAINTENANCE | ACCOUNTANT |
|---|:---:|:---:|:---:|:---:|:---:|
| User management | ✅ | ❌ | ❌ | ❌ | ❌ |
| Audit logs | ✅ | ❌ | ❌ | ❌ | ❌ |
| Room setup | ✅ | ❌ | ❌ | ❌ | ❌ |
| Availability / read rooms | ✅ | ✅ | ✅ | ✅ | ❌ |
| Create / amend bookings | ✅ | ✅ | ❌ | ❌ | ❌ |
| Check-in / check-out | ✅ | ✅ | ❌ | ❌ | ❌ |
| Room status updates | ✅ | ❌ | ✅ | ❌ | ❌ |
| Housekeeping tasks | ✅ | ❌ | ✅ | ❌ | ❌ |
| Inventory restock | ✅ | ❌ | ✅ | ❌ | ❌ |
| Damage reports | ✅ | ❌ | ✅ | ❌ | ❌ |
| Maintenance requests | ✅ | ❌ | ❌ | ✅ | ❌ |
| Complaint recording | ✅ | ✅ | ❌ | ✅ | ❌ |
| Equipment records | ✅ | ❌ | ❌ | ✅ | ❌ |
| Invoice read | ✅ | ✅ | ❌ | ❌ | ✅ |
| Invoice write / finalize | ✅ | ❌ | ❌ | ❌ | ✅ |
| Record payments | ✅ | ✅ | ❌ | ❌ | ✅ |

---

## 🚀 Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (v24+)
- [Node.js 20 LTS](https://nodejs.org/) (for Auth, Reservation, Invoice services)
- [Python 3.12](https://www.python.org/) (for Housekeeping service)
- [Java 21 JDK](https://adoptium.net/) (for Maintenance service)

### 1. Clone the repository

```bash
git clone https://github.com/your-org/hotel-pms.git
cd hotel-pms
```

### 2. Generate RSA keys (first-time only)

```bash
cd auth-service
npm install
npm run gen-keys
# Copy the printed keys into auth-service/.env
```

### 3. Configure environment files

Copy `.env.example` to `.env` in each service directory and fill in the values:

```bash
cp auth-service/.env.example         auth-service/.env
cp reservation-service/.env.example  reservation-service/.env
cp housekeeping-service/.env.example housekeeping-service/.env
cp maintenance-service/.env.example  maintenance-service/.env
cp invoice-service/.env.example      invoice-service/.env
```

The only value you **must** set manually is `JWT_PUBLIC_KEY` in every service except Auth — paste the public key generated in step 2.

### 4. Start the full stack

```bash
# From the repo root (requires a root docker-compose.yml)
docker-compose up --build

# Or start each service individually:
cd auth-service         && docker-compose up --build -d
cd reservation-service  && docker-compose up --build -d
cd housekeeping-service && docker-compose up --build -d
cd maintenance-service  && docker-compose up --build -d
cd invoice-service      && docker-compose up --build -d
```

### 5. Verify all services are running

```bash
curl http://localhost:8080/health   # Auth
curl http://localhost:8081/health   # Reservation
curl http://localhost:8082/health   # Housekeeping
curl http://localhost:8083/health   # Maintenance (Spring Boot)
curl http://localhost:8084/health   # Invoice
```

All should return `{ "status": "ok" }`.

### 6. First login

```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hotelpms.com", "password": "Admin@1234!"}'
```

Copy the `accessToken` from the response and use it as `Authorization: Bearer <token>` for all subsequent requests. Paste it into the Swagger UI **Authorize** button to test all endpoints interactively.

---

## 🔌 Port Reference

| Service | App Port | PostgreSQL Port | Redis Port |
|---|:---:|:---:|:---:|
| Auth & User | 8080 | 5435 | 6381 |
| Reservation | 8081 | 5436 | 6382 |
| Housekeeping | 8082 | 5434 | 6380 |
| Maintenance | 8083 | 5433 | — |
| Invoice | 8084 | 5437 | — |
| Kafka | — | — | 9092 |

> All PostgreSQL and Redis ports are offset to avoid conflicts when running all services simultaneously on the same machine.

---

## 🌱 Database Seeding

### Housekeeping Service — seed rooms (Windows PowerShell)

```powershell
docker exec housekeeping-postgres psql -U postgres -d housekeeping_db -c "
INSERT INTO room_status (id, room_id, room_number, floor, room_type, status, created_at, updated_at)
VALUES
  (gen_random_uuid(), 'room-101', '101', 1, 'SINGLE', 'VACANT',            NOW(), NOW()),
  (gen_random_uuid(), 'room-203', '203', 2, 'DOUBLE', 'DIRTY',             NOW(), NOW()),
  (gen_random_uuid(), 'room-305', '305', 3, 'DELUXE', 'UNDER_MAINTENANCE', NOW(), NOW()),
  (gen_random_uuid(), 'room-501', '501', 5, 'SUITE',  'CLEAN',             NOW(), NOW())
ON CONFLICT (room_id) DO NOTHING;
"
```

### Auth Service — seed users (Windows PowerShell)

The Auth Service auto-seeds one user per role on first startup in `ENVIRONMENT=development`. Default credentials:

| Role | Email | Password |
|---|---|---|
| Admin | admin@hotelpms.com | Admin@1234! |
| Front Desk | frontdesk@hotelpms.com | FrontDesk@1234 |
| Housekeeping | housekeeping@hotelpms.com | Housekeep@1234 |
| Maintenance | maintenance@hotelpms.com | Maintain@1234 |
| Accountant | accountant@hotelpms.com | Account@1234 |

> ⚠️ Change all passwords immediately in any non-development environment.

---

## 📁 Project Structure

```
hotel-pms/
├── auth-service/                  # Node.js + Express + TypeScript
│   ├── src/
│   │   ├── modules/auth/          # Login, logout, refresh, verify
│   │   ├── modules/users/         # User CRUD + role management
│   │   ├── modules/audit/         # Audit log read endpoints
│   │   ├── middleware/            # JWT filter, rate limiter, RBAC guard
│   │   └── shared/                # JWT helpers, errors, enums
│   ├── prisma/schema.prisma       # User, RefreshToken, AuditLog
│   ├── scripts/generate-rsa-keys.ts
│   └── docker-compose.yml
│
├── reservation-service/           # Node.js + NestJS + TypeScript
│   ├── src/
│   │   ├── domain/rooms/          # Room catalogue + availability
│   │   ├── domain/bookings/       # Booking CRUD + checkin/checkout
│   │   └── messaging/             # Kafka producers (checkout/checkin events)
│   └── docker-compose.yml
│
├── housekeeping-service/          # Python + FastAPI
│   ├── app/
│   │   ├── domain/room_status/    # Live room status + dashboard
│   │   ├── domain/tasks/          # Task lifecycle management
│   │   ├── domain/supplies/       # Room supply standards
│   │   ├── domain/inventory/      # Stock tracking + transactions
│   │   ├── domain/damage/         # Damage report + routing
│   │   ├── messaging/             # aiokafka consumer + producer
│   │   └── scheduler/             # APScheduler low-stock daily job
│   ├── alembic/                   # DB migrations
│   └── docker-compose.yml
│
├── maintenance-service/           # Java 21 + Spring Boot
│   ├── src/main/java/.../
│   │   ├── domain/complaint/      # Guest complaint handling
│   │   ├── domain/request/        # Maintenance request lifecycle
│   │   ├── domain/equipment/      # Equipment register + history
│   │   ├── domain/schedule/       # Preventive maintenance schedules
│   │   ├── messaging/             # Kafka consumer + publisher
│   │   └── scheduler/             # @Scheduled preventive job 08:00
│   ├── src/main/resources/db/migration/  # Flyway SQL migrations
│   └── docker-compose.yml
│
└── invoice-service/               # Node.js + NestJS + TypeScript
    ├── src/
    │   ├── domain/invoices/        # Invoice + line items
    │   ├── domain/payments/        # Payment recording
    │   ├── domain/discounts/       # Discount application
    │   └── messaging/              # Kafka consumer (damage/maintenance charges)
    └── docker-compose.yml
```

---

## 🧪 Running Tests

```bash
# Auth Service
cd auth-service && npm test

# Reservation Service
cd reservation-service && npm test

# Housekeeping Service
cd housekeeping-service && pytest tests/ -v --asyncio-mode=auto

# Maintenance Service
cd maintenance-service && ./mvnw test

# Invoice Service
cd invoice-service && npm test
```

All services use **Testcontainers** for integration tests — no external database required to run the test suite.

---

## 🔒 Security Notes

- **Never commit `.env` files or RSA key files** (`.keys/` directory is gitignored)
- The **JWT private key** must only exist in the Auth Service environment — never distribute it
- All passwords must meet the policy: min 8 chars, 1 uppercase, 1 number, 1 special character
- Swagger UI is **disabled in production** (`ENVIRONMENT=production`)
- Login endpoint is **rate-limited** to 10 requests per 15 minutes per IP

---

<div align="center">

Built for the Hotel Property Management System · Internal Use Only

</div>
