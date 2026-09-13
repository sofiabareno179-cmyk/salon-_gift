import os
from app import create_app, db

app = create_app()

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"[ERROR] No se pudo inicializar la base de datos: {e}")
        print("[ERROR] Verifica DATABASE_URL. La app arrancará igualmente.", flush=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    app.run(debug=False, host='0.0.0.0', port=port)