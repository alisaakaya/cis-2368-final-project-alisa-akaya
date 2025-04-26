from flask import jsonify, request
from models.customer import Customer

def get_all_customers():
    """Get all customers."""
    try:
        customers = Customer.get_all()
        return jsonify(customers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_customer(customer_id):
    """Get a customer by ID."""
    try:
        customer = Customer.get_by_id(customer_id)
        if customer:
            return jsonify(customer), 200
        return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_customer():
    """Create a new customer."""
    try:
        data = request.get_json()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')
        password = data.get('password')
        
        if not all([firstname, lastname, email, password]):
            return jsonify({"error": "Missing required fields"}), 400
        
        customer = Customer.create(firstname, lastname, email, password)
        return jsonify(customer), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_customer(customer_id):
    """Update a customer."""
    try:
        data = request.get_json()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')
        password = data.get('password')  # Optional
        
        if not all([firstname, lastname, email]):
            return jsonify({"error": "Missing required fields"}), 400
        
        customer = Customer.update(customer_id, firstname, lastname, email, password)
        if customer:
            return jsonify(customer), 200
        return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_customer(customer_id):
    """Delete a customer."""
    try:
        deleted = Customer.delete(customer_id)
        if deleted:
            return jsonify({"message": "Customer deleted successfully"}), 200
        return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500