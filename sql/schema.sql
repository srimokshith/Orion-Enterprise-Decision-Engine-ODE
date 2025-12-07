-- NovaCorp Unified Decision Intelligence Platform - Database Schema

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    segment VARCHAR(50),
    region VARCHAR(50),
    signup_date DATE,
    churn_flag INTEGER,
    lifetime_value DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(20) PRIMARY KEY,
    category VARCHAR(50),
    base_price DECIMAL(10,2),
    cost DECIMAL(10,2),
    carbon_footprint_per_unit DECIMAL(8,2)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    product_id VARCHAR(20),
    quantity INTEGER,
    price DECIMAL(10,2),
    channel VARCHAR(20),
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS inventory (
    location_id VARCHAR(20),
    product_id VARCHAR(20),
    stock_level INTEGER,
    reorder_point INTEGER,
    PRIMARY KEY (location_id, product_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS machines (
    machine_id VARCHAR(20) PRIMARY KEY,
    location_id VARCHAR(20),
    type VARCHAR(50),
    install_date DATE,
    last_maintenance_date DATE,
    status VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS machine_sensors (
    machine_id VARCHAR(20),
    timestamp TIMESTAMP,
    temperature DECIMAL(5,2),
    vibration DECIMAL(5,2),
    load_percent DECIMAL(5,2),
    fault_flag INTEGER,
    PRIMARY KEY (machine_id, timestamp),
    FOREIGN KEY (machine_id) REFERENCES machines(machine_id)
);

CREATE TABLE IF NOT EXISTS employees (
    emp_id INTEGER PRIMARY KEY,
    dept VARCHAR(50),
    role VARCHAR(50),
    join_date DATE,
    attrition_flag INTEGER,
    performance_score DECIMAL(3,2)
);

CREATE TABLE IF NOT EXISTS employee_activity (
    emp_id INTEGER,
    date DATE,
    meetings_count INTEGER,
    avg_work_hours DECIMAL(4,2),
    tasks_completed INTEGER,
    stress_index DECIMAL(3,2),
    PRIMARY KEY (emp_id, date),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);

CREATE TABLE IF NOT EXISTS routes (
    route_id VARCHAR(20) PRIMARY KEY,
    origin VARCHAR(50),
    destination VARCHAR(50),
    distance_km DECIMAL(8,2),
    avg_time_mins INTEGER
);

CREATE TABLE IF NOT EXISTS shipments (
    shipment_id INTEGER PRIMARY KEY,
    route_id VARCHAR(20),
    vehicle_id VARCHAR(20),
    planned_departure TIMESTAMP,
    actual_departure TIMESTAMP,
    planned_arrival TIMESTAMP,
    actual_arrival TIMESTAMP,
    fuel_used_litres DECIMAL(8,2),
    delay_minutes INTEGER,
    FOREIGN KEY (route_id) REFERENCES routes(route_id)
);

CREATE TABLE IF NOT EXISTS energy_usage (
    location_id VARCHAR(20),
    timestamp TIMESTAMP,
    kwh_used DECIMAL(10,2),
    PRIMARY KEY (location_id, timestamp)
);

CREATE TABLE IF NOT EXISTS external_economy (
    date DATE PRIMARY KEY,
    oil_price DECIMAL(8,2),
    fx_rate DECIMAL(8,4),
    market_index DECIMAL(10,2),
    sentiment_score DECIMAL(3,2)
);

CREATE TABLE IF NOT EXISTS competitor_pricing (
    date DATE,
    product_id VARCHAR(20),
    competitor_name VARCHAR(50),
    competitor_price DECIMAL(10,2),
    PRIMARY KEY (date, product_id, competitor_name),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
