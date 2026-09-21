from app.models.servicios import Servicio


def test_servicios_create_edit_delete(client, admin):
    client.post("/login", data={"email": admin.email, "password": "admin_password"})

    response = client.get("/Servicio/")
    assert response.status_code == 200

    response = client.post(
        "/Servicio/servicios/add/peluqueria",
        data={
            "nombre": "Corte moderno",
            "precio": "50000",
            "duracion": "45 min",
            "categoria": "peluqueria",
            "tip": "Incluye lavado",
        },
    )
    assert response.status_code == 302

    with client.application.app_context():
        servicio = Servicio.query.filter_by(nombre="Corte moderno").one()
        servicio_id = servicio.idservicio

    response = client.post(
        f"/Servicio/edit/{servicio_id}",
        data={
            "nombre": "Corte moderno premium",
            "precio": "65000",
            "duracion": "60 min",
            "categoria": "peluqueria",
            "tip": "Incluye lavado y peinado",
        },
    )
    assert response.status_code == 302

    with client.application.app_context():
        updated = Servicio.query.get(servicio_id)
        assert updated.nombre == "Corte moderno premium"

    response = client.post(f"/Servicio/delete/{servicio_id}")
    assert response.status_code == 302

    with client.application.app_context():
        assert Servicio.query.get(servicio_id) is None
