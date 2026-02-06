import pandas as pd
from datetime import datetime, timedelta
import os

# -------------------------------
# FILE PATHS
# -------------------------------
USERS_CSV   = "library_users.csv"
BOOKS_CSV   = "library_books.csv"
BORROW_CSV  = "borrow_records.csv"

# Simple admin credentials (in production → use .env + hashing!)
ADMIN_ID       = "admin"
ADMIN_PASSWORD = "lib123admin"

# -------------------------------
# Initialize CSV files
# -------------------------------
def initialize_files():
    if not os.path.exists(USERS_CSV):
        pd.DataFrame(columns=["user_id", "name", "phone", "email", "password"]).to_csv(USERS_CSV, index=False)

    if not os.path.exists(BOOKS_CSV):
        pd.DataFrame(columns=["title", "author", "price", "quantity", "department"]).to_csv(BOOKS_CSV, index=False)

    if not os.path.exists(BORROW_CSV):
        pd.DataFrame(columns=["user_id", "title", "borrow_date", "due_date", "returned", "fine"]).to_csv(BORROW_CSV, index=False)

initialize_files()

# Load data (global)
users_df  = pd.read_csv(USERS_CSV)
books_df  = pd.read_csv(BOOKS_CSV)
borrow_df = pd.read_csv(BORROW_CSV)

# -------------------------------
# Helpers
# -------------------------------
def save_all_data():
    global users_df, books_df, borrow_df
    users_df.to_csv(USERS_CSV, index=False)
    books_df.to_csv(BOOKS_CSV, index=False)
    borrow_df.to_csv(BORROW_CSV, index=False)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# -------------------------------
# USER functions (unchanged mostly)
# -------------------------------
def register_user():
    global users_df
    print("\n--- Register New User ---")
    user_id = input("Enter unique User ID: ").strip()

    if user_id in users_df["user_id"].values:
        print("User ID already exists!")
        return None

    name     = input("Enter your full name: ").strip()
    phone    = input("Enter phone number: ").strip()
    email    = input("Enter email: ").strip()
    password = input("Enter password: ").strip()

    new_user = pd.DataFrame({
        "user_id": [user_id], "name": [name], "phone": [phone],
        "email": [email], "password": [password]
    })

    users_df = pd.concat([users_df, new_user], ignore_index=True)
    save_all_data()
    print("Registration successful!")
    return user_id

def login_user():
    global users_df
    print("\n--- Member Login ---")
    user_id  = input("User ID: ").strip()
    password = input("Password: ").strip()

    row = users_df[(users_df["user_id"] == user_id) & (users_df["password"] == password)]
    if row.empty:
        print("Invalid credentials.")
        return None

    print(f"Welcome, {row['name'].iloc[0]}!")
    return user_id

# -------------------------------
# ADMIN functions
# -------------------------------
def login_admin():
    print("\n--- Admin Login ---")
    admin_id = input("Admin ID: ").strip()
    password = input("Password: ").strip()

    if admin_id == ADMIN_ID and password == ADMIN_PASSWORD:
        print("Admin access granted.")
        return True
    else:
        print("Admin login failed.")
        return False

def admin_view_all_borrows():
    global borrow_df, users_df, books_df
    if borrow_df.empty:
        print("No borrow records yet.")
        return

    # Merge for better display
    merged = borrow_df.merge(users_df[["user_id", "name"]], on="user_id", how="left")
    print("\n" + "="*80)
    print("ALL BORROW RECORDS")
    print("="*80)
    print(merged[["user_id", "name", "title", "borrow_date", "due_date", "returned", "fine"]].to_string(index=False))
    print("="*80 + "\n")

def admin_view_all_users():
    global users_df
    if users_df.empty:
        print("No users registered yet.")
        return
    print("\nRegistered Users:")
    print(users_df[["user_id", "name", "phone", "email"]].to_string(index=False))
    print()

def admin_add_book():
    global books_df
    print("\n--- Add New Book ---")
    title      = input("Book Title: ").strip()
    author     = input("Author: ").strip()
    price      = float(input("Price (₹): ").strip() or 0)
    quantity   = int(input("Initial Quantity: ").strip() or 1)
    department = input("Department/Category (optional): ").strip()

    if title in books_df["title"].values:
        print("A book with this exact title already exists.")
        add_more = input("Add more copies instead? (y/n): ").lower().startswith('y')
        if add_more:
            books_df.loc[books_df["title"] == title, "quantity"] += quantity
            save_all_data()
            print(f"Added {quantity} more copies of '{title}'.")
            return
        else:
            return

    new_book = pd.DataFrame({
        "title": [title],
        "author": [author],
        "price": [price],
        "quantity": [quantity],
        "department": [department or "General"]
    })

    books_df = pd.concat([books_df, new_book], ignore_index=True)
    save_all_data()
    print(f"Book '{title}' added successfully!")

# -------------------------------
# Book functions (member side)
# -------------------------------
def show_all_books():
    if books_df.empty:
        print("No books available yet.")
        return
    print("\nLibrary Collection:")
    print(books_df[["title", "author", "price", "quantity", "department"]].to_string(index=False))

def search_book_by_title():
    title = input("Enter book title (partial ok): ").strip().lower()
    results = books_df[books_df["title"].str.lower().str.contains(title, na=False)]
    if results.empty:
        print("No matching books found.")
        return None
    print("\nFound:")
    print(results[["title", "author", "price", "quantity", "department"]].to_string(index=False))
    return results

