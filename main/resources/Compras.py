from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.modelos import CompraModel
from main.auth.decorators import rol_required
from flask_jwt_extended import get_jwt_identity

class Compra(Resource):
    @rol_required(roles=['Admin','cliente'])
    def get(self, id):
        
        compra = db.session.query(CompraModel).get_or_404(id)
        currente_user = get_jwt_identity()
        if currente_user['usuarioId'] == compra.usuarioId or currente_user['role']=='Admin':
            try:
                return compra.to_json()
            except:
                return 'Resource not found'
        else:
            return 'Unauthorized', 401
        
    @rol_required(roles=['Admin','cliente'])  
    def put(self, id):
        compra = db.session.query(CompraModel).get_or_404(id)
        data = request.get_json().item()
        currente_user = get_jwt_identity()
        if currente_user['usuarioId'] == compra.usuarioId or currente_user['role']=='Admin':
            for key,value in data:
                setattr(compra, key, value)
            try:
                db.session.add(compra)
                db.session.commit()
                return compra.to_json(),201
            except:
                return '', 404
        else:
            return 'Unauthorized', 401
        

class Compras(Resource):
    @rol_required(roles=['Admin'])
    def get(self):
        page = 1
        per_page = 5
        compras = db.session.query(CompraModel)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                elif key == 'per_page':
                    per_page = int(value)
        compras = compras.paginate(page, per_page, True, 10)
        return jsonify({
            'compras': [compra.to_json() for compra in compras.items],
            'total': compras.total,
            'pages': compras.pages,
            'page': page
        })

    @rol_required(roles=['Admin','cliente']) 
    def post(self):
        compra = CompraModel.from_json(request.get_json())
        db.session.add(compra)
        db.session.commit()
        return compra.to_json(), 201
        