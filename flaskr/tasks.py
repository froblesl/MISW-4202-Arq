import time
from celery import Celery
from flaskr import create_app
from flaskr.modelos import db, Usuario

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

@celery_app.task(name='signin_task')
def signin_task(usuario, password, nombre, telefono, correo):
    app = create_app('default')
    db.init_app(app)
    with app.app_context():
        nuevo_usuario = Usuario(usuario=usuario,
                                password=password,
                                nombre=nombre,
                                telefono=telefono,
                                correo=correo)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {"mensaje": "Usuario creado exitosamente", "id": nuevo_usuario.id}