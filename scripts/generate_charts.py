import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import psycopg2
import pandas as pd
import numpy as np

conn = psycopg2.connect(host="postgres", dbname="kestra", user="kestra", password="k3str4")

plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['figure.dpi'] = 100

# Chart 1: Daily Revenue Trend (last 30 days)
df_rev = pd.read_sql("""
    SELECT summary_date, total_revenue, total_calls
    FROM daily_summary
    ORDER BY summary_date DESC LIMIT 30
""", conn)
df_rev = df_rev.sort_values('summary_date')

fig, ax = plt.subplots()
ax.plot(df_rev['summary_date'].astype(str), df_rev['total_revenue'], marker='o', linewidth=2, color='#2E86AB')
ax.set_title('Daily Revenue Trend (Last 30 Days)', fontsize=16, fontweight='bold')
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Revenue ($)', fontsize=12)
ax.tick_params(axis='x', rotation=45)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/outputs/revenue_trend.png', bbox_inches='tight')
plt.close()

# Chart 2: Call Type Distribution (Pie)
df_types = pd.read_sql("""
    SELECT call_type, COUNT(*) as count, SUM(cost) as revenue
    FROM call_records
    GROUP BY call_type
""", conn)

fig, (ax1, ax2) = plt.subplots(1, 2)
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
ax1.pie(df_types['count'], labels=df_types['call_type'], autopct='%1.1f%%', colors=colors, startangle=90)
ax1.set_title('Call Volume by Type', fontsize=14, fontweight='bold')
ax2.pie(df_types['revenue'], labels=df_types['call_type'], autopct='%1.1f%%', colors=colors, startangle=90)
ax2.set_title('Revenue by Call Type', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('/outputs/call_type_analysis.png', bbox_inches='tight')
plt.close()

# Chart 3: Top 10 Customers by Revenue
df_top = pd.read_sql("""
    SELECT c.first_name || ' ' || c.last_name as name,
           ROUND(SUM(cr.cost)::numeric, 2) as revenue,
           COUNT(*) as calls
    FROM call_records cr
    JOIN customers c ON cr.customer_id = c.customer_id
    GROUP BY c.first_name, c.last_name
    ORDER BY revenue DESC
    LIMIT 10
""", conn)

fig, ax = plt.subplots()
bars = ax.barh(df_top['name'], df_top['revenue'], color='#2ECC71')
ax.set_title('Top 10 Customers by Revenue', fontsize=16, fontweight='bold')
ax.set_xlabel('Revenue ($)', fontsize=12)
ax.invert_yaxis()
for bar, val in zip(bars, df_top['revenue']):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f'${val}',
            va='center', fontsize=10)
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('/outputs/top_customers.png', bbox_inches='tight')
plt.close()

# Chart 4: Hourly Call Volume (heatmap-style bar chart)
df_hourly = pd.read_sql("""
    SELECT EXTRACT(HOUR FROM call_date) as hour, COUNT(*) as calls
    FROM call_records
    GROUP BY hour
    ORDER BY hour
""", conn)

hours = [f"{int(h):02d}:00" for h in df_hourly['hour']]
fig, ax = plt.subplots()
bars = ax.bar(hours, df_hourly['calls'], color='#9B59B6')
ax.set_title('Call Volume by Hour of Day', fontsize=16, fontweight='bold')
ax.set_xlabel('Hour', fontsize=12)
ax.set_ylabel('Number of Calls', fontsize=12)
ax.tick_params(axis='x', rotation=45)
for bar, val in zip(bars, df_hourly['calls']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, str(val),
            ha='center', fontsize=9)
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('/outputs/hourly_volume.png', bbox_inches='tight')
plt.close()

conn.close()
print("All 4 charts generated successfully!")
