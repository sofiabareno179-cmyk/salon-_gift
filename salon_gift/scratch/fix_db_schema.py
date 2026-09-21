from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # Alter the table to make idcitas nullable
        db.session.execute(text('ALTER TABLE servicios ALTER COLUMN idcitas DROP NOT NULL;'))
        # Also drop the unique constraint if it exists (psycopg often names it after the column or a random string)
        # We can try to drop it by searching for it, but simpler is just allowing nulls for now.
        db.session.commit()
        print("Successfully altered table 'servicios' to make 'idcitas' nullable.")
    except Exception as e:
        db.session.rollback()
        print(f"Error altering table: {e}")
