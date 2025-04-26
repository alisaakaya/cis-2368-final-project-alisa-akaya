import psycopg2
from flask import jsonify, request
from models.book import Book

def get_all_books():
    """Get all books."""
    try:
        books = Book.get_all()
        return jsonify(books), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_book(book_id):
    """Get a book by ID."""
    try:
        book = Book.get_by_id(book_id)
        if book:
            return jsonify(book), 200
        return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_book():
    """Create a new book."""
    try:
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        genre = data.get('genre')
        status = data.get('status', 'available')
        
        if not all([title, author, genre]):
            return jsonify({"error": "Missing required fields"}), 400
        
        book = Book.create(title, author, genre, status)
        return jsonify(book), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_book(book_id):
    """Update a book."""
    try:
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        genre = data.get('genre')
        status = data.get('status')
        
        if not all([title, author, genre, status]):
            return jsonify({"error": "Missing required fields"}), 400
        
        book = Book.update(book_id, title, author, genre, status)
        if book:
            return jsonify(book), 200
        return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_book(book_id):
    """Delete a book."""
    try:
        deleted = Book.delete(book_id)
        if deleted:
            return jsonify({"message": "Book deleted successfully"}), 200
        return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500