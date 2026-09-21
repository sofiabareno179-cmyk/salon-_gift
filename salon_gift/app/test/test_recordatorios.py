from app.models.recordatorios import Recordatorios


def test_recordatorios_crud(client, user):
    client.post("/login", data={"email": user.email, "password": "test_password"})
    response = client.post(
        "/Recordatorios/recordatorios/nuevo",
        data={
            "titulo": "Comprar tinte",
            "mensaje": "Comprar antes del viernes",
            "fecha_recordatorio": "2026-09-25",
        },
    )
    assert response.status_code == 302
    with client.application.app_context():
        reminder = Recordatorios.query.filter_by(titulo="Comprar tinte").one()
        assert reminder.idusuario == user.idusuario
        reminder_id = reminder.idrecordatorios

    response = client.post(
        f"/Recordatorios/recordatorios/editar/{reminder_id}",
        data={
            "titulo": "Comprar shampoo",
            "mensaje": "Comprar esta semana",
            "fecha_recordatorio": "2026-09-26",
        },
    )
    assert response.status_code == 302
    response = client.post(f"/Recordatorios/recordatorios/eliminar/{reminder_id}")
    assert response.status_code == 302