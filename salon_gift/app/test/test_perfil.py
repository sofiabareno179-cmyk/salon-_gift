from app import db
from app.models.perfil import Perfil


def test_perfil_add_y_edit(client, user):
    client.post("/login", data={"email": user.email, "password": "test_password"})
    response = client.post(
        "/perfil/add",
        data={"nombre": "Test", "apellido": "User", "bio": "Mi bio"},
    )
    assert response.status_code == 302
    with client.application.app_context():
        profile = Perfil.query.filter_by(idusuario=user.idusuario).one()
        profile_id = profile.id

    response = client.post(
        f"/perfil/edit/{profile_id}",
        data={
            "nombre": "Updated",
            "apellido": "User",
            "bio": "Nueva bio",
            "nombreuser": user.nombreuser,
            "email": user.email,
            "telefono": "3000000002",
        },
    )
    assert response.status_code == 302
    with client.application.app_context():
        assert Perfil.query.get(profile_id).nombre == "Updated"