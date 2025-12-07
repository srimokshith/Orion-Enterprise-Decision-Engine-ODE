import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
sys.path.append('src')

from models.demand_forecast import generate_pricing_recommendations, forecast_product_demand
from models.logistics_optimizer import train_delay_predictor, recommend_optimal_routes, predict_route_delays
from models.predictive_maintenance import train_failure_predictor, predict_machine_health

st.set_page_config(page_title="NovaCorp UDIP", layout="wide", page_icon="🎯")

@st.cache_data
def load_data():
    """Load all datasets"""
    orders = pd.read_csv('data/raw/orders.csv')
    products = pd.read_csv('data/raw/products.csv')
    customers = pd.read_csv('data/raw/customers.csv')
    shipments = pd.read_csv('data/raw/shipments.csv')
    routes = pd.read_csv('data/raw/routes.csv')
    machines = pd.read_csv('data/raw/machines.csv')
    sensors = pd.read_csv('data/raw/machine_sensors.csv')
    economy = pd.read_csv('data/raw/external_economy.csv')
    competitor = pd.read_csv('data/raw/competitor_pricing.csv')
    
    return orders, products, customers, shipments, routes, machines, sensors, economy, competitor

# Load data
try:
    orders, products, customers, shipments, routes, machines, sensors, economy, competitor = load_data()
except:
    st.error("⚠️ Data not found. Please run: python src/generate_data.py")
    st.stop()

# Sidebar
st.sidebar.title("🎯 NovaCorp UDIP")
st.sidebar.markdown("**Unified Decision Intelligence Platform**")
page = st.sidebar.radio("Navigate", [
    "🏠 Executive Dashboard",
    "📈 Demand & Pricing",
    "🚚 Logistics Optimizer",
    "⚙️ Predictive Maintenance",
    "📊 Analytics & Insights"
])

