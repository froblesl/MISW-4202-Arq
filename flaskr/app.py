# app.py

from flaskr import create_app
from flask_restful import Api
from flaskr.vistas import VistaSignIn
from flaskr.modelos import db
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

import uptrace

app = create_app()
app_context = app.app_context()
app_context.push()

# Inicializar SQLAlchemy engine después de crear la aplicación
db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaSignIn, '/signin')

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.get_tracer_provider()

# Creates a tracer from the global tracer provider

# app.py


uptrace.configure_opentelemetry(
    dsn="https://oOcNZLnu7znxC_ENmcx9og@api.uptrace.dev?grpc=4317",
    service_name="myservice",
    service_version="1.0.0",
    deployment_environment="production",
)

tracer = trace.get_tracer("my.tracer.name", "1.0.0")
