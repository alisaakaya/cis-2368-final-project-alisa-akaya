from flask import Blueprint
from controllers.book_controller import get_all_books, get_book, create_book, update_book, delete_book

book_bp = Blueprint('books', __name__)

book_bp.route('/', methods=['GET'])(get_all_books)
book_bp.route('/<int:book_id>', methods=['GET'])(get_book)
book_bp.route('/', methods=['POST'])(create_book)
book_bp.route('/<int:book_id>', methods=['PUT'])(update_book)
book_bp.route('/<int:book_id>', methods=['DELETE'])(delete_book)