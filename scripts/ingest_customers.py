import json, psycopg2, random
from datetime import datetime

with open("data.json") as f:
    data = json.load(f)

conn = psycopg2.connect(host="postgres", dbname="kestra", user="kestra", password="k3str4")
cur = conn.cursor()
plans = ["Basic", "Standard", "Premium", "Business"]
count = 0

for user in data.get("results", []):
    cid = user["login"]["username"]
    cur.execute("SELECT 1 FROM customers WHERE customer_id=%s", (cid,))
    if cur.fetchone():
        continue
    cur.execute("""
        INSERT INTO customers (customer_id, first_name, last_name, email, phone, city, country, registration_date, plan_type)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        cid,
        user["name"]["first"],
        user["name"]["last"],
        user["email"],
        user["phone"],
        user["location"]["city"],
        user["location"]["country"],
        datetime.fromisoformat(user["registered"]["date"].replace("Z","")).strftime("%Y-%m-%d"),
        random.choice(plans)
    ))
    count += 1

conn.commit()
cur.close()
conn.close()
print(json.dumps({"inserted": count, "total_in_api": len(data.get("results",[]))}))
