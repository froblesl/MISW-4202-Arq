import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Rol(enum.Enum):
    ADMINISTRADOR = 1
    DEPORTISTA = 2
    ENTRENADOR = 3
    NUTRIOLOGO = 4
    MEDICO = 5
    PSICOLOGO = 6
    
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    password = db.Column(db.String(50), nullable=False)
    rol = db.Column(db.Enum(Rol), nullable=False)


class Deportista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(65), nullable=False)
    telefono = db.Column(db.String(10), nullable=False)
    correo = db.Column(db.String(200), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    estatura = db.Column(db.Float, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class Entrenador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(65), nullable=False)
    telefono = db.Column(db.String(10), nullable=False)
    correo = db.Column(db.String(200), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    deportistas = db.relationship('Deportista', secondary='deportistas_entrenadores', backref='entrenadores')
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    
deportistas_entrenadores = db.Table('deportistas_entrenadores',
    db.Column('deportista_id', db.Integer, db.ForeignKey('deportista.id'), primary_key=True),
    db.Column('entrenador_id', db.Integer, db.ForeignKey('entrenador.id'), primary_key=True)
)

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True

class DeportistaSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'nombre', 'telefono', 'correo', 'peso', 'estatura', 'fecha_nacimiento', 'sexo')

deportista_schema = DeportistaSchema(many=True)