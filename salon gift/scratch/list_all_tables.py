import psycopg

try:
    conn = psycopg.connect("postgresql://admin:9027865@127.0.0.1:500/salonglitt_db")
    cur = conn.cursor()
    
    # Get all tables
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
    """)
    tables = cur.fetchall()
    print("Tables in database:")
    for t in tables:
        print(f"\n--- Table: {t[0]} ---")
        cur.execute(f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = '{t[0]}';
        """)
        for col in cur.fetchall():
            print(col)
            
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
