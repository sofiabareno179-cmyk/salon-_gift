from app.models.productos import Productos


def test_productos_create_edit_delete(client, user):
    client.post("/login", data={"email": user.email, "password": "test_password"})

    response = client.get("/Productos/productos")
    assert response.status_code == 200

    response = client.post(
        "/Productos/productos/nuevo",
        data={
            "nombre": "Aceite reparador",
            "descripcion": "Producto para cuidado capilar",
            "precio": "25000",
            "categoria": "Cuidado",
        },
    )
    assert response.status_code == 302

    with client.application.app_context():
        product = Productos.query.filter_by(nombre="Aceite reparador").one()
        product_id = product.idproductos

    response = client.post(
        f"/Productos/productos/editar/{product_id}",
        data={
            "nombre": "Aceite reparador plus",
            "descripcion": "Versión reforzada para cabello seco",
            "precio": "32000",
            "categoria": "Cuidado",
        },
    )
    assert response.status_code == 302

    with client.application.app_context():
        updated = Productos.query.get(product_id)
        assert updated.nombre == "Aceite reparador plus"

    response = client.post(f"/Productos/productos/eliminar/{product_id}")
    assert response.status_code == 302

    with client.application.app_context():
        assert Productos.query.get(product_id) is None
