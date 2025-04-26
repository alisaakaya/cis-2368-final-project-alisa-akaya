import bcrypt
from db import get_connection, get_cursor
import psycopg2.extras

class Customer:
    @staticmethod
    def get_all():
        """Get all customers from the database."""
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT id, firstname, lastname, email FROM customers")
        customers = cur.fetchall()
        cur.close()
        conn.close()
        return customers
    
    @staticmethod
    def get_by_id(customer_id):
        """Get a customer by their ID."""
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT id, firstname, lastname, email FROM customers WHERE id = %s", (customer_id,))
        customer = cur.fetchone()
        cur.close()
        conn.close()
        return customer
    
    @staticmethod
    def create(firstname, lastname, email, password):
        """Create a new customer with hashed password."""
        # Generate salt and hash password
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            cur.execute(
                "INSERT INTO customers (firstname, lastname, email, passwordhash) VALUES (%s, %s, %s, %s) RETURNING id, firstname, lastname, email",
                (firstname, lastname, email, hashed_pw)
            )
            customer = cur.fetchone()
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            raise ValueError("Email already exists")
        finally:
            cur.close()
            conn.close()
        return customer
    
    @staticmethod
    def update(customer_id, firstname, lastname, email, password=None):
        """Update a customer's details, optionally updating password."""
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        if password:
            # Generate salt and hash password
            salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
            
            cur.execute(
                "UPDATE customers SET firstname = %s, lastname = %s, email = %s, passwordhash = %s WHERE id = %s RETURNING id, firstname, lastname, email",
                (firstname, lastname, email, hashed_pw, customer_id)
            )
        else:
            cur.execute(
                "UPDATE customers SET firstname = %s, lastname = %s, email = %s WHERE id = %s RETURNING id, firstname, lastname, email",
                (firstname, lastname, email, customer_id)
            )
        
        customer = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return customer
    
    @staticmethod
    def delete(customer_id):
        """Delete a customer."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM customers WHERE id = %s RETURNING id", (customer_id,))
        deleted = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return deleted