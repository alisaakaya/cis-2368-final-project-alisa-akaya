from flask import Blueprint
from controllers.customer_controller import get_all_customers, get_customer, create_customer, update_customer, delete_customer

customer_bp = Blueprint('customers', __name__)

customer_bp.route('/', methods=['GET'])(get_all_customers)
customer_bp.route('/<int:customer_id>', methods=['GET'])(get_customer)
customer_bp.route('/', methods=['POST'])(create_customer)
customer_bp.route('/<int:customer_id>', methods=['PUT'])(update_customer)
customer_bp.route('/<int:customer_id>', methods=['DELETE'])(delete_customer)