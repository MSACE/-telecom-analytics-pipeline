import json, psycopg2, random, sys
from datetime import datetime, timedelta

conn = psycopg2.connect(host="postgres", dbname="kestra", user="kestra", password="k3str4")
cur = conn.cursor()

cur.execute("SELECT customer_id FROM customers")
customers = [row[0] for row in cur.fetchall()]

if not customers:
    print(json.dumps({"error": "No customers found"}))
    sys.exit(0)

call_types = ["LOCAL", "STD", "ISD"]
destinations = {
    "LOCAL": ["City1", "City2", "City3"],
    "STD": ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"],
    "ISD": ["USA", "UK", "UAE", "Singapore", "Australia", "Canada"]
}

records = []
for _ in range(random.randint(150, 300)):
    customer_id = random.choice(customers)
    call_type = random.choice(call_types)
    duration = random.randint(10, 3600)
    cost_per_min = {"LOCAL": 0.5, "STD": 1.5, "ISD": 5.0}[call_type]
    cost = round((duration / 60) * cost_per_min, 4)
    dest = random.choice(destinations[call_type])
    call_date = datetime.now() - timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
    records.append((customer_id, call_date, duration, call_type, dest, cost))

cur.executemany(
    "INSERT INTO call_records (customer_id, call_date, duration_seconds, call_type, destination, cost) VALUES (%s,%s,%s,%s,%s,%s)",
    records
)
conn.commit()
cur.close()
conn.close()

print(json.dumps({"generated": len(records), "customers_used": len(customers)}))
