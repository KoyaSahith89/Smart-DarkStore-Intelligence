"""
Demand Forecasting Engine - Predicts future demand using time series analysis
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_schema import get_db_connection


class DemandForecastingEngine:
    """Forecast product demand using multiple methods"""

    def __init__(self):
        self.conn = get_db_connection()

    def get_historical_demand(self, store_id=None, product_id=None, days=30):
        """Get historical demand data"""
        query = """
        SELECT 
            DATE(o.order_date) as order_date,
            oi.product_id,
            p.product_name,
            p.category,
            s.store_id,
            s.store_name,
            SUM(oi.quantity) as daily_quantity,
            SUM(oi.line_total) as daily_revenue
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        JOIN products p ON oi.product_id = p.product_id
        JOIN stores s ON o.store_id = s.store_id
        WHERE DATE(o.order_date) >= DATE('now', '-{} days')
        """.format(days)

        if store_id:
            query += f" AND s.store_id = {store_id}"
        if product_id:
            query += f" AND p.product_id = {product_id}"

        query += " GROUP BY DATE(o.order_date), oi.product_id, s.store_id ORDER BY order_date DESC"
        return pd.read_sql_query(query, self.conn)

    def simple_exponential_smoothing(self, data, alpha=0.3, forecast_days=7):
        """Simple exponential smoothing for demand forecasting"""
        forecast = []
        if len(data) == 0:
            return [0] * forecast_days

        last_value = data[-1]
        for _ in range(forecast_days):
            forecast.append(last_value)
        return forecast

    def moving_average_forecast(self, data, window=7, forecast_days=7):
        """Moving average based forecast"""
        if len(data) < window:
            window = len(data)

        ma = np.mean(data[-window:])
        forecast = [ma] * forecast_days
        return forecast

    def trend_based_forecast(self, data, forecast_days=7):
        """Forecast with trend analysis"""
        if len(data) < 2:
            return [data[0] if data else 0] * forecast_days

        x = np.arange(len(data))
        y = np.array(data)

        # Calculate trend
        coeffs = np.polyfit(x, y, 1)
        trend = coeffs[0]
        intercept = coeffs[1]

        # Generate forecast
        forecast = []
        for i in range(forecast_days):
            predicted = intercept + trend * (len(data) + i)
            forecast.append(max(0, predicted))  # Ensure non-negative

        return forecast

    def forecast_for_store_product(self, store_id, product_id, forecast_days=7):
        """Generate demand forecast for specific store-product combination"""
        demand_data = self.get_historical_demand(store_id=store_id, product_id=product_id, days=30)

        if demand_data.empty:
            return None

        quantities = demand_data['daily_quantity'].values
        product_name = demand_data['product_name'].iloc[0]

        # Generate three forecasts
        ses_forecast = self.simple_exponential_smoothing(quantities, forecast_days=forecast_days)
        ma_forecast = self.moving_average_forecast(quantities, window=7, forecast_days=forecast_days)
        trend_forecast = self.trend_based_forecast(quantities, forecast_days=forecast_days)

        # Ensemble forecast (average of three methods)
        ensemble_forecast = np.mean([ses_forecast, ma_forecast, trend_forecast], axis=0)

        # Calculate confidence intervals
        std_dev = np.std(quantities)
        confidence_lower = ensemble_forecast - (1.96 * std_dev)
        confidence_upper = ensemble_forecast + (1.96 * std_dev)

        return {
            'store_id': store_id,
            'product_id': product_id,
            'product_name': product_name,
            'historical_avg': np.mean(quantities),
            'forecast': [max(0, int(f)) for f in ensemble_forecast],
            'confidence_lower': [max(0, int(f)) for f in confidence_lower],
            'confidence_upper': [max(0, int(f)) for f in confidence_upper],
            'forecast_method': 'ensemble'
        }

    def generate_all_forecasts(self, forecast_days=7):
        """Generate forecasts for all store-product combinations"""
        cursor = self.conn.cursor()

        # Get all store-product combinations with recent activity
        cursor.execute("""
        SELECT DISTINCT 
            s.store_id, 
            p.product_id
        FROM stores s
        CROSS JOIN products p
        WHERE EXISTS (
            SELECT 1 FROM orders o 
            JOIN order_items oi ON o.order_id = oi.order_id
            WHERE o.store_id = s.store_id 
            AND oi.product_id = p.product_id
            AND DATE(o.order_date) >= DATE('now', '-30 days')
        )
        """)

        combinations = cursor.fetchall()
        forecasts = []

        for store_id, product_id in combinations:
            forecast = self.forecast_for_store_product(store_id, product_id, forecast_days)
            if forecast:
                forecasts.append(forecast)

        return forecasts

    def save_forecasts_to_db(self, forecast_days=7):
        """Save forecasts to database"""
        forecasts = self.generate_all_forecasts(forecast_days)
        cursor = self.conn.cursor()

        base_date = datetime.now().date()

        for forecast in forecasts:
            for day_offset in range(forecast_days):
                forecast_date = base_date + timedelta(days=day_offset+1)
                forecasted_qty = forecast['forecast'][day_offset]
                lower = forecast['confidence_lower'][day_offset]
                upper = forecast['confidence_upper'][day_offset]

                cursor.execute(
                    """INSERT OR REPLACE INTO demand_forecast 
                    (store_id, product_id, forecast_date, forecasted_quantity, 
                     forecast_model, confidence_interval_lower, confidence_interval_upper)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (forecast['store_id'], forecast['product_id'], forecast_date,
                     forecasted_qty, forecast['forecast_method'], int(lower), int(upper))
                )

        self.conn.commit()
        print(f"✓ Saved {len(forecasts)} demand forecasts for {forecast_days} days ahead")

    def get_forecast_summary(self):
        """Get summary of current forecasts"""
        query = """
        SELECT 
            s.store_id,
            s.store_name,
            p.product_id,
            p.product_name,
            p.category,
            df.forecast_date,
            df.forecasted_quantity,
            df.confidence_interval_lower,
            df.confidence_interval_upper,
            df.forecast_model
        FROM demand_forecast df
        JOIN stores s ON df.store_id = s.store_id
        JOIN products p ON df.product_id = p.product_id
        WHERE df.forecast_date >= DATE('now')
        ORDER BY df.forecast_date, s.store_id
        """
        return pd.read_sql_query(query, self.conn)

    def close(self):
        """Close database connection"""
        self.conn.close()


def run_demand_forecasting():
    """Run demand forecasting engine"""
    engine = DemandForecastingEngine()

    print("\n🔮 Demand Forecasting Engine")
    print("-" * 60)

    # Generate and save forecasts
    engine.save_forecasts_to_db(forecast_days=7)

    # Display summary
    print("\n📊 Forecast Summary (Next 7 Days)")
    print("=" * 120)
    summary = engine.get_forecast_summary()
    print(summary.head(20).to_string(index=False))

    engine.close()


if __name__ == "__main__":
    run_demand_forecasting()
