from app.models.frases import Frase


def test_frases_index_y_edicion(client, admin):
    client.post("/login", data={"email": admin.email, "password": "admin_password"})
    response = client.get("/Frases/")
    assert response.status_code == 200

    response = client.post(
        "/Frases/",
        data={"titulo": "Frase nueva", "descripcion": "Sigue adelante", "activa": "on"},
    )
    assert response.status_code == 302
    with client.application.app_context():
        phrase = Frase.query.filter_by(titulo="Frase nueva").one()
        assert phrase.activa is True