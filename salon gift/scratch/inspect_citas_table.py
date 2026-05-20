import psycopg

try:
    conn = psycopg.connect("postgresql://admin:9027865@127.0.0.1:500/salonglitt_db")
    cur = conn.cursor()
    
    # Get column definitions for table 'citas'
    cur.execute("""
        SELECT column_name, data_type, character_maximum_length
        FROM information_schema.columns
        WHERE table_name = 'citas';
    """)
    print("Columns in 'citas':")
    for row in cur.fetchall():
        print(row)
        
    # Get some records
    cur.execute("SELECT * FROM citas LIMIT 10;")
    print("\nFirst 10 records in 'citas':")
    for row in cur.fetchall():
        print(row)
        
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
