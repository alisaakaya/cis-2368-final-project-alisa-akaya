from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Book, Customer, BorrowingRecord
from routes import register_routes
from config import Config

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    
    # Register blueprints/routes
    register_routes(app)
    
    # Create error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Resource not found'
        }), 404
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'message': 'Bad request'
        }), 400
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500
    
    # Create a simple route for health check/testing
    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': 'Library Management System API is running',
            'api_version': '1.0.0'
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
