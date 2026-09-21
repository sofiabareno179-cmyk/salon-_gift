from app.models.proveedores import Proveedores


def test_proveedores_create_edit_delete(client, user):
    client.post("/login", data={"email": user.email, "password": "test_password"})

    response = client.get("/Proveedores/proveedores")
    assert response.status_code == 200

    response = client.post(
        "/Proveedores/proveedores/nuevo",
        data={
            "nombre_empresa": "Belleza Plus",
            "contacto_nombre": "Ana Gómez",
            "telefono": "3201234567",
            "email": "ana@bellezaplus.com",
            "direccion": "Calle 10 # 20-30",
        },
    )
    assert response.status_code == 302

    with client.application.app_context():
        proveedor = Proveedores.query.filter_by(nombre_empresa="Belleza Plus").one()
        proveedor_id = proveedor.idproveedores

    response = client.post(
        f"/Proveedores/proveedores/editar/{proveedor_id}",
        data={
            "nombre_empresa": "Belleza Plus Premium",
            "contacto_nombre": "Ana Gómez",
            "telefono": "3201234568",
            "email": "ana@premium.com",
            "direccion": "Calle 15 # 30-40",
        },
    )
    assert response.status_code == 302

    with client.application.app_context():
        updated = Proveedores.query.get(proveedor_id)
        assert updated.nombre_empresa == "Belleza Plus Premium"

    response = client.post(f"/Proveedores/proveedores/eliminar/{proveedor_id}")
    assert response.status_code == 302

    with client.application.app_context():
        assert Proveedores.query.get(proveedor_id) is None
