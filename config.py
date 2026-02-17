"""
System Configuration & Constants
"""
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATABASE_PATH = PROJECT_ROOT / "darkstore.db"
DATA_SIMULATOR_PATH = PROJECT_ROOT / "data_simulator"
ENGINES_PATH = PROJECT_ROOT / "engines"
API_PATH = PROJECT_ROOT / "api"
DASHBOARD_PATH = PROJECT_ROOT / "dashboard"

# Database configuration
DATABASE_CONFIG = {
    "type": "sqlite",
    "path": str(DATABASE_PATH),
    "echo": False,
    "pool_size": 10,
    "max_overflow": 20
}

# Data simulation parameters
SIMULATION_CONFIG = {
    "num_areas": 5,
    "num_stores_per_area": 2,
    "num_products": 50,
    "num_customers_per_area": 50,
    "num_days": 30,
    "num_orders_per_day": 50
}

# Forecasting parameters
FORECASTING_CONFIG = {
    "forecast_days": 7,
    "alpha": 0.3,  # Exponential smoothing parameter
    "window": 7,  # Moving average window
    "confidence_level": 0.95
}

# Delivery prediction parameters
DELIVERY_CONFIG = {
    "target_sla_minutes": 30,
    "distance_factor": 2,  # Cost per km
    "avg_delivery_km": 5
}

# Inventory optimization parameters
INVENTORY_CONFIG = {
    "order_cost": 100,  # $ per order
    "holding_cost_rate": 0.25,  # 25% annual
    "lead_time_days": 3,
    "safety_stock_days": 2
}

# Location optimization parameters
LOCATION_CONFIG = {
    "initial_investment": 500000,
    "gross_margin": 0.40,
    "operational_cost_percentage": 0.15,
    "monthly_operating_cost": 30000
}

# Profit simulation parameters
PROFIT_CONFIG = {
    "gross_margin": 0.40,
    "cogs_percentage": 0.60,
    "operational_cost_percentage": 0.15,
    "delivery_cost_per_km": 2,
    "initial_store_investment": 500000,
    "ramp_up_months": 3,
    "price_elasticity": -1.2
}

# API configuration
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "reload": True,
    "title": "Smart DarkStore Intelligence API",
    "version": "1.0.0"
}

# Dashboard configuration
DASHBOARD_CONFIG = {
    "page_icon": "🏪",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Business logic constants
BUSINESS_CONSTANTS = {
    "average_order_value": 250,
    "avg_delivery_rating": 4.2,
    "target_sla_compliance": 0.85,
    "abc_threshold_a": 0.80,
    "abc_threshold_b": 0.95,
    "reorder_point_factor": 1.5,
    "max_stock_factor": 10
}

# Expansion criteria
EXPANSION_CRITERIA = {
    "high_priority_threshold": 70,
    "medium_priority_threshold": 50,
    "population_per_store_critical": 100000,
    "population_per_store_high": 50000,
    "minimum_roi": 30
}
