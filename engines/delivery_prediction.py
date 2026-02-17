"""
Delivery Time Prediction Engine - Predicts delivery times based on historical patterns
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_schema import get_db_connection


class DeliveryTimePredictionEngine:
    """Predict delivery times using historical data and patterns"""

    def __init__(self):
        self.conn = get_db_connection()

    def get_historical_delivery_data(self):
        """Get historical delivery data"""
        query = """
        SELECT 
            d.delivery_id,
            s.store_id,
            a.area_id,
            CAST(strftime('%H', o.order_time) AS INTEGER) as order_hour,
            CAST(strftime('%w', o.order_date) AS INTEGER) as day_of_week,
            d.delivery_time_minutes,
            d.distance_km,
            d.delivery_status,
            d.rating
        FROM deliveries d
        JOIN orders o ON d.order_id = o.order_id
        JOIN stores s ON d.store_id = s.store_id
        JOIN customers c ON d.customer_id = c.customer_id
        JOIN areas a ON c.area_id = a.area_id
        WHERE d.delivery_time_minutes IS NOT NULL
        AND d.delivery_time_minutes > 0
        """
        return pd.read_sql_query(query, self.conn)

    def analyze_delivery_patterns(self):
        """Analyze delivery time patterns by hour and day"""
        df = self.get_historical_delivery_data()

        if df.empty:
            return {}

        patterns = {}

        for store_id in df['store_id'].unique():
            for area_id in df['area_id'].unique():
                store_area_data = df[(df['store_id'] == store_id) & (df['area_id'] == area_id)]

                if store_area_data.empty:
                    continue

                for hour in range(24):
                    for day in range(7):
                        hour_day_data = store_area_data[
                            (store_area_data['order_hour'] == hour) &
                            (store_area_data['day_of_week'] == day)
                        ]

                        if not hour_day_data.empty:
                            avg_time = hour_day_data['delivery_time_minutes'].mean()
                            std_time = hour_day_data['delivery_time_minutes'].std()
                            count = len(hour_day_data)

                            key = (store_id, area_id, hour, day)
                            patterns[key] = {
                                'avg_time': avg_time,
                                'std_time': std_time if pd.notna(std_time) else avg_time * 0.1,
                                'count': count,
                                'confidence': min(1.0, count / 10)  # More data = higher confidence
                            }

        return patterns

    def predict_delivery_time(self, store_id, area_id, order_hour, day_of_week):
        """Predict delivery time for specific parameters"""
        patterns = self.analyze_delivery_patterns()
        key = (store_id, area_id, order_hour, day_of_week)

        if key in patterns:
            pattern = patterns[key]
            predicted_time = pattern['avg_time']
            confidence = pattern['confidence']
        else:
            # Fallback to store average
            store_patterns = {k: v for k, v in patterns.items() if k[0] == store_id}
            if store_patterns:
                avg_times = [v['avg_time'] for v in store_patterns.values()]
                predicted_time = np.mean(avg_times)
                confidence = 0.5
            else:
                # Global average
                all_patterns = patterns.values()
                if all_patterns:
                    avg_times = [v['avg_time'] for v in all_patterns]
                    predicted_time = np.mean(avg_times)
                    confidence = 0.3
                else:
                    predicted_time = 30  # Default estimate
                    confidence = 0.1

        return {
            'predicted_delivery_time': predicted_time,
            'confidence_score': confidence,
            'estimated_range_min': predicted_time * 0.8,
            'estimated_range_max': predicted_time * 1.2
        }

    def save_predictions_to_db(self):
        """Save delivery time predictions to database"""
        patterns = self.analyze_delivery_patterns()
        cursor = self.conn.cursor()

        count = 0
        for (store_id, area_id, hour, day), pattern in patterns.items():
            cursor.execute(
                """INSERT OR REPLACE INTO delivery_predictions
                (store_id, area_id, order_hour, day_of_week, predicted_delivery_time,
                 confidence_score, model_version)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (store_id, area_id, hour, day, pattern['avg_time'],
                 pattern['confidence'], 'v1.0')
            )
            count += 1

        self.conn.commit()
        print(f"✓ Saved {count} delivery time predictions")

    def get_predictions_summary(self):
        """Get summary of delivery predictions"""
        query = """
        SELECT 
            s.store_id,
            s.store_name,
            a.area_name,
            dp.order_hour,
            CASE dp.day_of_week
                WHEN 0 THEN 'Sunday'
                WHEN 1 THEN 'Monday'
                WHEN 2 THEN 'Tuesday'
                WHEN 3 THEN 'Wednesday'
                WHEN 4 THEN 'Thursday'
                WHEN 5 THEN 'Friday'
                WHEN 6 THEN 'Saturday'
            END as day_name,
            ROUND(dp.predicted_delivery_time, 1) as predicted_minutes,
            ROUND(dp.confidence_score * 100, 1) as confidence_percentage
        FROM delivery_predictions dp
        JOIN stores s ON dp.store_id = s.store_id
        JOIN areas a ON dp.area_id = a.area_id
        ORDER BY s.store_id, dp.day_of_week, dp.order_hour
        """
        return pd.read_sql_query(query, self.conn)

    def sla_achievability_analysis(self, target_minutes=30):
        """Analyze SLA achievability based on predictions"""
        query = f"""
        SELECT 
            s.store_id,
            s.store_name,
            COUNT(DISTINCT (dp.day_of_week || '_' || dp.order_hour)) as total_slots,
            COUNT(DISTINCT CASE WHEN dp.predicted_delivery_time <= {target_minutes} 
                THEN (dp.day_of_week || '_' || dp.order_hour) END) as achievable_slots,
            ROUND(100.0 * COUNT(DISTINCT CASE WHEN dp.predicted_delivery_time <= {target_minutes} 
                THEN (dp.day_of_week || '_' || dp.order_hour) END) / 
                COUNT(DISTINCT (dp.day_of_week || '_' || dp.order_hour)), 2) as sla_achievability_rate
        FROM delivery_predictions dp
        JOIN stores s ON dp.store_id = s.store_id
        GROUP BY s.store_id, s.store_name
        ORDER BY sla_achievability_rate DESC
        """
        return pd.read_sql_query(query, self.conn)

    def close(self):
        """Close database connection"""
        self.conn.close()


def run_delivery_prediction():
    """Run delivery time prediction engine"""
    engine = DeliveryTimePredictionEngine()

    print("\n⏱️  Delivery Time Prediction Engine")
    print("-" * 60)

    # Save predictions
    engine.save_predictions_to_db()

    # Display SLA analysis
    print("\n📊 SLA Achievability (Target: 30 minutes)")
    print("=" * 100)
    sla_analysis = engine.sla_achievability_analysis(target_minutes=30)
    print(sla_analysis.to_string(index=False))

    # Display predictions summary
    print("\n📍 Delivery Time Predictions by Store & Time")
    print("=" * 120)
    summary = engine.get_predictions_summary()
    print(summary.head(30).to_string(index=False))

    engine.close()


if __name__ == "__main__":
    run_delivery_prediction()
