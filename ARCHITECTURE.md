# 🎨 Visual Architecture Guide

## System Topology

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     SMART DARKSTORE INTELLIGENCE SYSTEM                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌────────────────────────────────────────────────────────────────────────┐   │
│  │                        DATA LAYER (SQLite)                             │   │
│  ├────────────────────────────────────────────────────────────────────────┤   │
│  │  Areas → Stores → Products → Customers → Orders → Deliveries         │   │
│  │                                                                         │   │
│  │  14 Tables | 1500+ Records | Normalized Schema                        │   │
│  └────────────────────────────────────────────────────────────────────────┘   │
│                                      ↓                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐   │
│  │                    ANALYTICS LAYER (SQL Queries)                       │   │
│  ├────────────────────────────────────────────────────────────────────────┤   │
│  │  Performance │ Demand │ Product Sales │ Delivery │ Customer │ Profit  │   │
│  │                                                                         │   │
│  │  10+ Pre-built Queries | Real-time Metrics                            │   │
│  └────────────────────────────────────────────────────────────────────────┘   │
│                                      ↓                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐   │
│  │               INTELLIGENCE LAYER (8 Specialized Engines)               │   │
│  ├────────────────────────────────────────────────────────────────────────┤   │
│  │                                                                         │   │
│  │  🔮 Demand        ⏱️  Delivery      📦 Inventory    🗺️  Location      │   │
│  │  Forecasting      Prediction       Optimization    Optimization       │   │
│  │  (7-day)          (SLA)            (ABC, EOQ)      (Expansion)        │   │
│  │                                                                         │   │
│  │  💰 Profit Simulation | Analysis Engines                              │   │
│  │  (What-if Scenarios)                                                   │   │
│  └────────────────────────────────────────────────────────────────────────┘   │
│                                      ↓                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐   │
│  │                      API LAYER (FastAPI Backend)                       │   │
│  ├────────────────────────────────────────────────────────────────────────┤   │
│  │  30+ REST Endpoints | Swagger/ReDoc | CORS Enabled                    │   │
│  │  http://localhost:8000 | /docs | /redoc                               │   │
│  └────────────────────────────────────────────────────────────────────────┘   │
│                                      ↓                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐   │
│  │                    PRESENTATION LAYER (Frontends)                      │   │
│  ├────────────────────────────────────────────────────────────────────────┤   │
│  │  📊 Streamlit Dashboard | 🔌 REST API Clients | 📱 Mobile Apps       │   │
│  │  8 Interactive Modules | Real-time Charts | Scenario Simulations     │   │
│  │  http://localhost:8501                                                │   │
│  └────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
                    RAW DATA
                       ↓
        ┌──────────────┴──────────────┐
        ↓                             ↓
   SIMULATE DATA              IMPORT FROM APIs
   (Faker)                     (Future)
        ↓                             ↓
        └──────────────┬──────────────┘
                       ↓
                   SQLite DB
                       ↓
        ┌──────────────┼──────────────┬──────────────┬───────────────┐
        ↓              ↓              ↓              ↓               ↓
   SQL Analytics  Demand         Delivery       Inventory        Location
   Queries        Forecasting    Prediction     Optimization     Optimization
        ↓              ↓              ↓              ↓               ↓
        └──────────────┼──────────────┴──────────────┴───────────────┘
                       ↓
                 Profit Simulation
                       ↓
                  FastAPI Backend
                       ↓
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
   Streamlit     REST API      Mobile App
   Dashboard     Clients       (Future)
```

---

## Database Schema Diagram

```
MASTER TABLES:
┌─────────┐    ┌───────┐    ┌──────────┐    ┌───────────┐
│ AREAS   │←───│STORES │←───│PRODUCTS  │    │CUSTOMERS  │
│ area_id │    │store_ │    │product_id│    │customer_id│
│ name    │    │id     │    │name      │    │name       │
│ city    │    │area_id│    │category  │    │area_id    │
│ pop     │    │name   │    │price     │    │email      │
└─────────┘    └───────┘    └──────────┘    └───────────┘
                   ↓
              TRANSACTION TABLES:
         ┌──────────┴─────────┐
         ↓                    ↓
      ORDERS             DELIVERIES
    (customer_id)      (order_id)
    (store_id)         (store_id)
    (order_date)       (delivery_time)
         ↓                    ↓
     ORDER_ITEMS        ANALYTICS TABLES
  (order_id)          (demand_forecast)
  (product_id)        (delivery_predictions)
  (quantity)          (inventory_metrics)
                      (profit_simulation)
         ↓
    INVENTORY
   (store_id)
   (product_id)
   (quantity)
