// main.js - Client-side JavaScript for the Library Management System

document.addEventListener('DOMContentLoaded', function() {
    // Format dates in tables
    const formatDates = () => {
      const dateCells = document.querySelectorAll('td:nth-child(3), td:nth-child(4)');
      dateCells.forEach(cell => {
        const text = cell.textContent.trim();
        if (text !== 'Not returned' && text !== '-' && text !== '') {
          try {
            const date = new Date(text);
            if (!isNaN(date.getTime())) {
              cell.textContent = new Intl.DateTimeFormat('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
              }).format(date);
            }
          } catch (e) {
            // Keep original text if date parsing fails
          }
        }
      });
    };
  
    // Add highlighting for late returns
    const highlightLateReturns = () => {
      const today = new Date();
      const borrowings = document.querySelectorAll('.active');
      
      borrowings.forEach(row => {
        const borrowDateCell = row.querySelector('td:nth-child(3)');
        if (borrowDateCell) {
          try {
            const borrowDate = new Date(borrowDateCell.textContent);
            const daysOut = Math.floor((today - borrowDate) / (1000 * 60 * 60 * 24));
            
            if (daysOut > 10) {
              row.classList.add('overdue');
              row.setAttribute('title', `Overdue by ${daysOut - 10} days`);
              
              // Add overdue indicator if not present
              const actionsCell = row.querySelector('td:last-child');
              if (actionsCell && !actionsCell.querySelector('.overdue-indicator')) {
                const overdueSpan = document.createElement('span');
                overdueSpan.className = 'overdue-indicator';
                overdueSpan.textContent = `Overdue: $${daysOut - 10}.00 fee`;
                actionsCell.prepend(overdueSpan);
              }
            }
          } catch (e) {
            // Skip if date parsing fails
          }
        }
      });
    };
  
    // Validate book borrowing form
    const validateBorrowingForm = () => {
      const borrowingForm = document.querySelector('form[action="/borrowings"]');
      if (borrowingForm) {
        borrowingForm.addEventListener('submit', function(e) {
          const bookSelect = document.getElementById('bookid');
          const customerSelect = document.getElementById('customerid');
          
          if (!bookSelect.value || !customerSelect.value) {
            e.preventDefault();
            alert('Please select both a book and a customer');
          }
        });
      }
    };
  
    // Validate customer form
    const validateCustomerForm = () => {
      const customerForm = document.querySelector('form[action="/customers"]');
      if (customerForm) {
        customerForm.addEventListener('submit', function(e) {
          const email = document.getElementById('email').value;
          const password = document.getElementById('password').value;
          
          // Simple email validation
          const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailPattern.test(email)) {
            e.preventDefault();
            alert('Please enter a valid email address');
            return;
          }
          
          // Password validation (minimum 6 characters)
          if (password.length < 6) {
            e.preventDefault();
            alert('Password must be at least 6 characters long');
          }
        });
      }
    };
  
    // Initialize functions if on relevant pages
    if (window.location.pathname.includes('borrowings')) {
      formatDates();
      highlightLateReturns();
      validateBorrowingForm();
    } else if (window.location.pathname.includes('customers')) {
      validateCustomerForm();
    }
  
    // Add CSS class for overdue books
    const style = document.createElement('style');
    style.textContent = `
      .overdue {
        background-color: #ffebee !important;
      }
      .overdue-indicator {
        display: block;
        font-size: 0.8rem;
        color: #e74c3c;
        margin-bottom: 0.5rem;
        font-weight: bold;
      }
    `;
    document.head.appendChild(style);
  });