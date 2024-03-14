from marshmallow import Schema, fields, post_load, post_dump
from main.modelos import UsuarioModel

class UsuarioSchema(Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String(required=True)
    apellido = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    role = fields.String(required=True)
    telefono = fields.String(required=True)
    fecha_registro = fields.DateTime(required=True)
    
    @post_load
    def create_usaurio(self,data, **kwargas):
        return UsuarioModel(**data)
    
    SKIPE_VALUES = ['password']
    @post_dump
    def remove_skipe_values(self, data, **kwargas):
        return {
            key: value for key, value in data.items() if key not in self.SKIPE_VALUES
        }