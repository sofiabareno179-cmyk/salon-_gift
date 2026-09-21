from io import BytesIO

from app import db
from app.models.galeria import Galeria


def test_galeria_crud(client, admin):
    client.post("/login", data={"email": admin.email, "password": "admin_password"})
    response = client.post(
        "/Galeria/nueva",
        data={
            "titulo": "Antes y despues",
            "descripcion": "Trabajo de color",
            "archivo": (BytesIO(b"fake image"), "galeria.jpg"),
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 302
    with client.application.app_context():
        item = Galeria.query.filter_by(titulo="Antes y despues").one()
        item_id = item.idgaleria

    response = client.post(
        f"/Galeria/editar/{item_id}",
        data={"titulo": "Resultado final", "descripcion": "Actualizado"},
    )
    assert response.status_code == 302
    response = client.post(f"/Galeria/eliminar/{item_id}")
    assert response.status_code == 302
    with client.application.app_context():
        assert Galeria.query.get(item_id) is None