from app import db
from app.models.notificacion import Notificacion


def test_notificaciones_marcar_leida_y_todas(client, user):
    client.post("/login", data={"email": user.email, "password": "test_password"})
    with client.application.app_context():
        notification = Notificacion(
            idusuario=user.idusuario,
            titulo="Aviso",
            mensaje="Tienes una cita",
        )
        db.session.add(notification)
        db.session.commit()
        notification_id = notification.idnotificacion

    response = client.get(f"/Notificaciones/marcar-leida/{notification_id}")
    assert response.status_code == 302
    with client.application.app_context():
        assert Notificacion.query.get(notification_id).leida is True

    response = client.get("/Notificaciones/marcar-todas")
    assert response.status_code == 302