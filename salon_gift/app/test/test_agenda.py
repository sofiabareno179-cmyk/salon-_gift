from app.models.agenda import Agenda


def test_agenda_create_edit_delete(client, user):
    client.post("/login", data={"email": user.email, "password": "test_password"})

    response = client.post(
        "/Agenda/agenda/nuevo",
        data={
            "diasemana": "Lunes",
            "horainicio": "09:00",
            "horafin": "18:00",
        },
    )
    assert response.status_code == 302

    with client.application.app_context():
        agenda = Agenda.query.filter_by(idusuario=user.idusuario, diasemana="Lunes").one()
        agenda_id = agenda.idagenda

    response = client.post(
        f"/Agenda/agenda/editar/{agenda_id}",
        data={
            "diasemana": "Martes",
            "horainicio": "10:00",
            "horafin": "17:00",
        },
    )
    assert response.status_code == 302

    with client.application.app_context():
        updated = Agenda.query.get(agenda_id)
        assert updated.diasemana == "Martes"

    response = client.post(f"/Agenda/agenda/eliminar/{agenda_id}")
    assert response.status_code == 302

    with client.application.app_context():
        assert Agenda.query.get(agenda_id) is None
