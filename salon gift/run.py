import sys

from sqlalchemy.exc import OperationalError

from app import create_app, db


def ensure_sqlite_schema(app):
    with app.app_context():
        if db.engine.dialect.name != 'sqlite':
            return

        with db.engine.begin() as conn:
            table_exists = conn.exec_driver_sql(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='servicios'"
            ).fetchone()

            if not table_exists:
                return

            columns = conn.exec_driver_sql("PRAGMA table_info(servicios)").fetchall()
            column_map = {column[1]: column for column in columns}
            has_imagen = 'imagen' in column_map
            has_tip = 'tip' in column_map
            idcitas_nullable = column_map.get('idcitas', (None, None, None, 1, None, None))[3] == 0

            if has_imagen and has_tip and idcitas_nullable:
                return

            if has_imagen and idcitas_nullable and not has_tip:
                conn.exec_driver_sql("ALTER TABLE servicios ADD COLUMN tip VARCHAR(255)")
                return

            conn.exec_driver_sql("ALTER TABLE servicios RENAME TO servicios_old")

            conn.exec_driver_sql(
                """
                CREATE TABLE servicios (
                    idservicio INTEGER PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    precio NUMERIC(10, 2) NOT NULL,
                    duracion VARCHAR(250) NOT NULL,
                    categoria VARCHAR(50) NOT NULL,
                    idcitas INTEGER,
                    imagen VARCHAR(255),
                    tip VARCHAR(255)
                )
                """
            )

            insert_columns = "idservicio, nombre, precio, duracion, categoria, idcitas"
            select_columns = "idservicio, nombre, precio, duracion, categoria, idcitas"

            if has_imagen:
                insert_columns = f"{insert_columns}, imagen"
                select_columns = f"{select_columns}, imagen"
            else:
                insert_columns = f"{insert_columns}, imagen"
                select_columns = f"{select_columns}, NULL AS imagen"

            if has_tip:
                insert_columns = f"{insert_columns}, tip"
                select_columns = f"{select_columns}, tip"
            else:
                insert_columns = f"{insert_columns}, tip"
                select_columns = f"{select_columns}, NULL AS tip"

            conn.exec_driver_sql(
                f"INSERT INTO servicios ({insert_columns}) SELECT {select_columns} FROM servicios_old"
            )
            conn.exec_driver_sql("DROP TABLE servicios_old")


def bootstrap_database(app):
    try:
        with app.app_context():
            ensure_sqlite_schema(app)
            db.create_all()
    except OperationalError as exc:
        print("\n[ERROR] No se pudo conectar a la base de datos.")
        print("Revisa la configuración de SQLALCHEMY_DATABASE_URI en config.py o app/.env.")
        print(f"Detalle: {exc}")
        raise SystemExit(1)


def main():
    app = create_app()
    bootstrap_database(app)
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()