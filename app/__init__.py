from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

db = SQLAlchemy()
jwt = JWTManager()
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 604800
  

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Import and register routes
    from .routes import init_routes
    init_routes(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    # JWT blacklist check
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        token = RevokedToken.query.filter_by(jti=jti).first()
        return token is not None

    return app

from .models import RevokedToken  # Import here to avoid circular imports