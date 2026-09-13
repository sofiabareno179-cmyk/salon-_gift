import os
import re
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    url = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    masked = re.sub(r'(://[^:]+:)[^@]+(@)', r'\1****\2', url)
    print(f"[INFO] Conectando a BD: {masked}", flush=True)

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"[ERROR] No se pudo inicializar la base de datos: {e}")
        print("[ERROR] Verifica DATABASE_URL. La app arrancará igualmente.", flush=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    app.run(debug=False, host='0.0.0.0', port=port)