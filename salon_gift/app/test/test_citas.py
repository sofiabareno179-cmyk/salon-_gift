from datetime import datetime, timedelta

from app import db
from app.models.agenda import Agenda
from app.models.citas import Citas


def test_citas_create_and_delete(client, user):
    client.post("/login", data={"email": user.email, "password": "test_password"})

    today = datetime.now()
    next_weekday = today + timedelta(days=(1 - today.weekday()) % 7 or 7)
    cita_date = next_weekday.strftime("%Y-%m-%d")
    weekday_name = next_weekday.strftime("%A")
    weekday_map = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo",
    }
    dia = weekday_map[weekday_name]

    with client.application.app_context():
        agenda = Agenda(
            diasemana=dia,
            horainicio="08:00",
            horafin="18:00",
            idusuario=user.idusuario,
        )
        db.session.add(agenda)
        db.session.commit()

    response = client.get("/Citas/citas")
    assert response.status_code == 200

    response = client.post(
        "/Citas/citas/nueva",
        data={
            "fechahora": f"{cita_date}T09:00",
            "servicio": "Corte de cabello",
            "estado": "Pendiente",
        },
    )
    assert response.status_code == 302

    with client.application.app_context():
        cita = Citas.query.filter_by(servicio="Corte de cabello").one()
        cita_id = cita.idcitas

    response = client.post(
        f"/Citas/citas/editar/{cita_id}",
        data={
            "estado": "Confirmada",
            "servicio": "Corte de cabello premium",
            "fechahora": f"{cita_date}T10:00",
        },
    )
    assert response.status_code == 302

    with client.application.app_context():
        updated = Citas.query.get(cita_id)
        assert updated.servicio == "Corte de cabello premium"
        assert updated.estado == "Confirmada"

    response = client.post(f"/Citas/citas/eliminar/{cita_id}")
    assert response.status_code == 302

    with client.application.app_context():
        assert Citas.query.get(cita_id) is None
