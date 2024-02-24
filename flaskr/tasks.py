import time
from celery import Celery, exceptions
from flaskr import create_app
from flaskr.modelos import db, Usuario
from flaskr.tracer import tracer  # Importa el tracer de tracer.py
import uptrace
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode
from json import dumps

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

uptrace.configure_opentelemetry(
    dsn="https://oOcNZLnu7znxC_ENmcx9og@api.uptrace.dev?grpc=4317",
    service_name="myservice",
    service_version="1.0.0",
    deployment_environment="production",
)
tracer = trace.get_tracer("flaskr", "1.0.0")

@celery_app.task(name='signin_task', autoretry_for=(Exception,), retry_backoff=True, max_retries=2)
def signin_task(usuario, password, nombre, telefono, correo):
    app = create_app()
    db.init_app(app)
    user_info = None
    with app.app_context():
        with tracer.start_as_current_span('signin_task_span') as span:
            try:
                nuevo_usuario = Usuario(usuario=usuario,
                                        password=password,
                                        nombre=nombre,
                                        telefono=telefono,
                                        correo=correo)
                db.session.add(nuevo_usuario)
                db.session.commit()
                user_info = {"mensaje": "Usuario creado exitosamente", "id": nuevo_usuario.id}
                span.set_attribute('user_info', dumps(user_info))  # Convierte el diccionario a una cadena
                return user_info
            except Exception as e:
                print(f"La tarea ha fallado con el error: {e}")
                span.set_status(Status(StatusCode.ERROR, "Error occurred: " + str(e)))
                user_info = "La tarea ha fallado con el error: " + str(e)
                return user_info
            finally:
                return user_info
