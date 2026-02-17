"""
FastAPI Backend - REST API for Smart DarkStore Intelligence
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_schema import get_db_connection
from engines.sql_analytics import SQLAnalytics
from engines.demand_forecasting import DemandForecastingEngine
from engines.delivery_prediction import DeliveryTimePredictionEngine
from engines.inventory_optimization import InventoryOptimizationEngine
from engines.location_optimization import LocationOptimizationEngine
from engines.profit_simulation import ProfitSimulationEngine

# Create FastAPI app
app = FastAPI(
    title="Smart DarkStore Intelligence API",
    description="AI-powered operations management system for dark stores",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============= Pydantic Models =============
class StorePerformance(BaseModel):
    store_id: int
    store_name: str
    total_orders: int
    total_revenue: float
    avg_order_value: float
    delivery_time_avg: float


class AreaDemand(BaseModel):
    area_id: int
    area_name: str
    total_customers: int
    total_orders: int
    area_revenue: float


class DemandForecast(BaseModel):
    store_id: int
    product_id: int
    product_name: str
    forecast_date: str
    forecasted_quantity: int
    confidence: float


class DeliveryMetrics(BaseModel):
    store_id: int
    store_name: str
    avg_delivery_time: float
    sla_compliance: float
    avg_rating: float


class InventoryAlert(BaseModel):
    store_id: int
    store_name: str
    product_id: int
    product_name: str
    quantity_on_hand: int
    reorder_point: int
    status: str


# ============= Utility Endpoints =============
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Smart DarkStore Intelligence API"}


# ============= Store Performance Endpoints =============
@app.get("/api/stores/performance")
def get_store_performance(days: int = Query(30, ge=1, le=365)):
    """Get store performance metrics"""
    try:
        analytics = SQLAnalytics()
        df = analytics.store_performance_summary(days=days)
        analytics.close()
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stores/{store_id}/profitability")
def get_store_profitability(store_id: int):
    """Get store profitability metrics"""
    try:
        analytics = SQLAnalytics()
        df = analytics.profitability_by_store()
        analytics.close()
        store_data = df[df['store_id'] == store_id].to_dict(orient="records")
        return store_data[0] if store_data else {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============= Area & Demand Endpoints =============
@app.get("/api/areas/demand")
def get_area_demand():
    """Get demand analysis by area"""
    try:
        analytics = SQLAnalytics()
        df = analytics.area_demand_analysis()
        analytics.close()
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/areas/expansion-opportunities")
def get_expansion_opportunities():
    """Get area expansion opportunities"""
    try:
        engine = LocationOptimizationEngine()
        df = engine.expansion_roi_estimate()
        engine.close()
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/areas/coverage-gaps")
def get_coverage_gaps():
    """Get coverage gap analysis"""
    try:
        engine = LocationOptimizationEngine()
        df = engine.coverage_gap_analysis()
        engine.close()
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============= Demand Forecasting Endpoints =============
@app.get("/api/forecast/demand")
def get_demand_forecast(store_id: Optional[int] = None, days: int = Query(7, ge=1, le=30)):
    """Get demand forecast"""
    try:
        engine = DemandForecastingEngine()
        df = engine.get_forecast_summary()
        engine.close()

        if store_id:
            df = df[df['store_id'] == store_id]

        return df.head(days * 50).to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/forecast/demand/{store_id}/{product_id}")
def get_product_forecast(store_id: int, product_id: int):
    """Get demand forecast for specific product"""
    try:
        engine = DemandForecastingEngine()
        forecast = engine.forecast_for_store_product(store_id, product_id, forecast_days=7)
        engine.close()
        return forecast if forecast else {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============= Delivery Endpoints =============
@app.get("/api/delivery/performance")
def get_delivery_performance():
    """Get delivery performance and SLA"""
    try:
        analytics = SQLAnalytics()
        df = analytics.delivery_performance_sla(target_minutes=30)
        analytics.close()
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/delivery/predictions")
def get_delivery_predictions():
    """Get delivery time predictions"""
    try:
        engine = DeliveryTimePredictionEngine()
        df = engine.get_predictions_summary()
        engine.close()
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/delivery/sla-achievability")
def get_sla_achievability(target_minutes: int = Query(30, ge=10, le=60)):
    """Get SLA achievability analysis"""
    try:
        engine = DeliveryTimePredictionEngine()
        df = engine.sla_achievability_analysis(target_minutes=target_minutes)
        engine.close()
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============= Inventory Endpoints =============
@app.get("/api/inventory/status")
def get_inventory_status():
    """Get inventory status across stores"""
    try:
        analytics = SQLAnalytics()
        df = analytics.inventory_status()
        analytics.close()
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/inventory/optimization")
def get_inventory_optimization():
    """Get inventory optimization recommendations"""
    try:
        engine = InventoryOptimizationEngine()
        df = engine.stockout_risk_analysis()
        engine.close()
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/inventory/abc-analysis")
def get_abc_analysis():
    """Get ABC inventory analysis"""
    try:
        engine = InventoryOptimizationEngine()
        df = engine.abc_analysis()
        engine.close()
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/inventory/efficiency")
def get_inventory_efficiency():
    """Get inventory efficiency metrics"""
    try:
        engine = InventoryOptimizationEngine()
        df = engine.inventory_efficiency_metrics()
        engine.close()
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============= Product Endpoints =============
@app.get("/api/products/sales")
def get_product_sales_analysis():
    """Get product sales analysis"""
    try:
        analytics = SQLAnalytics()
        df = analytics.product_sales_analysis()
        analytics.close()
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============= Profit Simulation Endpoints =============
@app.get("/api/simulation/pricing")
def simulate_pricing_change(percentage: int = Query(10, ge=1, le=50)):
    """Simulate pricing change impact"""
    try:
        engine = ProfitSimulationEngine()
        df = engine.simulate_pricing_changes(price_increase_percentage=percentage)
        engine.close()
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/simulation/inventory")
def simulate_inventory_reduction(reduction_percentage: int = Query(20, ge=5, le=50)):
    """Simulate inventory reduction impact"""
    try:
        engine = ProfitSimulationEngine()
        df = engine.simulate_inventory_reduction(reduction_percentage=reduction_percentage)
        engine.close()
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/simulation/new-store/{area_id}")
def simulate_new_store(area_id: int, monthly_revenue: float = Query(50000, ge=10000, le=500000)):
    """Simulate new store expansion"""
    try:
        engine = ProfitSimulationEngine()
        result = engine.simulate_new_store_expansion(area_id, estimated_monthly_revenue=monthly_revenue)
        engine.close()
        return result if result else {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============= Customer Endpoints =============
@app.get("/api/customers/insights")
def get_customer_insights():
    """Get customer behavior insights"""
    try:
        analytics = SQLAnalytics()
        df = analytics.customer_insights()
        analytics.close()
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============= Analytics Dashboard Endpoints =============
@app.get("/api/dashboard/kpis")
def get_dashboard_kpis():
    """Get key performance indicators for dashboard"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get KPIs
        kpis = {}

        cursor.execute("SELECT COUNT(*) FROM stores")
        kpis['total_stores'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM orders")
        kpis['total_orders'] = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(total_amount) FROM orders")
        result = cursor.fetchone()
        kpis['total_revenue'] = result[0] if result[0] else 0

        cursor.execute("SELECT AVG(total_amount) FROM orders")
        result = cursor.fetchone()
        kpis['avg_order_value'] = result[0] if result[0] else 0

        cursor.execute("SELECT COUNT(DISTINCT area_id) FROM stores")
        kpis['areas_served'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM customers")
        kpis['registered_customers'] = cursor.fetchone()[0]

        conn.close()
        return kpis

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dashboard/summary")
def get_dashboard_summary():
    """Get comprehensive dashboard summary"""
    try:
        analytics = SQLAnalytics()

        summary = {
            'stores': analytics.store_performance_summary(days=30).head(5).to_dict(orient="records"),
            'areas': analytics.area_demand_analysis().head(5).to_dict(orient="records"),
            'products': analytics.product_sales_analysis().head(5).to_dict(orient="records"),
            'delivery': analytics.delivery_performance_sla().head(5).to_dict(orient="records")
        }

        analytics.close()
        return summary

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
