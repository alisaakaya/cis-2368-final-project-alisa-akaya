from flask import Blueprint
from controllers.borrowing_controller import get_all_borrowings, get_borrowing, create_borrowing, return_book

borrowing_bp = Blueprint('borrowings', __name__)

borrowing_bp.route('/', methods=['GET'])(get_all_borrowings)
borrowing_bp.route('/<int:borrowing_id>', methods=['GET'])(get_borrowing)
borrowing_bp.route('/', methods=['POST'])(create_borrowing)
borrowing_bp.route('/<int:borrowing_id>/return', methods=['PUT'])(return_book)