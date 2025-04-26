from flask import Flask
from flask_cors import CORS
from routes.book_routes import book_bp
from routes.customer_routes import customer_bp
from routes.borrowing_routes import borrowing_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(book_bp, url_prefix='/api/books')
app.register_blueprint(customer_bp, url_prefix='/api/customers')
app.register_blueprint(borrowing_bp, url_prefix='/api/borrowings')

@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'healthy'}, 200

@app.route('/')
def home():
    return 'Welcome to the Library System API!'

if __name__ == '__main__':
    app.run(debug=True, port=5000)