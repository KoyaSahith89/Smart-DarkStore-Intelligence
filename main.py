"""
Main Orchestration Script - Coordinates all engines and systems
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database.db_schema import create_database
from data_simulator.simulate_data import simulate_all
from engines.sql_analytics import print_analytics
from engines.demand_forecasting import run_demand_forecasting
from engines.delivery_prediction import run_delivery_prediction
from engines.inventory_optimization import run_inventory_optimization
from engines.location_optimization import run_location_optimization
from engines.profit_simulation import run_profit_simulation


def main():
    """Main orchestration function"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║      🏪 SMART DARKSTORE INTELLIGENCE SYSTEM 🏪               ║
    ║         AI-Powered Dark Store Operations Platform             ║
    ║                    Version 1.0.0                              ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)

    print("\n📋 System Components:")
    print("  ✓ 8 Engines (Data, Analytics, Forecasting, etc.)")
    print("  ✓ SQLite Database")
    print("  ✓ FastAPI Backend")
    print("  ✓ Streamlit Dashboard")
    print("  ✓ REST API")

    while True:
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("1. Initialize Database")
        print("2. Run Data Simulation")
        print("3. Run SQL Analytics")
        print("4. Run Demand Forecasting Engine")
        print("5. Run Delivery Prediction Engine")
        print("6. Run Inventory Optimization Engine")
        print("7. Run Location Optimization Engine")
        print("8. Run Profit Simulation Engine")
        print("9. Run All Engines")
        print("10. View API Documentation")
        print("11. Start Dashboard")
        print("12. Quick Demo")
        print("0. Exit")
        print("="*60)

        choice = input("Select option: ").strip()

        if choice == "1":
            print("\n🔧 Initializing database schema...")
            create_database()

        elif choice == "2":
            print("\n📊 Running data simulation...")
            simulate_all()

        elif choice == "3":
            print("\n📈 Running SQL analytics...")
            print_analytics()

        elif choice == "4":
            print("\n🔮 Running demand forecasting...")
            run_demand_forecasting()

        elif choice == "5":
            print("\n⏱️  Running delivery prediction...")
            run_delivery_prediction()

        elif choice == "6":
            print("\n📦 Running inventory optimization...")
            run_inventory_optimization()

        elif choice == "7":
            print("\n🗺️  Running location optimization...")
            run_location_optimization()

        elif choice == "8":
            print("\n💰 Running profit simulation...")
            run_profit_simulation()

        elif choice == "9":
            print("\n🚀 Running all engines...\n")
            create_database()
            simulate_all()
            print_analytics()
            run_demand_forecasting()
            run_delivery_prediction()
            run_inventory_optimization()
            run_location_optimization()
            run_profit_simulation()
            print("\n✓ All engines completed!")

        elif choice == "10":
            print("""
            📚 API DOCUMENTATION
            
            API runs on: http://localhost:8000
            Swagger UI: http://localhost:8000/docs
            ReDoc: http://localhost:8000/redoc
            
            Key Endpoints:
            
            STORES:
              GET /api/stores/performance - Store performance metrics
              GET /api/stores/{store_id}/profitability - Store profitability
              
            AREAS:
              GET /api/areas/demand - Area demand analysis
              GET /api/areas/expansion-opportunities - Expansion ROI
              GET /api/areas/coverage-gaps - Coverage gap analysis
              
            DEMAND:
              GET /api/forecast/demand - Demand forecast
              GET /api/forecast/demand/{store_id}/{product_id} - Product forecast
              
            DELIVERY:
              GET /api/delivery/performance - Delivery SLA
              GET /api/delivery/predictions - Delivery time predictions
              GET /api/delivery/sla-achievability - SLA achievability
              
            INVENTORY:
              GET /api/inventory/status - Inventory status
              GET /api/inventory/optimization - Optimization recommendations
              GET /api/inventory/abc-analysis - ABC analysis
              GET /api/inventory/efficiency - Efficiency metrics
              
            PRODUCTS:
              GET /api/products/sales - Product sales analysis
              
            PROFIT:
              GET /api/simulation/pricing/{percentage} - Pricing simulation
              GET /api/simulation/inventory/{reduction} - Inventory simulation
              GET /api/simulation/new-store/{area_id} - New store simulation
              
            CUSTOMERS:
              GET /api/customers/insights - Customer insights
              
            DASHBOARD:
              GET /api/dashboard/kpis - KPI summary
              GET /api/dashboard/summary - Full dashboard summary
            
            To start API:
            $ python -m uvicorn api.main:app --reload
            """)

        elif choice == "11":
            print("""
            🎨 Starting Streamlit Dashboard...
            
            Run this command in a new terminal:
            $ streamlit run dashboard/app.py
            
            Dashboard will open at: http://localhost:8501
            """)

        elif choice == "12":
            print("\n⚡ Quick Demo - Running complete workflow...\n")
            print("1️⃣  Creating database schema...")
            create_database()
            print("\n2️⃣  Simulating realistic data...")
            simulate_all()
            print("\n3️⃣  Running analytics...")
            print_analytics()
            print("\n✓ Demo completed! Start the API or Dashboard to explore.")

        elif choice == "0":
            print("\n👋 Exiting Smart DarkStore Intelligence. Goodbye!")
            break

        else:
            print("❌ Invalid option. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 System interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