```

---

## Engine Interaction Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                    SQL ANALYTICS ENGINE                          │
│  (Base Metrics: Revenue, Orders, Customers, Performance)        │
└───────┬──────────────┬──────────────┬──────────────┬─────────────┘
        ↓              ↓              ↓              ↓
   ┌─────────────┐  ┌────────────┐ ┌──────────────┐ ┌──────────┐
   │  DEMAND     │  │ DELIVERY   │ │  INVENTORY   │ │ LOCATION │
   │ FORECASTING │  │ PREDICTION │ │ OPTIMIZATION │ │ OPTIM.   │
   │             │  │            │ │              │ │          │
   │ · Predict   │  │ · Estimate │ │ · ABC        │ │ · Gap    │
   │   demand    │  │   time     │ │ · EOQ        │ │ · ROI    │
   │ · Ensemble  │  │ · SLA      │ │ · Reorder    │ │ · Market │
   │   methods   │  │   achieve  │ │ · Stockout   │ │ · Growth │
   └──────┬──────┘  └────────────┘ └──────────────┘ └──────────┘
          ↓              ↓              ↓              ↓
          └──────────────┬──────────────┴──────────────┘
                         ↓
            ┌────────────────────────────┐
            │ PROFIT SIMULATION ENGINE   │
            │                            │
            │ · Pricing scenarios        │
            │ · Inventory impact         │
            │ · Store expansion ROI      │
            │ · What-if modeling         │
            └────────────────┬───────────┘
                             ↓
                    INSIGHTS & DECISIONS
```

---

## Module Dependencies

```
main.py
  ├── database/db_schema.py
  │   └── sqlite3 connection
  │
  ├── data_simulator/simulate_data.py
  │   └── database/db_schema.py
  │
  ├── engines/sql_analytics.py
  │   └── database/db_schema.py
  │
  ├── engines/demand_forecasting.py
  │   ├── database/db_schema.py
  │   └── pandas, numpy
  │
  ├── engines/delivery_prediction.py
  │   ├── database/db_schema.py
  │   └── pandas, numpy
  │
  ├── engines/inventory_optimization.py
  │   ├── database/db_schema.py
  │   └── pandas, numpy
  │
  ├── engines/location_optimization.py
  │   ├── database/db_schema.py
  │   └── pandas, numpy
  │
  ├── engines/profit_simulation.py
  │   ├── database/db_schema.py
  │   └── pandas, numpy
  │
  ├── api/main.py
  │   ├── fastapi
  │   └── all engines
  │
  └── dashboard/app.py
      ├── streamlit
      ├── plotly
      └── all engines
```

---

## Process Flow: From Start to Insight

```
START
  ↓
[1] INITIALIZE DB
  ├─ Create 14 tables
  ├─ Set up indexes
  └─ Ready for data
  ↓
[2] SIMULATE DATA
  ├─ 5 areas × 2 stores = 10 stores
  ├─ 50 products across 7 categories
  ├─ 250 customers distributed
  ├─ 1500 orders (30 days)
  ├─ 1500 deliveries
  └─ 500 inventory records
  ↓
[3] RUN ANALYTICS
  ├─ Store performance queries
  ├─ Area demand analysis
  ├─ Product sales breakdown
  ├─ Delivery SLA tracking
  └─ Profitability metrics
  ↓
[4] RUN ENGINES
  ├─ Demand Forecasting
  │  └─ 7-day predictions
  ├─ Delivery Prediction
  │  └─ SLA achievability
  ├─ Inventory Optimization
  │  └─ ABC, reorder points
  ├─ Location Optimization
  │  └─ Expansion ROI
  └─ Profit Simulation
     └─ What-if scenarios
  ↓
[5] SAVE INSIGHTS
  ├─ Store in database
  ├─ Cache for API
  └─ Generate reports
  ↓
[6] EXPOSE VIA API
  ├─ 30+ REST endpoints
  ├─ Swagger documentation
  └─ CORS enabled
  ↓
[7] VISUALIZE DASHBOARD
  ├─ 8 interactive modules
  ├─ Real-time charts
  ├─ Scenario simulations
  └─ Export capabilities
  ↓
INSIGHTS & DECISIONS
```

---

## Technology Stack Visualization

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  ┌──────────────┐                 ┌──────────────┐          │
│  │  Streamlit   │                 │   FastAPI    │          │
│  │  (Dashboard) │                 │   (Backend)  │          │
│  │              │                 │              │          │
│  │  Plotly      │                 │  Auto-docs   │          │
│  │  Charts      │                 │  Swagger     │          │
│  └──────────────┘                 └──────────────┘          │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────┴──────────────────────────────────────────┐
│                 BUSINESS LOGIC LAYER                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐  │
│  │  Pandas     │ │   NumPy     │ │  Scikit-learn       │  │
│  │  (Data)     │ │  (Math)     │ │  (ML)               │  │
│  └─────────────┘ └─────────────┘ └─────────────────────┘  │
│                                                            │
│  8 Engines with Optimization, Forecasting, Simulation     │
└──────────────────┬───────────────────────────────────────┘
                   │
