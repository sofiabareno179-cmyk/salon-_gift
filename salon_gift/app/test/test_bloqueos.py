from datetime import datetime

from app.models.bloqueo import Bloqueo


def test_bloqueos_index_create_and_delete(client, admin):
    client.post("/login", data={"email": admin.email, "password": "admin_password"})

    response = client.get("/Bloqueos/")
    assert response.status_code == 200

    response = client.post(
        "/Bloqueos/nuevo",
        data={
            "fecha": "2030-01-15",
            "hora_inicio": "09:00",
            "hora_fin": "10:00",
            "motivo": "Mantenimiento",
        },
    )
    assert response.status_code == 302

    with client.application.app_context():
        bloqueo = Bloqueo.query.filter_by(motivo="Mantenimiento").one()
        bloqueo_id = bloqueo.idbloqueo

    response = client.post(f"/Bloqueos/eliminar/{bloqueo_id}")
    assert response.status_code == 302

    with client.application.app_context():
        assert Bloqueo.query.get(bloqueo_id) is None
