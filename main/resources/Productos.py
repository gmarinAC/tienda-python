from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.modelos import ProductoModel
from main.auth.decorators import rol_required
from flask_jwt_extended import get_jwt_identity


class Producto(Resource):
    def get(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        try:
            return producto.to_json()
        except:
            return 'Resource not found'
    
    @rol_required(roles=['Admin'])   
    def put(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(producto, key, value)
        try:
            db.session.add(producto)
            db.session.commit()
            return producto.to_json(), 201
        except:
            return '', 404
        
    @rol_required(roles=['Admin'])
    def delete(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        try:
            db.session.delete(producto)
            db.session.commit()
        except:
            return 'Noexiste el producto', 404
class Productos(Resource):
    
    def get(self):
        page = 1
        per_page = 5
        productos = db.session.query(ProductoModel) #productos = db.session.query(ProductoModel).all()
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                elif key == 'per_page':
                    per_page = int(value)
        productos = productos.paginate(page, per_page, True, 15)
        return jsonify(
             {
                 'productos':[producto.to_json() for producto in productos.items],
                 'total':productos.total,
                 'pages':productos.pages,
                 'page':page
             }
        )
    
    @rol_required(roles=['Admin'])
    def post(self):
        producto = ProductoModel.from_json(request.get_json())
        db.session.add(producto)
        db.session.commit()
        return producto.to_json(), 201