def login(client, email, password):
    return client.post(
        "/login",
        data={"email": email, "password": password},
        follow_redirects=False,
    )


def test_login_valido_y_invalido(client, user):
    response = login(client, user.email, "test_password")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/User/dashboard")

    client.get("/logout")
    response = client.post(
        "/login",
        data={"email": user.email, "password": "incorrecta"},
    )
    assert response.status_code == 200
    assert b"Credenciales inv\xc3\xa1lidas" in response.data