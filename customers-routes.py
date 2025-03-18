from flask import Blueprint, request, jsonify
from models import db, Customer, BorrowingRecord

customers_bp = Blueprint('customers', __name__)

# Get all customers
@customers_bp.route('/', methods=['GET'])
def get_all_customers():
    customers = Customer.query.all()
    return jsonify({
        'success': True,
