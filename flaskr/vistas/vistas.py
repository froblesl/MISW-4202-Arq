import base64
from flask import request, json, Response,jsonify
from ..modelos import db, Usuario, UsuarioSchema, deportistas_entrenadores, Deportista, deportista_schema
from flask_restful import Resource
from datetime import datetime
from celery import Celery
from ..tasks import signinEntrenador_task, signinDeportista_task
from sqlalchemy import and_

from opentelemetry import trace
from flaskr.tracer import tracer  # Importa el tracer de tracer.py

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

usuario_schema = UsuarioSchema()
tracer = trace.get_tracer_provider()
class VistaSignInEntrenador(Resource):
    def post(self):
        tracer_provider = trace.get_tracer_provider()
        tracer = tracer_provider.get_tracer(__name__)
        with tracer.start_as_current_span('registro_colas'):
            usuario = request.json.get('usuario')
            password = request.json.get('password')
            rol = request.json.get('rol')
            nombre = request.json.get('nombre')
            telefono = request.json.get('telefono')
            correo = request.json.get('correo')
            especialidad = request.json.get('especialidad')

            signinEntrenador_task.apply_async(args=[usuario, password, rol, nombre, telefono, correo, especialidad], queue='signinEntrenador_task')

            return {"mensaje": "La solicitud de registro entrenador ha sido enviada y se está procesando."}, 202

class VistaSignInDeportista(Resource):
    def post(self):
        usuario = request.json.get('usuario')
        password = request.json.get('password')
        rol = request.json.get('rol')
        nombre = request.json.get('nombre')
        telefono = request.json.get('telefono')
        correo = request.json.get('correo')
        peso = request.json.get('peso')
        estatura = request.json.get('estatura')
        fecha_nacimiento = datetime.strptime(request.json.get('fecha_nacimiento'), '%Y-%m-%d')
        sexo = request.json.get('sexo')

        signinDeportista_task.apply_async(args=[usuario, password, rol, nombre, telefono, correo, peso, estatura, fecha_nacimiento, sexo], queue='signinDeportista_task')

        return {"mensaje": "La solicitud de registro deportista ha sido enviada y se está procesando."}, 202

class VistaAsignarDeportistaEntrenador(Resource):
    def post(self):
        id_deportista = request.json.get('id_deportista')
        id_entrenador = request.json.get('id_entrenador')
        deportista_entrenador = deportistas_entrenadores.insert().values(deportista_id=id_deportista, entrenador_id=id_entrenador)
        db.session.execute(deportista_entrenador)
        db.session.commit()
        
        return {"mensaje": "Deportista asignado a entrenador"}, 200

class VistaConsultarDeportistasPorEntrenador(Resource):
    def get(self, id_entrenador):
        # Verifica que el entrenador exista y tiene deportistas asociados directamente en la consulta
        deportistas = db.session.query(Deportista).join(
            deportistas_entrenadores,
            and_(
                deportistas_entrenadores.c.deportista_id == Deportista.id,
                deportistas_entrenadores.c.entrenador_id == id_entrenador
            )
        ).all()
        print(deportistas)
        return deportista_schema.dump(deportistas)
