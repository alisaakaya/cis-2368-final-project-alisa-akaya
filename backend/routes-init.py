from routes.books import books_bp
from routes.customers import customers_bp
from routes.borrowing import borrowing_bp

def register_routes(app):
    """Register all blueprint routes"""
    app.register_blueprint(books_bp, url_prefix='/api/books')
    app.register_blueprint(customers_bp, url_prefix='/api/customers')
    app.register_blueprint(borrowing_bp, url_prefix='/api/borrowing')
