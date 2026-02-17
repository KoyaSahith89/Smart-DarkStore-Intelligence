# 🏪 Smart DarkStore Intelligence - File Index & Navigation

## 📌 Start Here

1. **First Time?** → Read [QUICKSTART.md](QUICKSTART.md) (5 minutes)
2. **Want Full Details?** → Read [README.md](README.md)
3. **Understand Architecture?** → Read [ARCHITECTURE.md](ARCHITECTURE.md)
4. **Interview Prep?** → Read [SYSTEM_SUMMARY.md](SYSTEM_SUMMARY.md)
5. **Project Complete?** → Read [BUILD_COMPLETE.md](BUILD_COMPLETE.md)

---

## 📁 File Organization

### 🎯 Entry Points (Start with these)
- **`main.py`** - Main orchestration menu (START HERE!)
- **`verify_system.py`** - Verify all systems are installed
- **`config.py`** - All configuration parameters

### 📚 Documentation (Read these)
| File | Purpose | Read Time |
|------|---------|-----------|
| **README.md** | Complete documentation | 10 min |
| **QUICKSTART.md** | 5-minute setup guide | 5 min |
| **SYSTEM_SUMMARY.md** | Project overview for interviews | 8 min |
| **ARCHITECTURE.md** | Visual architecture diagrams | 7 min |
| **BUILD_COMPLETE.md** | Project completion summary | 5 min |
| **INDEX.md** | This file - file organization | 5 min |

### 💾 Database Layer
```
database/
├── db_schema.py          # SQLite schema creation & tables
│   └── 14 tables, setup functions
```

### 📊 Data Simulation
```
data_simulator/
├── simulate_data.py      # Generates realistic operational data
│   ├── areas, stores, products
│   ├── customers, orders
│   ├── deliveries, inventory
│   └── 1500+ records total
└── __pycache__/
```

### 🎯 Eight Intelligence Engines
```
engines/
├── __init__.py                   # Package initialization
├── sql_analytics.py              # 📈 SQL Analytics Engine
│   └── 10+ BI queries
├── demand_forecasting.py         # 🔮 Demand Forecasting Engine
│   └── 7-day predictions
├── delivery_prediction.py        # ⏱️ Delivery Prediction Engine
│   └── SLA optimization
├── inventory_optimization.py     # 📦 Inventory Optimization Engine
│   └── ABC analysis, EOQ, reorder points
├── location_optimization.py      # 🗺️ Location Optimization Engine
│   └── Expansion analysis
└── profit_simulation.py          # 💰 Profit Simulation Engine
    └── What-if scenarios
```

### 🔌 API Backend
```
api/
└── main.py                       # FastAPI backend
    ├── 30+ REST endpoints
    ├── Auto-generated docs
    └── CORS enabled
```

### 🎨 Dashboard Frontend
```
dashboard/
└── app.py                        # Streamlit dashboard
    ├── 8 interactive modules
    ├── Real-time charts
    └── Scenario simulations
```

### 📓 Notebooks
```
notebooks/
└── (exploratory analysis space)
```

---

## 🚀 Common Tasks & Files

### "I want to start right now"
1. Run: `python main.py`
2. Select: 1 (Initialize DB)
3. Select: 2 (Generate Data)
4. Select: 9 (Run All Engines)

### "I want to understand the architecture"
→ Read: `ARCHITECTURE.md`

### "I want API documentation"
→ Open: `http://localhost:8000/docs` (after starting API)

### "I want to see the database schema"
→ Read: `database/db_schema.py`

### "I want to run individual engines"
```python
# SQL Analytics
from engines.sql_analytics import print_analytics
print_analytics()

# Demand Forecasting
from engines.demand_forecasting import run_demand_forecasting
run_demand_forecasting()

# Etc. for other engines...
```

### "I want to modify the configuration"
→ Edit: `config.py`

### "I want to add more features"
→ Add to: `engines/` directory

### "I want to verify system integrity"
→ Run: `python verify_system.py`

---

## 📊 Component Mapping

### Data Flow
```
main.py (Menu)
    ↓
├─→ database/db_schema.py (Create DB)
│
├─→ data_simulator/simulate_data.py (Generate Data)
│
├─→ engines/* (Run Engines)
│   ├─→ sql_analytics.py
│   ├─→ demand_forecasting.py
│   ├─→ delivery_prediction.py
│   ├─→ inventory_optimization.py
│   ├─→ location_optimization.py
│   └─→ profit_simulation.py
│
├─→ api/main.py (Start API)
│   └─→ All engines (for REST calls)
│
└─→ dashboard/app.py (Start Dashboard)
    └─→ All engines (for visualizations)
```

### Import Chain
```
main.py
  ├── database.db_schema
  ├── data_simulator.simulate_data
  └── engines.*
      ├── sql_analytics
      ├── demand_forecasting
      ├── delivery_prediction
      ├── inventory_optimization
      ├── location_optimization
      └── profit_simulation

api/main.py
  └── all engines

dashboard/app.py
  └── all engines
```

---

## 🎯 Use Cases → Files

