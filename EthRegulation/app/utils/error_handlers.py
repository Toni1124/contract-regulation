from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({
            'code': 400,
            'message': 'Validation error',
            'errors': error.messages
        }), 400

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        return jsonify({
            'code': 400,
            'message': 'Database integrity error',
        }), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({
            'code': 404,
            'message': 'Resource not found'
        }), 404 