┌──────────────────┴───────────────────────────────────────┐
│                  DATA LAYER                             │
│  ┌──────────────┐                 ┌──────────────┐     │
│  │  SQLAlchemy  │                 │   SQLite     │     │
│  │  (ORM)       │─────────────────│  (Database)  │     │
│  │              │                 │              │     │
│  └──────────────┘                 └──────────────┘     │
└────────────────────────────────────────────────────────┘
```

---

## Deployment Architecture (Future)

```
┌────────────────────────────────────────────────────────────┐
│                   CLOUD DEPLOYMENT                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────────┐        ┌──────────────────┐        │
│  │   Load Balancer  │        │   API Gateway    │        │
│  └────────┬─────────┘        └────────┬─────────┘        │
│           │                           │                  │
│  ┌────────┴────────┐        ┌────────┴─────────┐        │
│  │                 │        │                  │        │
│  ├─────────────────┤        ├──────────────────┤        │
│  │   API Servers   │        │   Dashboard      │        │
│  │   (FastAPI)     │        │   (Streamlit)    │        │
│  │   (3 instances) │        │   (2 instances)  │        │
│  └────────┬────────┘        └────────┬─────────┘        │
│           │                          │                  │
│           └──────────────┬───────────┘                  │
│                          │                              │
│           ┌──────────────┴──────────────┐               │
│           │                             │               │
│    ┌──────┴──────┐             ┌────────┴────────┐     │
│    │   SQLite    │             │    Redis Cache  │     │
│    │   Database  │             │   (Caching)     │     │
│    │             │             │                 │     │
│    │  (RDS)      │             │  (ElastiCache)  │     │
│    └─────────────┘             └─────────────────┘     │
│                                                         │
│    ┌────────────────────────────────────────────┐      │
│    │      Logging & Monitoring (CloudWatch)     │      │
│    └────────────────────────────────────────────┘      │
│                                                         │
└────────────────────────────────────────────────────────┘
```

---

## API Request/Response Flow

```
CLIENT REQUEST
     ↓
HTTP POST /api/forecast/demand
     ↓
FastAPI Router
     ↓
Input Validation (Pydantic)
     ↓
DemandForecastingEngine.get_forecast_summary()
     ↓
Execute Query on SQLite
     ↓
Parse Results (Pandas DataFrame)
     ↓
Format as JSON
     ↓
HTTP 200 Response
     ↓
CLIENT RECEIVES JSON
```

---

## Interactive Dashboard Navigation

```
MAIN DASHBOARD
  ├─ Executive Summary (KPIs)
  ├─ Store Performance Chart
  ├─ Area Revenue Distribution
  ├─ Peak Hours Analysis
  └─ Delivery Performance Plot
       ↓
    SIDEBAR MENU
       ├─ Store Performance (Detailed)
       ├─ Area Analytics (Market Analysis)
       ├─ Inventory Optimization (ABC, Risk)
       ├─ Delivery Management (SLA, Metrics)
       ├─ Demand Forecasting (7-day Chart)
       ├─ Expansion Strategy (ROI, Opportunities)
       └─ Profit Simulation (Scenarios)
```

---

## Success Metrics Dashboard

```
┌─────────────────────────────────────────────────────────┐
│                  KEY METRICS                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  OPERATIONS                   FINANCIAL               │
│  ├─ 10 Stores               ├─ $2.5M Revenue         │
│  ├─ 5 Areas                 ├─ 15% Margin            │
│  ├─ 250 Customers           ├─ 3x ROI (Expansion)    │
│  ├─ 1500 Orders             ├─ $100K Savings (Inv.)  │
│  └─ 95% Fulfillment         └─ +12% (Pricing)        │
│                                                         │
│  PREDICTION                   OPTIMIZATION            │
│  ├─ 7-day Forecast          ├─ ABC Analysis           │
│  ├─ 85% SLA Achieve         ├─ 50% Stockout Reduce   │
│  ├─ 25min Avg Delivery      ├─ EOQ Optimization      │
│  ├─ 4.2★ Avg Rating         └─ Reorder Points        │
│  └─ Confidence: 95%                                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

This visual guide shows how all components work together to create a comprehensive decision support system! 🎨
