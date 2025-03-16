from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.extensions import db, migrate, ma
from app.api.black_white_list import bp as black_white_list_bp
from app.views.rule import bp as rule_bp
from app.config import Config
from app.api import contracts

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS with specific configuration
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],  # 前端开发服务器地址
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # 允许的方法
            "allow_headers": ["Content-Type", "Authorization"],  # 允许的头部
            "expose_headers": ["Content-Range", "X-Total-Count"],  # 暴露的头部
            "supports_credentials": True  # 允许携带凭证
        }
    })

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # Register blueprints
    app.register_blueprint(black_white_list_bp)
    app.register_blueprint(rule_bp)
    app.register_blueprint(contracts.bp, url_prefix='/api')

    return app 