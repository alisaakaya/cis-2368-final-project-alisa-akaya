from flask import jsonify
from datetime import datetime

# Response helpers
def success_response(message, data=None, status_code=200):
    """Create a success response"""
    response = {
        'success': True,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code

def error_response(message, status_code=400):
    """Create an error response"""
    return jsonify({
        'success': False,
        'message': message
    }), status_code

# Date-related functions
def parse_date(date_str):
    """Parse date string in YYYY-MM-DD format"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None
