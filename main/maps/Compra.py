from marshmallow import Schema, fields, post_load, post_dump
from main.modelos import CompraModel
from .Usuario import UsuarioSchema

class CompraSchema(Schema):
    id = fields.Integer(dump_only = True)
    fecha_compra = fields.DateTime(required = True)
    usaurioId = fields.Integer(required = True)
    usaurio = fields.Nested(UsuarioSchema)
    
    @post_load
    def create_compra(self, data, **kwargas):
        return CompraModel(**data)
    
    SKIPE_VALUES = ['usuarioId']
    
    @post_dump
    def remove_skipe_values(self, data, **kwargas):
        return {
            key: value for key, value in data.items() if key not in self.SKIPE_VALUES
        }