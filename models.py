from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.hash import pbkdf2_sha256

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='available')  # 'available' or 'unavailable'
    
    # Relationship with BorrowingRecord
    borrowing_records = db.relationship('BorrowingRecord', backref='book', lazy=True, cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'status': self.status
        }


class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    passwordhash = db.Column(db.String(255), nullable=False)
    
    # Relationship with BorrowingRecord
    borrowing_records = db.relationship('BorrowingRecord', backref='customer', lazy=True, cascade="all, delete-orphan")
    
    @staticmethod
    def hash_password(password):
        return pbkdf2_sha256.hash(password)
    
    @staticmethod
    def verify_password(password, hash):
        return pbkdf2_sha256.verify(password, hash)
    
    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email
        }
    
    def has_active_borrowing(self):
        # Check if customer has any active borrowing (no return date)
        active_borrowings = BorrowingRecord.query.filter_by(
            customer_id=self.id, 
            return_date=None
        ).count()
        return active_borrowings > 0


class BorrowingRecord(db.Model):
    __tablename__ = 'borrowingrecords'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    borrow_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.Date, nullable=True)
    late_fee = db.Column(db.Float, nullable=True, default=0.0)
    
    def calculate_late_fee(self):
        """Calculate late fee if book is returned after 10 days"""
        if self.return_date and self.borrow_date:
            # Calculate days borrowed
            days_borrowed = (self.return_date - self.borrow_date).days
            # If more than 10 days, charge $1 per extra day
            if days_borrowed > 10:
                self.late_fee = (days_borrowed - 10) * 1.0
            else:
                self.late_fee = 0.0
        return self.late_fee
    
    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'book_title': self.book.title if self.book else None,
            'customer_id': self.customer_id,
            'customer_name': f"{self.customer.firstname} {self.customer.lastname}" if self.customer else None,
            'borrow_date': self.borrow_date.strftime('%Y-%m-%d') if self.borrow_date else None,
            'return_date': self.return_date.strftime('%Y-%m-%d') if self.return_date else None,
            'late_fee': self.late_fee
        }
