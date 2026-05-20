from app import create_app, db
from app.models.citas import Citas
from app.models.usuario import User
from datetime import datetime

app = create_app()
with app.app_context():
    try:
        print("Testing DB query for all Citas...")
        citas = Citas.query.all()
        print(f"Success! Found {len(citas)} appointments.")
        
        # Find a user to assign the appointment to
        user = User.query.first()
        if user:
            print(f"Found user: {user.nombreuser} (ID: {user.idusuario})")
            
            # Create a test appointment
            print("Creating test appointment...")
            new_cita = Citas(
                fechahora=datetime.now(),
                servicio="Corte de cabello de prueba",
                estado="Pendiente",
                idusuario=user.idusuario
            )
            db.session.add(new_cita)
            db.session.commit()
            print(f"Appointment created successfully! ID: {new_cita.idcitas}")
            
            # Clean up the test appointment
            print("Cleaning up test appointment...")
            db.session.delete(new_cita)
            db.session.commit()
            print("Cleanup successful!")
        else:
            print("No users found to test creating appointment.")
            
    except Exception as e:
        print(f"Error during query/creation: {e}")
        import traceback
        traceback.print_exc()
