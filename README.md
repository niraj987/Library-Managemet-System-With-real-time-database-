# Library Management System  
**Console-Based Library Management in Python**

A straightforward, educational **Library Management System** built in pure Python using **pandas** for data storage (CSV files).  
It supports two types of users:

- **Members** → register, login, browse, borrow, return books, see their borrowings and fines  
- **Admin** → manage book catalog, view all borrow history, see registered users

Designed as a clean, beginner-to-intermediate level project demonstrating:

- CRUD operations with pandas  
- File-based persistence (no database required)  
- Date & time handling for due dates & fines  
- Basic role-based access (member vs admin)  
- Clean console UI with formatted output (slips, tables)

Perfect for college mini-projects, Python learning, file I/O practice, or first portfolio console application.

## Main Features

### Member (User) Capabilities
- Register new account (user_id, name, phone, email, password)
- Login with credentials
- View complete list of available books
- Search books by title (partial match supported)
- Borrow a book (choose duration 1–14 days)
- Return a book → automatic late fine calculation (₹5 per day)
- View currently borrowed books with due dates
- Nicely formatted return slip showing borrow/return dates, days late & fine

### Administrator Capabilities
- Special admin login (default: admin / lib123admin)
- View **all active & returned borrowings** (user-wise, with status & fines)
- See list of all registered members
- Add new books to the catalog
- Increase stock quantity of existing books

### Data Storage (all automatic)
Three CSV files are created/used in the project folder:

- `library_users.csv`     → user accounts  
- `library_books.csv`      → book catalog (title, author, price, quantity, department)  
- `borrow_records.csv`     → borrowing history (user, book, dates, returned flag, fine)

## Tech Stack

- Python 3.8+
- pandas (data frames & CSV read/write)
- datetime + timedelta (due date & fine logic)
- os (file existence checks & screen clear)

No external database, web framework or GUI — pure console application.

Default Admin Login
User ID: admin
Password: lib123admin

🎯 Sample Usage Flow

Register as a new member
Login → browse books → borrow a book
Login as admin → add more books or check who has what
Return book (after due date) → see fine calculation & nice return slip


 
