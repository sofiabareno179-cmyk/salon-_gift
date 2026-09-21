import pytest


@pytest.fixture()
def app(tmp_path, monkeypatch):
    database_path = tmp_path / "test.sqlite"
    monkeypatch.setenv("SQLALCHEMY_DATABASE_URI", f"sqlite:///{database_path}")

    from app import create_app, db

    application = create_app()
    application.config.update(TESTING=True, WTF_CSRF_ENABLED=False)

    with application.app_context():
        db.create_all()

    yield application

    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def user(app):
    from app import db
    from app.models.usuario import User

    with app.app_context():
        new_user = User(
            nombreuser="test_user",
            email="test@example.com",
            telefono="3000000000",
            rol="cliente",
        )
        new_user.set_password("test_password")
        db.session.add(new_user)
        db.session.commit()
        new_user.idusuario = new_user.idusuario
        new_user.email = new_user.email
        new_user.nombreuser = new_user.nombreuser
        db.session.expunge(new_user)
        return new_user


@pytest.fixture()
def admin(app):
    from app import db
    from app.models.usuario import User

    with app.app_context():
        new_admin = User(
            nombreuser="test_admin",
            email="admin@example.com",
            telefono="3000000001",
            rol="admin",
        )
        new_admin.set_password("admin_password")
        db.session.add(new_admin)
        db.session.commit()
        new_admin.idusuario = new_admin.idusuario
        new_admin.email = new_admin.email
        new_admin.nombreuser = new_admin.nombreuser
        db.session.expunge(new_admin)
        return new_admin