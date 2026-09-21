from app.models.catalogo_precio import CatalogoPrecio


def test_catalogo_create_edit_delete(client, admin):
    client.post("/login", data={"email": admin.email, "password": "admin_password"})

    response = client.get("/Catalogo/")
    assert response.status_code == 200

    response = client.post(
        "/Catalogo/nuevo",
        data={
            "nombre": "Paquete facial",
            "precio": "50000",
            "categoria": "Belleza",
            "descripcion": "Tratamiento facial básico",
        },
    )
    assert response.status_code == 302

    with client.application.app_context():
        item = CatalogoPrecio.query.filter_by(nombre="Paquete facial").one()
        item_id = item.idcatalogo

    response = client.post(
        f"/Catalogo/editar/{item_id}",
        data={
            "nombre": "Paquete facial premium",
            "precio": "65000",
            "categoria": "Belleza",
            "descripcion": "Tratamiento facial premium",
        },
    )
    assert response.status_code == 302

    with client.application.app_context():
        updated = CatalogoPrecio.query.get(item_id)
        assert updated.nombre == "Paquete facial premium"

    response = client.post(f"/Catalogo/eliminar/{item_id}")
    assert response.status_code == 302

    with client.application.app_context():
        assert CatalogoPrecio.query.get(item_id) is None
