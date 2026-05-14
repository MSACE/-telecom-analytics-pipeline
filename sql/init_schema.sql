CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(200),
    phone VARCHAR(50),
    city VARCHAR(100),
    country VARCHAR(100),
    registration_date DATE,
    plan_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS call_records (
    call_id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) REFERENCES customers(customer_id),
    call_date TIMESTAMP,
    duration_seconds INTEGER,
    call_type VARCHAR(20),
    destination VARCHAR(100),
    cost DECIMAL(10,4),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS daily_summary (
    summary_date DATE PRIMARY KEY,
    total_calls INTEGER,
    total_minutes DECIMAL(10,2),
    total_revenue DECIMAL(12,2),
    unique_customers INTEGER,
    avg_call_duration DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);