def borrow_book(user_id):
    global books_df, borrow_df
    book_row = search_book_by_title()
    if book_row is None or book_row.empty:
        return

    if len(book_row) > 1:
        print("Multiple matches — please be more specific next time.")
        return

    chosen = book_row.iloc[0]
    title = chosen["title"]

    if chosen["quantity"] < 1:
        print("Out of stock.")
        return

    try:
        days = int(input("Borrow for how many days? (1–14): "))
        if not 1 <= days <= 14:
            print("Allowed range: 1 to 14 days.")
            return
    except:
        print("Invalid number.")
        return

    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=days)

    books_df.loc[books_df["title"] == title, "quantity"] -= 1

    new_record = pd.DataFrame({
        "user_id": [user_id],
        "title": [title],
        "borrow_date": [borrow_date.strftime("%Y-%m-%d %H:%M")],
        "due_date": [due_date.strftime("%Y-%m-%d %H:%M")],
        "returned": [False],
        "fine": [0.0]
    })

    borrow_df = pd.concat([borrow_df, new_record], ignore_index=True)
    save_all_data()

    print(f"\nBorrowed '{title}' successfully.")
    print(f"Due on: {due_date.strftime('%Y-%m-%d')}")

def return_book(user_id):
    global borrow_df, books_df, users_df

    active = borrow_df[(borrow_df["user_id"] == user_id) & (~borrow_df["returned"])]
    if active.empty:
        print("No books currently borrowed.")
        return

    print("\nYour borrowed books:")
    for i, row in active.iterrows():
        print(f"{i+1}. {row['title']}  Due: {row['due_date']}")

    try:
        idx = int(input("\nEnter number to return: ")) - 1
        selected = active.iloc[idx]
    except:
        print("Invalid selection.")
        return

    title = selected["title"]
    due_str = selected["due_date"]

    due = datetime.strptime(due_str, "%Y-%m-%d %H:%M")
    now = datetime.now()
    days_late = max(0, (now - due).days)
    fine = days_late * 5.0

    user_name = users_df.loc[users_df["user_id"] == user_id, "name"].iloc[0] if not users_df.empty else "Unknown"

    borrow_idx = borrow_df[(borrow_df["user_id"] == user_id) &
                           (borrow_df["title"] == title) &
                           (~borrow_df["returned"])].index[0]

    borrow_df.loc[borrow_idx, "returned"] = True
    borrow_df.loc[borrow_idx, "fine"] = fine
    books_df.loc[books_df["title"] == title, "quantity"] += 1

    save_all_data()

    # Return slip
    print("\n" + "="*60)
    print("         RETURN SLIP")
    print("="*60)
    print(f"Return Time : {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"User        : {user_id}  ({user_name})")
    print(f"Book        : {title}")
    print(f"Borrowed    : {selected['borrow_date']}")
    print(f"Due Date    : {due_str}")
    print(f"Days Late   : {days_late}")
    print(f"Fine        : ₹{fine:.2f}")
    print("-"*60)
    print("** Pay fine at counter if applicable **" if fine > 0 else "Returned on time — Thank you!")
    print("="*60 + "\n")

def show_my_books(user_id):
    active = borrow_df[(borrow_df["user_id"] == user_id) & (~borrow_df["returned"])]
    if active.empty:
        print("No active borrowings.")
        return
    print("\nYour Borrowed Books:")
    print(active[["title", "borrow_date", "due_date"]].to_string(index=False))

# -------------------------------
# MAIN MENU
# -------------------------------
def main():
    current_user = None
    is_admin = False

    while True:
        clear_screen()
    
        print("╔════════════════════════════════════╗")
        print("║     LIBRARY MANAGEMENT SYSTEM      ║")
        print("╚════════════════════════════════════╝")

        if current_user is None and not is_admin:
            print("1. Member Login")
            print("2. Register")
            print("3. Admin Login")
            print("0. Exit")
            ch = input("\nChoice: ").strip()

            if ch == "1":
                current_user = login_user()
                is_admin = False
            elif ch == "2":
                register_user()
            elif ch == "3":
                if login_admin():
                    is_admin = True
                    current_user = None
            elif ch == "0":
                print("\nThank you for using the Library. Goodbye!")
                break
            else:
                print("Invalid choice.")

        elif is_admin:
            print("ADMIN MODE")
            print("1. View all borrow records")
            print("2. View all users")
            print("3. Add new book")
            print("4. Logout")
            print("0. Exit program")
            ch = input("\nChoice: ").strip()

            if ch == "1": admin_view_all_borrows()
            elif ch == "2": admin_view_all_users()
            elif ch == "3": admin_add_book()
            elif ch == "4":
                is_admin = False
                print("Admin logged out.")
            elif ch == "0":
                print("Shutting down...")
                break

        else:  # normal member
            print(f"Logged in: {current_user}")
            print("1. View all books")
            print("2. Search & Borrow")
            print("3. Return book")
            print("4. My borrowed books")
            print("5. Logout")
            print("0. Exit")
            ch = input("\nChoice: ").strip()

            if   ch == "1": show_all_books()
            elif ch == "2": borrow_book(current_user)
            elif ch == "3": return_book(current_user)
            elif ch == "4": show_my_books(current_user)
            elif ch == "5":
                current_user = None
                print("Logged out.")
            elif ch == "0":
                print("Goodbye!")
                break

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    print("--- Welcome to the Library Management System ---")
    main()