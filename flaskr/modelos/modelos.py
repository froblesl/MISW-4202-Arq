from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    password = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(65), nullable=False)
    telefono = db.Column(db.String(10), nullable=False)
    correo = db.Column(db.String(200), nullable=False)
    

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True