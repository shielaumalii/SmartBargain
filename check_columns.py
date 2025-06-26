import sqlite3

conn = sqlite3.connect('core/db/smartbargain.db')
cursor = conn.cursor()

print("Columns in negotiation_dashboard:")
cursor.execute("PRAGMA table_info(negotiation_dashboard);")
for column in cursor.fetchall():
    print(column)
