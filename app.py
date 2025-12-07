import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="NovaCorp UDIP", layout="wide", page_icon="🎯")

@st.cache_data
def load_data():
    """Load all datasets"""
    try:
        orders = pd.read_csv('data/raw/orders.csv')
        products = pd.read_csv('data/raw/products.csv')
        customers = pd.read_csv('data/raw/customers.csv')
        shipments = pd.read_csv('data/raw/shipments.csv')
        routes = pd.read_csv('data/raw/routes.csv')
        return orders, products, customers, shipments, routes
    except:
        st.error("⚠️ Data files not found. Please ensure data is generated.")
        return None, None, None, None, None

# Load data
orders, products, customers, shipments, routes = load_data()

if orders is None:
    st.stop()

# Sidebar
st.sidebar.title("🎯 NovaCorp UDIP")
st.sidebar.markdown("**Unified Decision Intelligence Platform**")
page = st.sidebar.radio("Navigate", [
    "🏠 Executive Dashboard",
    "📈 Sales Analytics",
    "🚚 Logistics",
    "📊 Insights"
])

# ============= EXECUTIVE DASHBOARD =============
if page == "🏠 Executive Dashboard":
    st.title("🏠 Executive Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_revenue = (orders['price'] * orders['quantity']).sum()
    total_orders = len(orders)
    churn_rate = (customers['churn_flag'].sum() / len(customers) * 100)
    avg_delay = shipments['delay_minutes'].mean()
    
    col1.metric("Total Revenue", f"${total_revenue/1e6:.2f}M")
    col2.metric("Total Orders", f"{total_orders:,}")
    col3.metric("Churn Rate", f"{churn_rate:.1f}%")
    col4.metric("Avg Delay", f"{avg_delay:.0f} min")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Revenue Trend")
        orders['order_date'] = pd.to_datetime(orders['order_date'])
        monthly = orders.groupby(orders['order_date'].dt.to_period('M')).apply(
            lambda x: (x['price'] * x['quantity']).sum()
        ).reset_index()
        monthly.columns = ['month', 'revenue']
        monthly['month'] = monthly['month'].astype(str)
        
        fig = px.line(monthly, x='month', y='revenue')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Top Products")
        top_products = orders.groupby('product_id').apply(
            lambda x: (x['price'] * x['quantity']).sum()
        ).nlargest(10).reset_index()
        top_products.columns = ['product_id', 'revenue']
        
        fig = px.bar(top_products, x='product_id', y='revenue')
        st.plotly_chart(fig, use_container_width=True)

# ============= SALES ANALYTICS =============
elif page == "📈 Sales Analytics":
    st.title("📈 Sales Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sales by Category")
        category_sales = orders.merge(products, on='product_id').groupby('category').apply(
            lambda x: (x['price'] * x['quantity']).sum()
        ).reset_index()
        category_sales.columns = ['category', 'revenue']
        
        fig = px.pie(category_sales, values='revenue', names='category')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Sales by Region")
        region_sales = orders.merge(customers, on='customer_id').groupby('region').apply(
            lambda x: (x['price'] * x['quantity']).sum()
        ).reset_index()
        region_sales.columns = ['region', 'revenue']
        
        fig = px.bar(region_sales, x='region', y='revenue')
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📋 Recent Orders")
    st.dataframe(orders.tail(20), use_container_width=True)

# ============= LOGISTICS =============
elif page == "🚚 Logistics":
    st.title("🚚 Logistics Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    on_time = (shipments['delay_minutes'] <= 15).sum()
    on_time_pct = (on_time / len(shipments) * 100)
    
    col1.metric("Total Shipments", f"{len(shipments):,}")
    col2.metric("On-Time %", f"{on_time_pct:.1f}%")
    col3.metric("Avg Delay", f"{shipments['delay_minutes'].mean():.0f} min")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Delay Distribution")
        fig = px.histogram(shipments, x='delay_minutes', nbins=50)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top Delayed Routes")
        route_delays = shipments.groupby('route_id')['delay_minutes'].mean().nlargest(10).reset_index()
        
        fig = px.bar(route_delays, x='route_id', y='delay_minutes')
        st.plotly_chart(fig, use_container_width=True)

# ============= INSIGHTS =============
elif page == "📊 Insights":
    st.title("📊 Business Insights")
    
    st.subheader("🎯 Key Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    avg_order_value = (orders['price'] * orders['quantity']).sum() / len(orders)
    col1.metric("Avg Order Value", f"${avg_order_value:.2f}")
    
    total_customers = len(customers)
    col2.metric("Total Customers", f"{total_customers:,}")
    
    total_products = len(products)
    col3.metric("Total Products", f"{total_products}")
    
    st.markdown("---")
    
    st.subheader("📈 Customer Segments")
    segment_dist = customers['segment'].value_counts().reset_index()
    segment_dist.columns = ['segment', 'count']
    
    fig = px.pie(segment_dist, values='count', names='segment')
    st.plotly_chart(fig, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.info("**NovaCorp UDIP v1.0**\n\nSimplified for fast deployment")