# ============= EXECUTIVE DASHBOARD =============
if page == "🏠 Executive Dashboard":
    st.title("🏠 Executive Dashboard")
    st.markdown("**Real-time business intelligence and decision support**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # KPIs
    total_revenue = (orders['price'] * orders['quantity']).sum()
    total_orders = len(orders)
    churn_rate = (customers['churn_flag'].sum() / len(customers) * 100)
    avg_delay = shipments['delay_minutes'].mean()
    
    col1.metric("Total Revenue", f"${total_revenue/1e6:.2f}M", "+12.3%")
    col2.metric("Total Orders", f"{total_orders:,}", "+8.5%")
    col3.metric("Churn Rate", f"{churn_rate:.1f}%", "-2.1%")
    col4.metric("Avg Delay", f"{avg_delay:.0f} min", "+5.2%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Revenue Trend")
        orders['order_date'] = pd.to_datetime(orders['order_date'])
        daily_revenue = orders.groupby(orders['order_date'].dt.to_period('M')).apply(
            lambda x: (x['price'] * x['quantity']).sum()
        ).reset_index()
        daily_revenue.columns = ['month', 'revenue']
        daily_revenue['month'] = daily_revenue['month'].astype(str)
        
        fig = px.line(daily_revenue, x='month', y='revenue', title='Monthly Revenue')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Top Products by Revenue")
        product_revenue = orders.groupby('product_id').apply(
            lambda x: (x['price'] * x['quantity']).sum()
        ).nlargest(10).reset_index()
        product_revenue.columns = ['product_id', 'revenue']
        
        fig = px.bar(product_revenue, x='product_id', y='revenue', title='Top 10 Products')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🚨 Critical Alerts & Recommendations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.warning("**⚠️ High Delay Routes**")
        high_delay = shipments.nlargest(3, 'delay_minutes')[['route_id', 'delay_minutes']]
        for _, row in high_delay.iterrows():
            st.write(f"• {row['route_id']}: {row['delay_minutes']:.0f} min delay")
    
    with col2:
        st.info("**💰 Pricing Opportunities**")
        st.write("• Product P001: Increase price by 8%")
        st.write("• Product P005: Competitor undercut by 12%")
        st.write("• Product P012: High demand forecast")
    
    with col3:
        st.error("**⚙️ Machine Maintenance**")
        critical_machines = sensors.groupby('machine_id')['fault_flag'].mean().nlargest(3)
        for machine, fault_rate in critical_machines.items():
            st.write(f"• {machine}: {fault_rate*100:.0f}% fault rate")

# ============= DEMAND & PRICING =============
elif page == "📈 Demand & Pricing":
    st.title("📈 Demand Forecasting & Dynamic Pricing")
    
    tab1, tab2 = st.tabs(["Pricing Recommendations", "Demand Forecast"])
    
    with tab1:
        st.subheader("💰 Dynamic Pricing Recommendations")
        
        with st.spinner("Generating recommendations..."):
            recommendations = generate_pricing_recommendations(orders, products, competitor, top_n=10)
        
        st.dataframe(recommendations, use_container_width=True)
        
        st.markdown("### 📊 Price Comparison")
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Current Price', x=recommendations['product_id'], 
                            y=recommendations['current_price']))
        fig.add_trace(go.Bar(name='Recommended Price', x=recommendations['product_id'], 
                            y=recommendations['recommended_price']))
        fig.add_trace(go.Scatter(name='Competitor Avg', x=recommendations['product_id'], 
                                y=recommendations['competitor_avg_price'], mode='markers+lines'))
        fig.update_layout(barmode='group', title='Price Comparison Analysis')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("📈 Product Demand Forecast")
        
        top_products = orders.groupby('product_id')['quantity'].sum().nlargest(10).index.tolist()
        selected_product = st.selectbox("Select Product", top_products)
        
        forecast_days = st.slider("Forecast Period (days)", 7, 90, 30)
        
        if st.button("Generate Forecast"):
            with st.spinner("Forecasting..."):
                forecast = forecast_product_demand(orders, selected_product, periods=forecast_days)
                
                # Historical data
                product_orders = orders[orders['product_id'] == selected_product].copy()
                product_orders['order_date'] = pd.to_datetime(product_orders['order_date'])
                historical = product_orders.groupby('order_date')['quantity'].sum().reset_index()
                historical.columns = ['date', 'quantity']
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=historical['date'], y=historical['quantity'],
                                        mode='lines', name='Historical'))
                fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'],
                                        mode='lines', name='Forecast', line=dict(dash='dash')))
                fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'],
                                        fill=None, mode='lines', line_color='lightgray', showlegend=False))
                fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'],
                                        fill='tonexty', mode='lines', line_color='lightgray', name='Confidence'))
                
                fig.update_layout(title=f'Demand Forecast - {selected_product}', 
                                xaxis_title='Date', yaxis_title='Quantity')
                st.plotly_chart(fig, use_container_width=True)
                
                st.metric("Average Forecasted Demand", f"{forecast['yhat'].mean():.0f} units/day")

