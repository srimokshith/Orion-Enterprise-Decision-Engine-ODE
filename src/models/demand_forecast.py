import pandas as pd
import numpy as np

def exponential_smoothing_simple(data, alpha=0.3):
    """Simple Exponential Smoothing"""
    result = [data.iloc[0]]
    for i in range(1, len(data)):
        result.append(alpha * data.iloc[i] + (1 - alpha) * result[-1])
    return result[-1]

def forecast_product_demand(orders_df, product_id, periods=30):
    """Forecast demand for a specific product using exponential smoothing"""
    product_orders = orders_df[orders_df['product_id'] == product_id].copy()
    product_orders['order_date'] = pd.to_datetime(product_orders['order_date'])
    
    daily_demand = product_orders.groupby('order_date')['quantity'].sum().reset_index()
    daily_demand.columns = ['ds', 'y']
    
    # Fill missing dates
    date_range = pd.date_range(daily_demand['ds'].min(), daily_demand['ds'].max(), freq='D')
    daily_demand = daily_demand.set_index('ds').reindex(date_range, fill_value=0).reset_index()
    daily_demand.columns = ['ds', 'y']
    
    # Simple forecast using exponential smoothing
    last_value = exponential_smoothing_simple(daily_demand['y'])
    
    future_dates = pd.date_range(daily_demand['ds'].max() + pd.Timedelta(days=1), periods=periods)
    forecast = pd.DataFrame({
        'ds': future_dates,
        'yhat': [last_value] * periods,
        'yhat_lower': [last_value * 0.8] * periods,
        'yhat_upper': [last_value * 1.2] * periods
    })
    
    return forecast

def calculate_dynamic_price(forecast_demand, competitor_price, cost, base_price, elasticity=-1.5):
    """Calculate optimal price based on demand forecast"""
    if forecast_demand <= 0:
        return base_price
    
    demand_factor = min(1.3, max(0.7, forecast_demand / 100))
    comp_factor = competitor_price / base_price if competitor_price > 0 else 1.0
    
    optimal_price = base_price * demand_factor * (1 + 0.1 * (comp_factor - 1))
    optimal_price = max(cost * 1.2, min(base_price * 1.5, optimal_price))
    
    return round(optimal_price, 2)

def generate_pricing_recommendations(orders_df, products_df, competitor_df, top_n=10):
    """Generate pricing recommendations for top products"""
    top_products = orders_df.groupby('product_id')['quantity'].sum().nlargest(top_n).index
    
    recommendations = []
    for product_id in top_products:
        forecast = forecast_product_demand(orders_df, product_id, periods=30)
        avg_forecast = forecast['yhat'].mean()
        
        product_info = products_df[products_df['product_id'] == product_id].iloc[0]
        
        recent_comp = competitor_df[competitor_df['product_id'] == product_id]
        comp_price = recent_comp['competitor_price'].mean() if len(recent_comp) > 0 else product_info['base_price']
        
        optimal_price = calculate_dynamic_price(
            avg_forecast, comp_price, product_info['cost'], product_info['base_price']
        )
        
        revenue_current = product_info['base_price'] * avg_forecast
        revenue_optimal = optimal_price * avg_forecast
        revenue_gain = ((revenue_optimal - revenue_current) / revenue_current * 100) if revenue_current > 0 else 0
        
        recommendations.append({
            'product_id': product_id,
            'category': product_info['category'],
            'current_price': product_info['base_price'],
            'recommended_price': optimal_price,
            'competitor_avg_price': round(comp_price, 2),
            'forecast_demand_30d': round(avg_forecast, 0),
            'expected_revenue_gain_pct': round(revenue_gain, 2)
        })
    
    return pd.DataFrame(recommendations)
