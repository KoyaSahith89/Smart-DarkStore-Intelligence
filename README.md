# 🏪 Smart DarkStore Intelligence System

**An AI-powered operations management platform for optimizing dark store networks**

---

## 📋 Overview

Smart DarkStore Intelligence is a comprehensive system designed for operations heads to:

- ✅ **Monitor store performance** - Real-time KPIs across all stores
- ✅ **Predict demand** - AI-powered forecasting for inventory planning
- ✅ **Reduce stockouts** - Intelligent inventory optimization
- ✅ **Improve SLA** - Delivery time predictions & optimization
- ✅ **Decide store locations** - Data-driven expansion strategy
- ✅ **Simulate profits** - What-if analysis for business decisions

---

## 🎯 Architecture: 8 Engines

### 1. **Data Simulation Engine**
Generates realistic dark store operational data:
- Areas & locations
- Stores across regions
- Products & categories
- Customers & behavior
- Orders & deliveries
- Inventory levels

📁 Location: `data_simulator/simulate_data.py`

### 2. **Data Warehouse (SQLite)**
Persistent data storage with optimized schema:
- 14 core tables
- Relational integrity
- Indexed for performance

📁 Location: `database/db_schema.py`

### 3. **SQL Analytics Layer**
Business intelligence queries:
- Store performance metrics
- Area demand analysis
- Product sales analysis
- Delivery SLA tracking
- Customer insights
- Profitability analysis

📁 Location: `engines/sql_analytics.py`

### 4. **Demand Forecasting Engine**
Time series prediction using:
- Simple Exponential Smoothing
- Moving Average Analysis
- Trend-based forecasting
- Ensemble methods

📁 Location: `engines/demand_forecasting.py`

### 5. **Delivery Time Prediction Engine**
ML-based delivery time estimation:
- Historical pattern analysis
- Hour & day-of-week patterns
- SLA achievability analysis
- Confidence scoring

📁 Location: `engines/delivery_prediction.py`

### 6. **Inventory Optimization Engine**
Advanced inventory management:
- ABC analysis (Pareto principle)
- EOQ calculations
- Reorder point optimization
- Stockout risk analysis
- Safety stock calculations

📁 Location: `engines/inventory_optimization.py`

### 7. **Location Optimization Engine**
Strategic store placement:
- Market demand analysis
- Coverage gap identification
- ROI estimation
- Competition analysis
- Growth opportunity scoring

📁 Location: `engines/location_optimization.py`

### 8. **Profit Simulation Engine**
What-if scenario analysis:
- Pricing change impact
- Inventory reduction impact
- New store expansion ROI
- Break-even analysis

📁 Location: `engines/profit_simulation.py`

---

## 📁 Project Structure

```
Smart-DarkStore-Intelligence/
│
├── database/
│   └── db_schema.py           # SQLite schema & setup
│
├── data_simulator/
│   └── simulate_data.py       # Realistic data generation
│
├── engines/
│   ├── sql_analytics.py       # Analytics Layer
│   ├── demand_forecasting.py  # Forecasting Engine
│   ├── delivery_prediction.py # Delivery Prediction
│   ├── inventory_optimization.py # Inventory Engine
│   ├── location_optimization.py # Location Engine
│   └── profit_simulation.py   # Profit Simulation
│
├── api/
│   └── main.py                # FastAPI Backend
│
├── dashboard/
│   └── app.py                 # Streamlit Dashboard
│
├── notebooks/
│   └── (exploratory analysis)
│
├── main.py                    # Orchestration Script
├── darkstore.db              # SQLite Database
└── README.md
```

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install pandas numpy faker matplotlib scikit-learn sqlalchemy fastapi uvicorn streamlit plotly
```

### 2. Initialize System

```bash
# Run main orchestration script
python main.py

# Select option 1: Initialize Database
# Select option 2: Run Data Simulation
```

### 3. Run Analytics

```bash
# Option 3: Run SQL Analytics
# Option 4-8: Run individual engines
# Option 9: Run all engines
```

### 4. Start API Server

```bash
python -m uvicorn api.main:app --reload

# API will be available at: http://localhost:8000
# Swagger UI: http://localhost:8000/docs
```

### 5. Launch Dashboard

```bash
# In a new terminal
streamlit run dashboard/app.py

