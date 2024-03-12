from datetime import datetime
from celery import Celery
from flaskr import create_app
from flaskr.modelos import db, Usuario, Entrenador, Deportista
from flaskr.tracer import tracer
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

@celery_app.task(name='signinEntrenador_task', autoretry_for=(Exception,), retry_backoff=True, max_retries=2)
def signinEntrenador_task(usuario, password, rol, nombre, telefono, correo, especialidad):
    app = create_app()
    db.init_app(app)
    user_info = None
    with app.app_context():
        with tracer.start_as_current_span('signin_task_span_entrenador') as span:
            try:
                nuevo_usuario = Usuario(usuario=usuario,
                                        password=password,
                                        rol=rol)
                nuevo_entrenador = Entrenador(nombre=nombre,
                                              telefono=telefono,
                                              correo=correo,
                                              especialidad=especialidad)
                nuevo_usuario.entrenador = nuevo_entrenador
                db.session.add(nuevo_usuario)
                db.session.commit()
                nuevo_entrenador.usuario_id = nuevo_usuario.id
                db.session.add(nuevo_entrenador)
                db.session.commit()
                user_info = {"mensaje": "Usuario creado exitosamente", "id": nuevo_usuario.id}
                span.set_attribute('user_info', dumps(user_info))
                return user_info
            except Exception as e:
                print(f"La tarea ha fallado con el error: {e}")
                span.set_status(Status(StatusCode.ERROR, "Error occurred: " + str(e)))
                user_info = "La tarea ha fallado con el error: " + str(e)
                return user_info
            finally:
                return user_info

@celery_app.task(name='signinDeportista_task', autoretry_for=(Exception,), retry_backoff=True, max_retries=2)
def signinDeportista_task(usuario, password, rol, nombre, telefono, correo, peso, estatura, fecha_nacimiento, sexo):
    app = create_app()
    db.init_app(app)
    user_info = None
    with app.app_context():
        with tracer.start_as_current_span('signin_task_span_deportista') as span:
            try:
                nuevo_usuario = Usuario(usuario=usuario,
                                        password=password,
                                        rol=rol)
                nuevo_deportista = Deportista(nombre=nombre,
                                                      telefono=telefono,
                                                      correo=correo,
                                                      peso=peso,
                                                      estatura=estatura,
                                                      fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%dT%H:%M:%S'),
                                                      sexo=sexo)
                nuevo_usuario.deportista = nuevo_deportista

                db.session.add(nuevo_usuario)
                db.session.commit()
                nuevo_deportista.usuario_id = nuevo_usuario.id
                db.session.add(nuevo_deportista)
                db.session.commit()
                user_info = {"mensaje": "Usuario creado exitosamente", "id": nuevo_usuario.id}
                span.set_attribute('user_info', dumps(user_info))
                return user_info
            except Exception as e:
                print(f"La tarea ha fallado con el error: {e}")
                span.set_status(Status(StatusCode.ERROR, "Error occurred: " + str(e)))
                user_info = "La tarea ha fallado con el error: " + str(e)
                return user_info
            finally:
                return user_info