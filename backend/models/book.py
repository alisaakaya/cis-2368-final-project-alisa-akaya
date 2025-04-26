from db import get_connection, get_cursor
import psycopg2

class Book:
    @staticmethod
    def get_all():
        """Get all books from the database."""
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM books")
        books = cur.fetchall()
        cur.close()
        conn.close()
        return books
    
    @staticmethod
    def get_by_id(book_id):
        """Get a book by its ID."""
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        book = cur.fetchone()
        cur.close()
        conn.close()
        return book
    
    @staticmethod
    def create(title, author, genre, status="available"):
        """Create a new book."""
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "INSERT INTO books (title, author, genre, status) VALUES (%s, %s, %s, %s) RETURNING *",
            (title, author, genre, status)
        )
        book = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return book
    
    @staticmethod
    def update(book_id, title, author, genre, status):
        """Update a book."""
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "UPDATE books SET title = %s, author = %s, genre = %s, status = %s WHERE id = %s RETURNING *",
            (title, author, genre, status, book_id)
        )
        book = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return book
    
    @staticmethod
    def delete(book_id):
        """Delete a book."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM books WHERE id = %s RETURNING id", (book_id,))
        deleted = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return deleted
    
    @staticmethod
    def update_status(book_id, status):
        """Update a book's status."""
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "UPDATE books SET status = %s WHERE id = %s RETURNING *",
            (status, book_id)
        )
        book = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return book