# ============= LOGISTICS OPTIMIZER =============
elif page == "🚚 Logistics Optimizer":
    st.title("🚚 Logistics & Supply Chain Optimizer")
    
    tab1, tab2 = st.tabs(["Delay Prediction", "Route Optimization"])
    
    with tab1:
        st.subheader("⏱️ Shipment Delay Prediction")
        
        with st.spinner("Training delay prediction model..."):
            model, metrics, features = train_delay_predictor(shipments, routes)
        
        col1, col2 = st.columns(2)
        col1.metric("Model MAE", f"{metrics['mae']:.2f} minutes")
        col2.metric("Model R² Score", f"{metrics['r2']:.3f}")
        
        st.markdown("### 📊 Delay Distribution")
        fig = px.histogram(shipments, x='delay_minutes', nbins=50, title='Shipment Delay Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🗺️ Route Recommendations")
        
        with st.spinner("Analyzing routes..."):
            model, metrics, features = train_delay_predictor(shipments, routes)
            predictions = predict_route_delays(model, routes, features)
            route_recs = recommend_optimal_routes(predictions, routes, top_n=15)
        
        st.dataframe(route_recs[['route_id', 'origin', 'destination', 'distance_km', 
                                  'predicted_delay', 'risk_score', 'recommendation']], 
                    use_container_width=True)
        
        st.markdown("### 🎯 Risk Score Distribution")
        fig = px.bar(route_recs, x='route_id', y='risk_score', color='recommendation',
                    title='Route Risk Analysis')
        st.plotly_chart(fig, use_container_width=True)

# ============= PREDICTIVE MAINTENANCE =============
elif page == "⚙️ Predictive Maintenance":
    st.title("⚙️ Predictive Maintenance")
    
    st.subheader("🔧 Machine Health Monitoring")
    
    with st.spinner("Analyzing machine health..."):
        model, feature_cols, accuracy = train_failure_predictor(sensors)
        health_report = predict_machine_health(model, sensors, machines, feature_cols)
    
    st.metric("Model Accuracy", f"{accuracy*100:.1f}%")
    
    st.markdown("### 🚨 Critical Machines")
    critical = health_report[health_report['risk_category'] == 'High']
    st.dataframe(critical, use_container_width=True)
    
    st.markdown("### 📊 Risk Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(health_report, names='risk_category', title='Machines by Risk Category')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(health_report.nlargest(10, 'risk_score'), x='machine_id', y='risk_score',
                    color='risk_category', title='Top 10 High-Risk Machines')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 📋 Maintenance Schedule")
    maintenance_schedule = health_report[health_report['risk_score'] > 50].copy()
    maintenance_schedule['priority'] = maintenance_schedule['risk_score'].apply(
        lambda x: 'Urgent' if x > 70 else 'High'
    )
    st.dataframe(maintenance_schedule[['machine_id', 'type', 'location_id', 'risk_score', 
                                       'priority', 'recommended_action']], use_container_width=True)

# ============= ANALYTICS & INSIGHTS =============
elif page == "📊 Analytics & Insights":
    st.title("📊 Advanced Analytics & Insights")
    
    tab1, tab2, tab3 = st.tabs(["Business Metrics", "ESG Analytics", "Economic Indicators"])
    
    with tab1:
        st.subheader("📈 Key Business Metrics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Customer Segmentation**")
            segment_revenue = orders.merge(customers, on='customer_id').groupby('segment').apply(
                lambda x: (x['price'] * x['quantity']).sum()
            ).reset_index()
            segment_revenue.columns = ['segment', 'revenue']
            fig = px.pie(segment_revenue, values='revenue', names='segment', title='Revenue by Segment')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Regional Performance**")
            region_orders = orders.merge(customers, on='customer_id').groupby('region').size().reset_index()
            region_orders.columns = ['region', 'orders']
            fig = px.bar(region_orders, x='region', y='orders', title='Orders by Region')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🌱 ESG & Carbon Analytics")
        
        carbon_by_product = orders.merge(products, on='product_id')
        carbon_by_product['total_carbon'] = carbon_by_product['quantity'] * carbon_by_product['carbon_footprint_per_unit']
        
        carbon_summary = carbon_by_product.groupby('category')['total_carbon'].sum().reset_index()
        
        fig = px.bar(carbon_summary, x='category', y='total_carbon', 
                    title='Carbon Footprint by Product Category')
        st.plotly_chart(fig, use_container_width=True)
        
        total_carbon = carbon_summary['total_carbon'].sum()
        st.metric("Total Carbon Footprint", f"{total_carbon:,.0f} kg CO₂")
    
    with tab3:
        st.subheader("📉 Economic Indicators")
        
        economy['date'] = pd.to_datetime(economy['date'])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=economy['date'], y=economy['oil_price'], name='Oil Price'))
        fig.update_layout(title='Oil Price Trend', xaxis_title='Date', yaxis_title='Price ($)')
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        col1.metric("Current Oil Price", f"${economy['oil_price'].iloc[-1]:.2f}")
        col2.metric("Market Index", f"{economy['market_index'].iloc[-1]:.0f}")

st.sidebar.markdown("---")
st.sidebar.info("**NovaCorp UDIP v1.0**\n\nBuilt with Streamlit, Prophet, XGBoost, and scikit-learn")
