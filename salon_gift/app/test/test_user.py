from app.models.usuario import User


def login(client, email, password):
    return client.post("/login", data={"email": email, "password": password})


def test_user_index_y_add(client, user):
    login(client, user.email, "test_password")
    response = client.get("/User/dashboard")
    assert response.status_code == 200

    response = client.post(
        "/User/add",
        data={
            "nombreuser": "new_user",
            "email": "new@example.com",
            "password": "new_password",
            "nombre": "Nuevo",
            "apellido": "Usuario",
        },
    )
    assert response.status_code == 302
    with client.application.app_context():
        created = User.query.filter_by(email="new@example.com").one()
        assert created.check_password("new_password")


def test_user_edit_y_delete(client, user, admin):
    login(client, user.email, "test_password")
    response = client.post(
        f"/User/edit/{user.idusuario}",
        data={
            "nombreuser": "updated_user",
            "email": "updated@example.com",
            "telefono": "3111111111",
            "password": "updated_password",
        },
    )
    assert response.status_code == 302
    with client.application.app_context():
        assert User.query.get(user.idusuario).nombreuser == "updated_user"

    client.get("/logout")
    login(client, admin.email, "admin_password")
    response = client.post(f"/User/delete/{user.idusuario}")
    assert response.status_code == 302
    with client.application.app_context():
        assert User.query.get(user.idusuario) is None