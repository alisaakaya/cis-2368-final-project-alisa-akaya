from flask import Blueprint, request, jsonify
from models import db, Book, Customer, BorrowingRecord
from datetime import datetime

borrowing_bp = Blueprint('borrowing', __name__)

# Get all borrowing records
@borrowing_bp.route('/', methods=['GET'])
def get_all_borrowings():
    # Option to filter only active borrowings
    active_only = request.args.get('active', 'false').lower() == 'true'
    
    if active_only:
        borrowings = BorrowingRecord.query.filter_by(return_date=None).all()
    else:
        borrowings = BorrowingRecord.query.all()
    
    return jsonify({
        'success': True,
        'borrowings': [borrowing.to_dict() for borrowing in borrowings]
    }), 200

# Get a single borrowing record
@borrowing_bp.route('/<int:borrowing_id>', methods=['GET'])
def get_borrowing(borrowing_id):
    borrowing = BorrowingRecord.query.get(borrowing_id)
    if not borrowing:
        return jsonify({
            'success': False,
            'message': 'Borrowing record not found'
        }), 404
    
    return jsonify({
        'success': True,
        'borrowing': borrowing.to_dict()
    }), 200

# Create a new borrowing record
@borrowing_bp.route('/', methods=['POST'])
def create_borrowing():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['book_id', 'customer_id', 'borrow_date']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'message': f'Missing required field: {field}'
            }), 400
    
    # Validate book exists and is available
    book = Book.query.get(data['book_id'])
    if not book:
        return jsonify({
            'success': False,
            'message': 'Book not found'
        }), 404
    
    if book.status != 'available':
        return jsonify({
            'success': False,
            'message': 'Book is not available for borrowing'
        }), 400
    
    # Validate customer exists and can borrow
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({
            'success': False,
            'message': 'Customer not found'
        }), 404
    
    if customer.has_active_borrowing():
        return jsonify({
            'success': False,
            'message': 'Customer already has an active borrowing'
        }), 400
    
    # Parse borrow date
    try:
        borrow_date = datetime.strptime(data['borrow_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({
            'success': False,
            'message': 'Invalid date format. Use YYYY-MM-DD'
        }), 400
    
    # Create borrowing record
    new_borrowing = BorrowingRecord(
        book_id=data['book_id'],
        customer_id=data['customer_id'],
        borrow_date=borrow_date
    )
    
    # Update book status
    book.status = 'unavailable'
    
    db.session.add(new_borrowing)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Borrowing record created successfully',
        'borrowing': new_borrowing.to_dict()
    }), 201

# Return a book (update borrowing record with return date)
@borrowing_bp.route('/<int:borrowing_id>/return', methods=['PUT'])
def return_book(borrowing_id):
    borrowing = BorrowingRecord.query.get(borrowing_id)
    if not borrowing:
        return jsonify({
            'success': False,
            'message': 'Borrowing record not found'
        }), 404
    
    # Check if book is already returned
    if borrowing.return_date:
        return jsonify({
            'success': False,
            'message': 'Book has already been returned'
        }), 400
    
    data = request.get_json()
    
    # Parse return date
    try:
        if 'return_date' in data:
            return_date = datetime.strptime(data['return_date'], '%Y-%m-%d').date()
        else:
            # Use current date if not provided
            return_date = datetime.now().date()
    except ValueError:
        return jsonify({
            'success': False,
            'message': 'Invalid date format. Use YYYY-MM-DD'
        }), 400
    
    # Update borrowing record
    borrowing.return_date = return_date
    borrowing.calculate_late_fee()
    
    # Update book status to available
    book = Book.query.get(borrowing.book_id)
    if book:
        book.status = 'available'
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Book returned successfully',
        'borrowing': borrowing.to_dict()
    }), 200

# Get borrowings by customer ID
@borrowing_bp.route('/customer/<int:customer_id>', methods=['GET'])
def get_customer_borrowings(customer_id):
    # Verify customer exists
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({
            'success': False,
            'message': 'Customer not found'
        }), 404
    
    # Get customer's borrowing records
    active_only = request.args.get('active', 'false').lower() == 'true'
    
    if active_only:
        borrowings = BorrowingRecord.query.filter_by(
            customer_id=customer_id,
            return_date=None
        ).all()
    else:
        borrowings = BorrowingRecord.query.filter_by(
            customer_id=customer_id
        ).all()
    
    return jsonify({
        'success': True,
        'customer': customer.to_dict(),
        'borrowings': [borrowing.to_dict() for borrowing in borrowings]
    }), 200

# Get borrowings by book ID
@borrowing_bp.route('/book/<int:book_id>', methods=['GET'])
def get_book_borrowings(book_id):
    # Verify book exists
    book = Book.query.get(book_id)
    if not book:
        return jsonify({
            'success': False,
            'message': 'Book not found'
        }), 404
    
    # Get book's borrowing records
    borrowings = BorrowingRecord.query.filter_by(book_id=book_id).all()
    
    return jsonify({
        'success': True,
        'book': book.to_dict(),
        'borrowings': [borrowing.to_dict() for borrowing in borrowings]
    }), 200
