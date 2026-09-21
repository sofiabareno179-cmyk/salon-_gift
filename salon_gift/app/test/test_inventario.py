from app.models.inventario import Inventario


def test_inventario_create_edit_delete(client, user):
    client.post("/login", data={"email": user.email, "password": "test_password"})

    response = client.get("/Inventario/inventario")
    assert response.status_code == 200

    response = client.post(
        "/Inventario/inventario/nuevo",
        data={
            "stock": "12",
            "fecha": "2026-09-21",
        },
    )
    assert response.status_code == 302

    with client.application.app_context():
        item = Inventario.query.filter_by(stock=12).one()
        item_id = item.idinventario

    response = client.post(
        f"/Inventario/inventario/editar/{item_id}",
        data={
            "stock": "15",
            "fecha": "2026-09-22",
        },
    )
    assert response.status_code == 302

    with client.application.app_context():
        updated = Inventario.query.get(item_id)
        assert updated.stock == 15

    response = client.post(f"/Inventario/inventario/eliminar/{item_id}")
    assert response.status_code == 302

    with client.application.app_context():
        assert Inventario.query.get(item_id) is None
