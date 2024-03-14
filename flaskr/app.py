# app.py

from flaskr import create_app
from flask_restful import Api
from flaskr.vistas import VistaSignInEntrenador, VistaSignInDeportista
from flaskr.modelos import db
from flaskr.vistas.vistas import VistaAsignarDeportistaEntrenador, VistaConsultarDeportistasPorEntrenador, VistaLogin
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from flask_jwt_extended import JWTManager

import uptrace

app = create_app()
app.config['JWT_SECRET_KEY'] = 'd3b1149cebbc40bbf20fd74cf32cde34389f21f3a4cfc962a384d526bcadd264'  # Reemplaza esto con tu propia clave secreta
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)

app_context = app.app_context()
app_context.push()

# Inicializar SQLAlchemy engine después de crear la aplicación
db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaSignInEntrenador, '/signinEntrenador')
api.add_resource(VistaSignInDeportista, '/signinDeportista')
api.add_resource(VistaAsignarDeportistaEntrenador, '/asignarDeportista')
api.add_resource(VistaConsultarDeportistasPorEntrenador, '/consultarDeportistasPorEntrenador/<int:id_entrenador>')
api.add_resource(VistaLogin, '/login')

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.get_tracer_provider()

# Creates a tracer from the global tracer provider

uptrace.configure_opentelemetry(
    dsn="https://oOcNZLnu7znxC_ENmcx9og@api.uptrace.dev?grpc=4317",
    service_name="myservice",
    service_version="1.0.0",
    deployment_environment="production",
)

tracer = trace.get_tracer("my.tracer.name", "1.0.0")