# Dashboard opens at: http://localhost:8501
```

---

## 📊 Key Features

### Store Performance Dashboard
- Revenue tracking
- Order fulfillment rates
- Delivery time metrics
- Customer ratings

### Area Analytics
- Market demand analysis
- Coverage gap identification
- Population vs store ratio
- Expansion opportunities

### Inventory Management
- ABC classification
- Reorder point optimization
- Stockout risk alerts
- Carrying cost analysis

### Demand Forecasting
- 7-day forecast
- Confidence intervals
- Multiple forecasting methods
- Store-product level granularity

### Delivery Optimization
- SLA compliance tracking
- Delivery time predictions
- Performance by hour/day
- Route efficiency

### Profit Simulation
- Pricing scenario analysis
- Inventory reduction impact
- New store ROI calculations
- Break-even analysis

---

## 📈 API Endpoints

### Stores
- `GET /api/stores/performance` - Store KPIs
- `GET /api/stores/{store_id}/profitability` - Store profit

### Areas
- `GET /api/areas/demand` - Area demand
- `GET /api/areas/expansion-opportunities` - Expansion ROI
- `GET /api/areas/coverage-gaps` - Coverage analysis

### Forecasting
- `GET /api/forecast/demand` - Demand forecast
- `GET /api/forecast/demand/{store_id}/{product_id}` - Product forecast

### Delivery
- `GET /api/delivery/performance` - Delivery SLA
- `GET /api/delivery/predictions` - Time predictions
- `GET /api/delivery/sla-achievability` - SLA analysis

### Inventory
- `GET /api/inventory/status` - Current status
- `GET /api/inventory/optimization` - Recommendations
- `GET /api/inventory/abc-analysis` - ABC analysis
- `GET /api/inventory/efficiency` - Efficiency metrics

### Products
- `GET /api/products/sales` - Sales analysis

### Profit
- `GET /api/simulation/pricing/{percentage}` - Price impact
- `GET /api/simulation/inventory/{reduction}` - Inventory impact
- `GET /api/simulation/new-store/{area_id}` - Store expansion

### Dashboard
- `GET /api/dashboard/kpis` - Summary KPIs
- `GET /api/dashboard/summary` - Full summary

---

## 💡 Use Cases

### For Operations Head

1. **Monitor Performance**: Track 10+ KPIs across 100+ stores
2. **Plan Inventory**: Optimize stock levels with ABC analysis
3. **Predict Demand**: Forecast next 7 days per product per store
4. **Improve Delivery**: Hit 30-minute SLA with time predictions
5. **Expand Smart**: Data-driven location selection
6. **Simulate Impact**: Test pricing and inventory strategies

### Interview Narrative

*"We built an intelligent system that helps operations heads make data-driven decisions. Using 8 specialized engines, we monitor performance, predict demand, optimize inventory, and simulate business scenarios. The system processes real-time data through analytics layer, forecasting models, and optimization algorithms to provide actionable insights for 100+ stores across multiple regions."*

---

## 🔧 Technology Stack

- **Backend**: FastAPI, SQLAlchemy
- **Data**: SQLite, Pandas, NumPy
- **ML**: Scikit-learn, Time Series Analysis
- **Frontend**: Streamlit, Plotly
- **Data Gen**: Faker, Random

---

## 📊 Data Model

### Core Tables
1. **areas** - Geographic regions
2. **stores** - Dark store locations
3. **products** - Inventory items
4. **customers** - Customer data
5. **orders** - Order transactions
6. **order_items** - Line items
7. **deliveries** - Fulfillment tracking
8. **inventory** - Stock levels
9. **store_metrics** - Daily store KPIs
10. **delivery_metrics** - Delivery performance
11. **inventory_metrics** - Inventory analysis
12. **demand_forecast** - Predictions
13. **delivery_predictions** - Time estimates
14. **profit_simulation** - What-if scenarios

---

## 🎯 KPIs Tracked

### Store Level
- Total Revenue
- Order Count
- Average Order Value
- Fulfillment Rate
- Delivery Time
- Customer Rating
- Profit Margin

### Area Level
- Area Revenue
- Customer Count
- Orders Per Customer
- Market Penetration
- Coverage Gaps

### Product Level
- Sales Volume
- Revenue Contribution
- Inventory Turnover
- Reorder Points
- ABC Category

### Delivery Level
- SLA Compliance
- Average Time
- Cost Per Delivery
- Rating Distribution

---

## 🚀 Deployment

### Local Development
```bash
python main.py  # Run orchestration menu
```

### Production API
```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### Production Dashboard
```bash
streamlit run dashboard/app.py --server.port 8501
```

---

## 📝 Example Workflow

```
1. Initialize DB
   └─ Creates 14 tables

2. Simulate Data
   └─ 5 areas, 10 stores, 50 products, 250 customers
   └─ 1500 orders with deliveries

3. Run Analytics
   └─ Store performance summaries
   └─ Area demand analysis
   └─ Product sales breakdown

4. Run Engines
   ├─ Demand Forecast (7 days ahead)
   ├─ Delivery Prediction (SLA compliance)
   ├─ Inventory Optimization (ABC analysis)
   ├─ Location Optimization (Expansion ROI)
   └─ Profit Simulation (What-if scenarios)

5. Explore via API or Dashboard
   └─ View real-time KPIs
   └─ Run simulations
   └─ Download reports
```

---

## 🎓 Learning Resources

- **Time Series Forecasting**: Exponential Smoothing, ARIMA
- **Inventory Management**: ABC Analysis, EOQ, Reorder Points
- **Location Analysis**: Market Demand, Coverage Gaps, ROI
- **Profit Modeling**: Contribution Margin, Break-even, Scenarios

---

## 📞 Support

For questions or issues:
1. Check the API documentation at `/docs`
2. Review the code comments
3. Check dashboard tooltips

---

## 📄 License

Internal Use Only - Smart DarkStore Intelligence

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Built with**: Python, SQLite, FastAPI, Streamlit
