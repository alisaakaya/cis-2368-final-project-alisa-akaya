const express = require('express');
const axios = require('axios');
const path = require('path');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Set EJS as templating engine
app.set('view engine', 'ejs');

// Routes (we'll add these next)

// Start server
app.listen(port, () => {
  console.log(`Frontend server running on http://localhost:${port}`);
});

// Home route
app.get('/', (req, res) => {
  res.render('index');
});

// Books routes
app.get('/books', async (req, res) => {
  try {
    const response = await axios.get(`${process.env.BACKEND_API_URL}/books`);
    res.render('books', { books: response.data });
  } catch (error) {
    console.error('Error fetching books:', error);
    res.render('books', { books: [], error: 'Failed to fetch books' });
  }
});

app.post('/books', async (req, res) => {
  try {
    await axios.post(`${process.env.BACKEND_API_URL}/books`, req.body);
    res.redirect('/books');
  } catch (error) {
    console.error('Error adding book:', error);
    res.redirect('/books');
  }
});

app.post('/books/:id/update', async (req, res) => {
  try {
    await axios.put(`${process.env.BACKEND_API_URL}/books/${req.params.id}`, req.body);
    res.redirect('/books');
  } catch (error) {
    console.error('Error updating book:', error);
    res.redirect('/books');
  }
});

app.post('/books/:id/delete', async (req, res) => {
  try {
    await axios.delete(`${process.env.BACKEND_API_URL}/books/${req.params.id}`);
    res.redirect('/books');
  } catch (error) {
    console.error('Error deleting book:', error);
    res.redirect('/books');
  }
});

// Customer routes
app.get('/customers', async (req, res) => {
  try {
    const response = await axios.get(`${process.env.BACKEND_API_URL}/customers`);
    res.render('customers', { customers: response.data });
  } catch (error) {
    console.error('Error fetching customers:', error);
    res.render('customers', { customers: [], error: 'Failed to fetch customers' });
  }
});

app.post('/customers', async (req, res) => {
  try {
    // Handle password hashing on the backend
    await axios.post(`${process.env.BACKEND_API_URL}/customers`, req.body);
    res.redirect('/customers');
  } catch (error) {
    console.error('Error adding customer:', error);
    res.redirect('/customers');
  }
});

app.post('/customers/:id/update', async (req, res) => {
  try {
    await axios.put(`${process.env.BACKEND_API_URL}/customers/${req.params.id}`, req.body);
    res.redirect('/customers');
  } catch (error) {
    console.error('Error updating customer:', error);
    res.redirect('/customers');
  }
});

app.post('/customers/:id/delete', async (req, res) => {
  try {
    await axios.delete(`${process.env.BACKEND_API_URL}/customers/${req.params.id}`);
    res.redirect('/customers');
  } catch (error) {
    console.error('Error deleting customer:', error);
    res.redirect('/customers');
  }
});

// Borrowing routes
app.get('/borrowings', async (req, res) => {
  try {
    const borrowingsResponse = await axios.get(`${process.env.BACKEND_API_URL}/borrowings`);
    const booksResponse = await axios.get(`${process.env.BACKEND_API_URL}/books`);
    const customersResponse = await axios.get(`${process.env.BACKEND_API_URL}/customers`);
    
    // Filter available books (status = 'available')
    const availableBooks = booksResponse.data.filter(book => book.status === 'available');
    
    // Filter eligible customers (those not currently borrowing a book)
    const borrowedCustomerIds = borrowingsResponse.data
      .filter(record => !record.returndate)
      .map(record => record.customerid);
    
    const eligibleCustomers = customersResponse.data.filter(
      customer => !borrowedCustomerIds.includes(customer.id)
    );
    
    res.render('borrowings', {
      borrowings: borrowingsResponse.data,
      availableBooks,
      eligibleCustomers
    });
  } catch (error) {
    console.error('Error fetching borrowing data:', error);
    res.render('borrowings', { 
      borrowings: [], 
      availableBooks: [], 
      eligibleCustomers: [], 
      error: 'Failed to fetch data' 
    });
  }
});

app.post('/borrowings', async (req, res) => {
  try {
    await axios.post(`${process.env.BACKEND_API_URL}/borrowings`, req.body);
    res.redirect('/borrowings');
  } catch (error) {
    console.error('Error creating borrowing record:', error);
    res.redirect('/borrowings');
  }
});

app.post('/borrowings/:id/return', async (req, res) => {
  try {
    await axios.put(`${process.env.BACKEND_API_URL}/borrowings/${req.params.id}/return`, {
      returndate: req.body.returndate
    });
    res.redirect('/borrowings');
  } catch (error) {
    console.error('Error returning book:', error);
    res.redirect('/borrowings');
  }
});