from flask import jsonify, request
from models.borrowing import Borrowing

def get_all_borrowings():
    """Get all borrowing records."""
    try:
        borrowings = Borrowing.get_all()
        return jsonify(borrowings), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_borrowing(borrowing_id):
    """Get a borrowing record by ID."""
    try:
        borrowing = Borrowing.get_by_id(borrowing_id)
        if borrowing:
            return jsonify(borrowing), 200
        return jsonify({"error": "Borrowing record not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_borrowing():
    """Create a new borrowing record."""
    try:
        data = request.get_json()
        bookid = data.get('bookid')
        customerid = data.get('customerid')
        borrowdate = data.get('borrowdate')
        
        if not all([bookid, customerid, borrowdate]):
            return jsonify({"error": "Missing required fields"}), 400
        
        borrowing = Borrowing.create(bookid, customerid, borrowdate)
        return jsonify(borrowing), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def return_book(borrowing_id):
    """Process a book return."""
    try:
        data = request.get_json()
        returndate = data.get('returndate')
        
        if not returndate:
            return jsonify({"error": "Return date is required"}), 400
        
        borrowing = Borrowing.return_book(borrowing_id, returndate)
        return jsonify(borrowing), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500