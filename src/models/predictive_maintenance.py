import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def create_rolling_features(sensor_df, window=24):
    """Create rolling window features from sensor data"""
    sensor_df = sensor_df.sort_values(['machine_id', 'timestamp'])
    
    for col in ['temperature', 'vibration', 'load_percent']:
        sensor_df[f'{col}_rolling_mean'] = sensor_df.groupby('machine_id')[col].transform(
            lambda x: x.rolling(window, min_periods=1).mean()
        )
        sensor_df[f'{col}_rolling_std'] = sensor_df.groupby('machine_id')[col].transform(
            lambda x: x.rolling(window, min_periods=1).std()
        )
    
    return sensor_df

def train_failure_predictor(sensor_df):
    """Train model to predict machine failures"""
    df = create_rolling_features(sensor_df.copy())
    df = df.dropna()
    
    feature_cols = [col for col in df.columns if 'rolling' in col or col in ['temperature', 'vibration', 'load_percent']]
    X = df[feature_cols]
    y = df['fault_flag']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    
    return model, feature_cols, accuracy

def predict_machine_health(model, sensor_df, machines_df, feature_cols):
    """Predict health status for all machines"""
    df = create_rolling_features(sensor_df.copy())
    
    latest_readings = df.groupby('machine_id').tail(1)
    latest_readings['failure_probability'] = model.predict_proba(latest_readings[feature_cols])[:, 1]
    
    latest_readings['risk_score'] = (latest_readings['failure_probability'] * 100).round(0)
    latest_readings['risk_category'] = pd.cut(
        latest_readings['risk_score'],
        bins=[0, 30, 60, 100],
        labels=['Low', 'Medium', 'High']
    )
    
    result = latest_readings.merge(machines_df[['machine_id', 'type', 'location_id']], on='machine_id')
    
    result['recommended_action'] = result['risk_category'].map({
        'Low': 'Continue monitoring',
        'Medium': 'Schedule inspection within 7 days',
        'High': 'Immediate maintenance required'
    })
    
    return result[['machine_id', 'type', 'location_id', 'risk_score', 'risk_category', 
                   'temperature', 'vibration', 'recommended_action']].sort_values('risk_score', ascending=False)
