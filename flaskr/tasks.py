import time
from celery import Celery, exceptions
from flaskr import create_app
from flaskr.modelos import db, Usuario

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

@celery_app.task(name='signin_task', autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def signin_task(usuario, password, nombre, telefono, correo):
    with create_app().app_context():
        try:
            nuevo_usuario = Usuario(usuario=usuario,
                                    password=password,
                                    nombre=nombre,
                                    telefono=telefono,
                                    correo=correo)
            db.session.add(nuevo_usuario)
            db.session.commit()
            return {"mensaje": "Usuario creado exitosamente", "id": nuevo_usuario.id}
        except Exception as e:
            print(f"La tarea ha fallado con el error: {e}")
            raise  # Vuelve a lanzar la excepción para que Celery sepa que la tarea ha fallado