from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.extensions import db, migrate, ma
from app.api.black_white_list import bp as black_white_list_bp
from app.api.rule import bp as rule_bp
from app.config import Config
from app.api import contracts
from app.api.realtime_monitor import bp as realtime_monitor_bp
from app.api.contract_audit import bp as contract_audit_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS with specific configuration
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Range", "X-Total-Count"]
        }
    })

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # Register blueprints
    app.register_blueprint(black_white_list_bp)
    app.register_blueprint(rule_bp)
    app.register_blueprint(realtime_monitor_bp)
    app.register_blueprint(contracts.bp, url_prefix='/api')
    app.register_blueprint(contract_audit_bp)

    return app 

