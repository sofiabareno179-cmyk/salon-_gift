import psycopg

try:
    print("Connecting to port 500...")
    conn = psycopg.connect("postgresql://admin:9027865@127.0.0.1:500/salonglitt_db", connect_timeout=5)
    print("Connection to port 500 successful!")
    conn.close()
except Exception as e:
    print(f"Failed connection to port 500: {e}")

try:
    print("Connecting to port 5432...")
    conn = psycopg.connect("postgresql://admin:9027865@127.0.0.1:5432/salonglitt_db", connect_timeout=5)
    print("Connection to port 5432 successful!")
    conn.close()
except Exception as e:
    print(f"Failed connection to port 5432: {e}")
