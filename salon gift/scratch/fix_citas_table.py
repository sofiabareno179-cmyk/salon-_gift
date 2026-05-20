import psycopg

try:
    print("Connecting to database on port 500...")
    conn = psycopg.connect("postgresql://admin:9027865@127.0.0.1:500/salonglitt_db")
    cur = conn.cursor()
    
    # 1. Alter fechahora column type to timestamp
    print("Altering fechahora column type to TIMESTAMP WITHOUT TIME ZONE...")
    cur.execute("""
        ALTER TABLE citas 
        ALTER COLUMN fechahora TYPE timestamp without time zone 
        USING (fechahora::timestamp without time zone);
    """)
    
    # 2. Add servicio column
    print("Adding 'servicio' column to 'citas' table...")
    cur.execute("""
        ALTER TABLE citas 
        ADD COLUMN IF NOT EXISTS servicio character varying(150);
    """)
    
    conn.commit()
    print("Database schema migration completed successfully!")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error during migration: {e}")
