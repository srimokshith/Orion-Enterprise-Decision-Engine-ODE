import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import os

fake = Faker()
np.random.seed(42)

output_dir = 'data/raw'
os.makedirs(output_dir, exist_ok=True)

# Date range
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
dates = pd.date_range(start_date, end_date, freq='D')

# Products
products = pd.DataFrame({
    'product_id': [f'P{str(i).zfill(3)}' for i in range(1, 21)],
    'category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Sports'], 20),
    'base_price': np.random.uniform(20, 500, 20).round(2),
    'cost': np.random.uniform(10, 300, 20).round(2),
    'carbon_footprint_per_unit': np.random.uniform(0.5, 5, 20).round(2)
})
products.to_csv(f'{output_dir}/products.csv', index=False)

# Customers
customers = pd.DataFrame({
    'customer_id': range(1, 1001),
    'segment': np.random.choice(['Premium', 'Standard', 'Budget'], 1000),
    'region': np.random.choice(['North', 'South', 'East', 'West'], 1000),
    'signup_date': [fake.date_between(start_date='-3y', end_date='today') for _ in range(1000)],
    'churn_flag': np.random.choice([0, 1], 1000, p=[0.85, 0.15]),
    'lifetime_value': np.random.uniform(100, 10000, 1000).round(2)
})
customers.to_csv(f'{output_dir}/customers.csv', index=False)

# Orders
orders_data = []
order_id = 1
for date in dates:
    n_orders = np.random.poisson(50)
    for _ in range(n_orders):
        product = products.sample(1).iloc[0]
        orders_data.append({
            'order_id': order_id,
            'customer_id': np.random.randint(1, 1001),
            'order_date': date,
            'product_id': product['product_id'],
            'quantity': np.random.randint(1, 10),
            'price': product['base_price'] * np.random.uniform(0.9, 1.1),
            'channel': np.random.choice(['Online', 'Store', 'Mobile']),
            'status': np.random.choice(['Completed', 'Pending', 'Cancelled'], p=[0.85, 0.1, 0.05])
        })
        order_id += 1

orders = pd.DataFrame(orders_data)
orders.to_csv(f'{output_dir}/orders.csv', index=False)

# Routes
routes = pd.DataFrame({
    'route_id': [f'R{str(i).zfill(3)}' for i in range(1, 51)],
    'origin': [fake.city() for _ in range(50)],
    'destination': [fake.city() for _ in range(50)],
    'distance_km': np.random.uniform(50, 1000, 50).round(2),
    'avg_time_mins': np.random.randint(60, 600, 50)
})
routes.to_csv(f'{output_dir}/routes.csv', index=False)

# Shipments
shipments_data = []
shipment_id = 1
for date in dates:
    n_shipments = np.random.poisson(20)
    for _ in range(n_shipments):
        route = routes.sample(1).iloc[0]
        planned_dep = datetime.combine(date, datetime.min.time()) + timedelta(hours=np.random.randint(0, 24))
        delay = max(0, int(np.random.normal(15, 30)))
        
        shipments_data.append({
            'shipment_id': shipment_id,
            'route_id': route['route_id'],
            'vehicle_id': f'V{np.random.randint(1, 51):03d}',
            'planned_departure': planned_dep,
            'actual_departure': planned_dep + timedelta(minutes=int(np.random.randint(-10, 30))),
            'planned_arrival': planned_dep + timedelta(minutes=int(route['avg_time_mins'])),
            'actual_arrival': planned_dep + timedelta(minutes=int(route['avg_time_mins']) + delay),
            'fuel_used_litres': float((route['distance_km'] / 10) * np.random.uniform(0.9, 1.1)),
            'delay_minutes': delay
        })
        shipment_id += 1

shipments = pd.DataFrame(shipments_data)
shipments.to_csv(f'{output_dir}/shipments.csv', index=False)

# Machines
machines = pd.DataFrame({
    'machine_id': [f'M{str(i).zfill(3)}' for i in range(1, 31)],
    'location_id': [f'L{np.random.randint(1, 6):02d}' for _ in range(30)],
    'type': np.random.choice(['CNC', 'Press', 'Conveyor', 'Robot'], 30),
    'install_date': [fake.date_between(start_date='-5y', end_date='-1y') for _ in range(30)],
    'last_maintenance_date': [fake.date_between(start_date='-6m', end_date='today') for _ in range(30)],
    'status': np.random.choice(['Active', 'Maintenance', 'Idle'], 30, p=[0.8, 0.1, 0.1])
})
machines.to_csv(f'{output_dir}/machines.csv', index=False)

# Machine sensors
sensor_data = []
for machine_id in machines['machine_id']:
    for date in pd.date_range(start_date, end_date, freq='H'):
        base_temp = np.random.uniform(60, 80)
        base_vib = np.random.uniform(0.5, 2)
        fault = 1 if (base_temp > 75 and base_vib > 1.8) else 0
        
        sensor_data.append({
            'machine_id': machine_id,
            'timestamp': date,
            'temperature': base_temp + np.random.normal(0, 2),
            'vibration': base_vib + np.random.normal(0, 0.2),
            'load_percent': np.random.uniform(40, 95),
            'fault_flag': fault
        })

sensors = pd.DataFrame(sensor_data[:50000])  # Limit size
sensors.to_csv(f'{output_dir}/machine_sensors.csv', index=False)

# Employees
employees = pd.DataFrame({
    'emp_id': range(1, 201),
    'dept': np.random.choice(['Sales', 'Operations', 'IT', 'HR', 'Finance'], 200),
    'role': np.random.choice(['Manager', 'Senior', 'Junior', 'Lead'], 200),
    'join_date': [fake.date_between(start_date='-5y', end_date='today') for _ in range(200)],
    'attrition_flag': np.random.choice([0, 1], 200, p=[0.88, 0.12]),
    'performance_score': np.random.uniform(0.5, 1.0, 200).round(2)
})
employees.to_csv(f'{output_dir}/employees.csv', index=False)

# External economy
economy = pd.DataFrame({
    'date': dates,
    'oil_price': 70 + np.cumsum(np.random.normal(0, 2, len(dates))),
    'fx_rate': 1.1 + np.cumsum(np.random.normal(0, 0.01, len(dates))),
    'market_index': 3000 + np.cumsum(np.random.normal(0, 50, len(dates))),
    'sentiment_score': np.random.uniform(-1, 1, len(dates))
})
economy.to_csv(f'{output_dir}/external_economy.csv', index=False)

# Competitor pricing
comp_pricing = []
for date in dates[::7]:  # Weekly
    for product_id in products['product_id'][:10]:
        base = products[products['product_id'] == product_id]['base_price'].values[0]
        comp_pricing.append({
            'date': date,
            'product_id': product_id,
            'competitor_name': np.random.choice(['CompA', 'CompB', 'CompC']),
            'competitor_price': base * np.random.uniform(0.85, 1.15)
        })

comp_df = pd.DataFrame(comp_pricing)
comp_df.to_csv(f'{output_dir}/competitor_pricing.csv', index=False)

print(f"✅ Generated {len(orders)} orders")
print(f"✅ Generated {len(shipments)} shipments")
print(f"✅ Generated {len(sensors)} sensor readings")
print(f"✅ All data saved to {output_dir}/")