| Use Case | File(s) |
|----------|---------|
| Monitor store performance | `engines/sql_analytics.py`, `dashboard/app.py` |
| Predict demand | `engines/demand_forecasting.py` |
| Optimize inventory | `engines/inventory_optimization.py` |
| Improve delivery | `engines/delivery_prediction.py` |
| Find expansion sites | `engines/location_optimization.py` |
| Simulate profit | `engines/profit_simulation.py` |
| Use via API | `api/main.py` |
| View dashboard | `dashboard/app.py` |
| Configure system | `config.py` |

---

## 📈 Learning Path

### Beginner (Understanding)
1. Read: `README.md`
2. Read: `QUICKSTART.md`
3. Run: `python main.py` (options 1-2)
4. View: Dashboard

### Intermediate (Extending)
1. Read: `ARCHITECTURE.md`
2. Review: `engines/` directory structure
3. Modify: `config.py`
4. Run individual engines

### Advanced (Customizing)
1. Read: `database/db_schema.py`
2. Understand: Data model
3. Modify: Engine logic
4. Add: New endpoints to `api/main.py`
5. Deploy: To cloud

---

## 🔍 File Dependencies

```
main.py
  ├─ (none)

database/db_schema.py
  └─ sqlite3

data_simulator/simulate_data.py
  ├─ database/db_schema.py
  ├─ random
  └─ datetime

engines/sql_analytics.py
  ├─ database/db_schema.py
  ├─ pandas
  └─ sqlite3

engines/demand_forecasting.py
  ├─ database/db_schema.py
  ├─ pandas
  └─ numpy

engines/delivery_prediction.py
  ├─ database/db_schema.py
  ├─ pandas
  └─ numpy

engines/inventory_optimization.py
  ├─ database/db_schema.py
  ├─ pandas
  └─ numpy

engines/location_optimization.py
  ├─ database/db_schema.py
  ├─ pandas
  └─ numpy

engines/profit_simulation.py
  ├─ database/db_schema.py
  ├─ pandas
  ├─ numpy
  └─ json

api/main.py
  ├─ fastapi
  ├─ database/db_schema.py
  └─ all engines

dashboard/app.py
  ├─ streamlit
  ├─ plotly
  └─ all engines
```

---

## 💡 Quick Reference

### Start System
```bash
python main.py
```

### Verify Install
```bash
python verify_system.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Start API
```bash
python -m uvicorn api.main:app --reload
# Then open: http://localhost:8000/docs
```

### Start Dashboard
```bash
streamlit run dashboard/app.py
# Then open: http://localhost:8501
```

---

## 📞 Support

### Can't Find Something?
- Check: `QUICKSTART.md`
- Check: `README.md`
- Check: File index below

### Need More Details?
- Full architecture: `ARCHITECTURE.md`
- Complete guide: `README.md`
- Quick start: `QUICKSTART.md`

### Want to Understand Code?
- Engine logic: `engines/*.py`
- Database: `database/db_schema.py`
- Data generation: `data_simulator/simulate_data.py`

---

## 📋 Complete File List (29 Files)

```
1. main.py                          ← START HERE
2. verify_system.py                 ← Verification
3. config.py                        ← Configuration
4. requirements.txt                 ← Dependencies

5. README.md                        ← Full docs
6. QUICKSTART.md                    ← Quick setup
7. SYSTEM_SUMMARY.md               ← Project overview
8. ARCHITECTURE.md                 ← Visual guide
9. BUILD_COMPLETE.md               ← Completion report
10. INDEX.md                        ← This file

11. database/db_schema.py           ← Database setup

12. data_simulator/simulate_data.py ← Data generation

13. engines/__init__.py             ← Package init
14. engines/sql_analytics.py        ← Analytics
15. engines/demand_forecasting.py   ← Forecasting
16. engines/delivery_prediction.py  ← Delivery
17. engines/inventory_optimization.py ← Inventory
18. engines/location_optimization.py ← Location
19. engines/profit_simulation.py    ← Simulation

20. api/main.py                     ← API Backend

21. dashboard/app.py                ← Dashboard

22. darkstore.db                    ← Database (created at runtime)

+ various __pycache__ directories (auto-created)
```

---

## 🎯 Interview Preparation Map

```
Topic              → Files to Review
─────────────────────────────────────
System Overview    → SYSTEM_SUMMARY.md
Architecture       → ARCHITECTURE.md
Business Logic     → engines/*.py
Data Model         → database/db_schema.py
API Design         → api/main.py
UI/UX              → dashboard/app.py
Configuration      → config.py
Deployment         → QUICKSTART.md
```

---

## ✨ Key Files to Show Interviewers

1. **Architecture**: Show `ARCHITECTURE.md`
2. **Code Structure**: Show `engines/` directory
3. **Database**: Show `database/db_schema.py`
4. **API**: Show `api/main.py`
5. **Results**: Show `dashboard/app.py` running
6. **Completeness**: Show `BUILD_COMPLETE.md`

---

## 🚀 Next Steps

1. ✅ Read this file (INDEX.md)
2. ✅ Read QUICKSTART.md
3. ✅ Run `python main.py`
4. ✅ Explore the system
5. ✅ Run `python -m uvicorn api.main:app --reload`
6. ✅ Run `streamlit run dashboard/app.py`
7. ✅ Review code in `engines/`
8. ✅ Prepare for interview

---

**Navigation Guide**: INDEX.md  
**Last Updated**: February 17, 2024  
**Status**: ✅ Complete  
**Ready for**: Immediate Use
