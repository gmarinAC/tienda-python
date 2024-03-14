import os
from flask import Flask
from dotenv import load_dotenv

from flask_restful import Api

from flask_sqlalchemy import SQLAlchemy

from flask_jwt_extended import JWTManager

from flask_mail import Mail

api = Api()
db = SQLAlchemy()
jwt = JWTManager()
mailsender = Mail()

def create_app():
    
    app = Flask(__name__)
    #cargo las variables de entorno
    load_dotenv()
    #configuracion de la base de datos
    
    PATH = os.getenv("DATABASE_PATH")
    DB_NAME = os.getenv("DATABASE_NAME")
    if not os.path.exists(f'{PATH}{DB_NAME}'):
        os.chdir(f'{PATH}')
        file = os.open(f'{DB_NAME}',os.O_CREAT)
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{PATH}{DB_NAME}'
    db.init_app(app)
    
    
    import main.resources as resources
    import main.controllers as controllers
    api.add_resource(resources.ClientesResource, '/clientes')
    api.add_resource(resources.ClienteResource, '/cliente/<id>')
    api.add_resource(resources.UsuariosResource, '/usuarios')
    api.add_resource(resources.UsuarioResource, '/usuario/<id>')
    api.add_resource(resources.ComprasResource, '/compras')
    api.add_resource(resources.CompraResource, '/compra/<id>')
    api.add_resource(resources.ProductosResource, '/productos')
    api.add_resource(resources.ProductoResource, '/producto/<id>')
    api.add_resource(resources.ProductosComprasResource, '/productos-compras')
    api.add_resource(resources.ProductoCompraResource, '/producto-compra/<id>')
    
    api.add_resource(controllers.CompraController,'/compra-controller/<id>')
    api.add_resource(controllers.ComprasController,'/compra-controller')
    
    api.init_app(app)
    
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    jwt.init_app(app)
    
    from main.auth import routes
    app.register_blueprint(auth.routes.auth)
    from main.mail import function
    app.register_blueprint(mail.function.mail)
    #Configurar mail
    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME') 
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER') 
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT') 
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') 
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME') 
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD') 
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER') 
    
    mailsender.init_app(app)
    
    return app