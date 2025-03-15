from flask import Flask
from flask_cors import CORS
from app.extensions import db, migrate, ma
from app.api.black_white_list import bp as black_white_list_bp
from app.utils.error_handlers import register_error_handlers
from app.views.rule import bp as rule_bp
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # Register blueprints
    app.register_blueprint(black_white_list_bp, url_prefix='/api')
    app.register_blueprint(rule_bp, url_prefix='/api')

    # Register error handlers
    register_error_handlers(app)

    return app 