from flask import Blueprint, request, jsonify
from models import db, Book, BorrowingRecord

books_bp = Blueprint('books', __name__)

# Get all books
@books_bp.route('/', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    return jsonify({
        'success': True,
        'books': [book.to_dict() for book in books]
    }), 200

# Get single book by ID
@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({
            'success': False,
            'message': 'Book not found'
        }), 404
    
    return jsonify({
        'success': True,
        'book': book.to_dict()
    }), 200

# Create a new book
@books_bp.route('/', methods=['POST'])
def create_book():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'author', 'genre']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'message': f'Missing required field: {field}'
            }), 400
    
    # Create new book
    new_book = Book(
        title=data['title'],
        author=data['author'],
        genre=data['genre'],
        status=data.get('status', 'available')
    )
    
    db.session.add(new_book)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Book created successfully',
        'book': new_book.to_dict()
    }), 201

# Update a book
@books_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({
            'success': False,
            'message': 'Book not found'
        }), 404
    
    data = request.get_json()
    
    # Update book fields
    if 'title' in data:
        book.title = data['title']
    if 'author' in data:
        book.author = data['author']
    if 'genre' in data:
        book.genre = data['genre']
    if 'status' in data:
        book.status = data['status']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Book updated successfully',
        'book': book.to_dict()
    }), 200

# Delete a book
@books_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({
            'success': False,
            'message': 'Book not found'
        }), 404
    
    # Check if book is currently borrowed
    active_borrowing = BorrowingRecord.query.filter_by(
        book_id=book_id,
        return_date=None
    ).first()
    
    if active_borrowing:
        return jsonify({
            'success': False,
            'message': 'Cannot delete book while it is being borrowed'
        }), 400
    
    db.session.delete(book)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Book deleted successfully'
    }), 200
