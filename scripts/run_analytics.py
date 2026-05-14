import json, psycopg2
from datetime import date

conn = psycopg2.connect(host="postgres", dbname="kestra", user="kestra", password="k3str4")
cur = conn.cursor()

today = date.today()

cur.execute("""
    SELECT COUNT(*), COALESCE(SUM(duration_seconds)/60.0, 0),
           COALESCE(SUM(cost), 0), COUNT(DISTINCT customer_id),
           COALESCE(AVG(duration_seconds), 0)
    FROM call_records
    WHERE DATE(call_date) = %s
""", (today,))
row = cur.fetchone()

cur.execute("""
    INSERT INTO daily_summary (summary_date, total_calls, total_minutes, total_revenue, unique_customers, avg_call_duration)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (summary_date) DO UPDATE SET
        total_calls = EXCLUDED.total_calls,
        total_minutes = EXCLUDED.total_minutes,
        total_revenue = EXCLUDED.total_revenue,
        unique_customers = EXCLUDED.unique_customers,
        avg_call_duration = EXCLUDED.avg_call_duration
""", (today, row[0], round(row[1],2), round(row[2],2), row[3], round(row[4],2)))
conn.commit()

cur.execute("""
    SELECT c.first_name || ' ' || c.last_name as name,
           COUNT(*) as calls, SUM(cr.cost) as revenue
    FROM call_records cr
    JOIN customers c ON cr.customer_id = c.customer_id
    WHERE DATE(cr.call_date) = %s
    GROUP BY c.first_name, c.last_name
    ORDER BY revenue DESC
    LIMIT 5
""", (today,))
top = [{"name": r[0], "calls": r[1], "revenue": float(round(r[2],2))} for r in cur.fetchall()]

cur.close()
conn.close()

result = {
    "date": str(today),
    "total_calls": row[0],
    "total_minutes": float(round(row[1], 2)),
    "total_revenue": float(round(row[2], 2)),
    "unique_customers": row[3],
    "avg_duration_seconds": float(round(row[4], 2)),
    "top_customers": top
}
print(json.dumps(result, indent=2))
