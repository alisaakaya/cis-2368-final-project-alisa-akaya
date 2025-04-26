from datetime import datetime, timedelta
from db import get_connection, get_cursor
import psycopg2.extras

class Borrowing:
    @staticmethod
    def get_all():
        """Get all borrowing records."""
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT br.*, b.title as book_title, c.firstname, c.lastname
            FROM borrowingrecords br
            JOIN books b ON br.bookid = b.id
            JOIN customers c ON br.customerid = c.id
            ORDER BY 
                CASE WHEN br.returndate IS NULL THEN 0 ELSE 1 END,
                br.borrowdate DESC
        """)
        borrowings = cur.fetchall()
        cur.close()
        conn.close()
        return borrowings
    
    @staticmethod
    def get_by_id(borrowing_id):
        """Get a borrowing record by ID."""
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT br.*, b.title as book_title, c.firstname, c.lastname
            FROM borrowingrecords br
            JOIN books b ON br.bookid = b.id
            JOIN customers c ON br.customerid = c.id
            WHERE br.id = %s
        """, (borrowing_id,))
        borrowing = cur.fetchone()
        cur.close()
        conn.close()
        return borrowing
    
    @staticmethod
    def create(bookid, customerid, borrowdate):
        """Create a new borrowing record."""
        conn = get_connection()
        try:
            # Check if book is available
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT status FROM books WHERE id = %s", (bookid,))
            book = cur.fetchone()
            
            if not book or book['status'] != 'available':
                conn.close()
                raise ValueError("Book is not available for borrowing")
            
            # Check if customer already has a book borrowed
            cur.execute("""
                SELECT COUNT(*) as count FROM borrowingrecords
                WHERE customerid = %s AND returndate IS NULL
            """, (customerid,))
            result = cur.fetchone()
            
            if result['count'] > 0:
                conn.close()
                raise ValueError("Customer already has a book borrowed")
            
            # Update book status to unavailable
            cur.execute(
                "UPDATE books SET status = 'unavailable' WHERE id = %s",
                (bookid,)
            )
            
            # Create borrowing record
            cur.execute(
                "INSERT INTO borrowingrecords (bookid, customerid, borrowdate) VALUES (%s, %s, %s) RETURNING *",
                (bookid, customerid, borrowdate)
            )
            
            borrowing = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
            return borrowing
        
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    @staticmethod
    def return_book(borrowing_id, return_date):
        """Process a book return and calculate late fee if applicable."""
        conn = get_connection()
        try:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Get borrowing record
            cur.execute("SELECT * FROM borrowingrecords WHERE id = %s", (borrowing_id,))
            borrowing = cur.fetchone()
            
            if not borrowing:
                conn.close()
                raise ValueError("Borrowing record not found")
            
            if borrowing['returndate']:
                conn.close()
                raise ValueError("Book already returned")
            
            # Calculate late fee if return date is more than 10 days after borrow date
            borrow_date = borrowing['borrowdate']
            return_date_obj = datetime.strptime(return_date, '%Y-%m-%d').date()
            
            late_fee = 0.0
            days_borrowed = (return_date_obj - borrow_date).days
            
            if days_borrowed > 10:
                late_fee = (days_borrowed - 10) * 1.0  # $1 per day late
            
            # Update borrowing record
            cur.execute(
                "UPDATE borrowingrecords SET returndate = %s, late_fee = %s WHERE id = %s RETURNING *",
                (return_date, late_fee, borrowing_id)
            )
            updated_borrowing = cur.fetchone()
            
            # Update book status to available
            cur.execute(
                "UPDATE books SET status = 'available' WHERE id = %s",
                (borrowing['bookid'],)
            )
            
            conn.commit()
            cur.close()
            conn.close()
            return updated_borrowing
        
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e