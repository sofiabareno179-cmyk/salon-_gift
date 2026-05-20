# pyrefly: ignore [missing-import]
import psycopg
try:
    conn = psycopg.connect("postgresql://postgres:9027865@127.0.0.1:5432/salonglitt_db", connect_timeout=5)
    print("Success with postgres user")
    conn.close()
except Exception as e:
    print(f"Error with postgres user: {e}")

try:
    conn = psycopg.connect("postgresql://admin:9027865@127.0.0.1:5432/salonglitt_db", connect_timeout=5)
    print("Success with admin user")
    conn.close()
except Exception as e:
    print(f"Error with admin user: {e}")
