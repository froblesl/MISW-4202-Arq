import base64
from flask import request
from ..modelos import db, Usuario, UsuarioSchema
from flask_restful import Resource
from datetime import datetime
from celery import Celery
from ..tasks import signin_task
from opentelemetry import trace
from flaskr.tracer import tracer  # Importa el tracer de tracer.py

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

usuario_schema = UsuarioSchema()
tracer = trace.get_tracer_provider()
class VistaSignIn(Resource):
    def post(self):
        tracer_provider = trace.get_tracer_provider()
        tracer = tracer_provider.get_tracer(__name__)
        with tracer.start_as_current_span('registro_colas'):
            # Obtén los datos de la solicitud
            usuario = request.json.get('usuario')
            password = request.json.get('password')
            nombre = request.json.get('nombre')
            telefono = request.json.get('telefono')
            correo = request.json.get('correo')

            # Llama a la tarea de Celery
            signin_task.apply_async(args=[usuario, password, nombre, telefono, correo], queue='signin_task')

            return {"mensaje": "La solicitud de inicio de sesión ha sido enviada y se está procesando."}, 202

