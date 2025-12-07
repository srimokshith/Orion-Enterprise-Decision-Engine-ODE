import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

def prepare_shipment_features(shipments_df, routes_df):
    """Prepare features for delay prediction"""
    df = shipments_df.merge(routes_df, on='route_id', how='left')
    
    df['planned_departure'] = pd.to_datetime(df['planned_departure'])
    df['hour_of_day'] = df['planned_departure'].dt.hour
    df['day_of_week'] = df['planned_departure'].dt.dayofweek
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    
    # Historical delay by route
    route_delay_avg = df.groupby('route_id')['delay_minutes'].mean().to_dict()
    df['route_avg_delay'] = df['route_id'].map(route_delay_avg)
    
    features = ['distance_km', 'avg_time_mins', 'hour_of_day', 'day_of_week', 
                'is_weekend', 'route_avg_delay']
    
    return df, features

def train_delay_predictor(shipments_df, routes_df):
    """Train model to predict shipment delays using Random Forest"""
    df, features = prepare_shipment_features(shipments_df, routes_df)
    
    df = df.dropna(subset=features + ['delay_minutes'])
    X = df[features]
    y = df['delay_minutes']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    return model, {'mae': mae, 'r2': r2}, features

def predict_route_delays(model, routes_df, features):
    """Predict delays for all routes"""
    test_data = []
    for _, route in routes_df.iterrows():
        for hour in [8, 14, 18]:
            test_data.append({
                'route_id': route['route_id'],
                'distance_km': route['distance_km'],
                'avg_time_mins': route['avg_time_mins'],
                'hour_of_day': hour,
                'day_of_week': 2,
                'is_weekend': 0,
                'route_avg_delay': route.get('avg_delay', 15)
            })
    
    test_df = pd.DataFrame(test_data)
    test_df['predicted_delay'] = model.predict(test_df[features])
    
    return test_df

def recommend_optimal_routes(predictions_df, routes_df, top_n=10):
    """Recommend best routes based on predicted delays"""
    route_summary = predictions_df.groupby('route_id').agg({
        'predicted_delay': 'mean'
    }).reset_index()
    
    route_summary = route_summary.merge(routes_df, on='route_id')
    route_summary['risk_score'] = (
        route_summary['predicted_delay'] / route_summary['predicted_delay'].max() * 100
    ).round(0)
    
    route_summary['recommendation'] = route_summary['risk_score'].apply(
        lambda x: 'High Risk - Avoid' if x > 70 else ('Medium Risk - Monitor' if x > 40 else 'Low Risk - Optimal')
    )
    
    return route_summary.sort_values('risk_score', ascending=False).head(top_n)
