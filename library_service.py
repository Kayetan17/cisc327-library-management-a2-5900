"""
Library Service Module - Business Logic Functions
Contains all the core business logic for the Library Management System
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import (
    get_book_by_id, get_book_by_isbn, get_patron_borrow_count,
    insert_book, insert_borrow_record, update_book_availability,
    update_borrow_record_return_date, get_all_books, get_patron_borrowed_books
)

def add_book_to_catalog(title: str, author: str, isbn: str, total_copies: int) -> Tuple[bool, str]:
    """
    Add a new book to the catalog.
    Implements R1: Book Catalog Management
    
    Args:
        title: Book title (max 200 chars)
        author: Book author (max 100 chars)
        isbn: 13-digit ISBN
        total_copies: Number of copies (positive integer)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Input validation
    if not title or not title.strip():
        return False, "Title is required."
    
    if len(title.strip()) > 200:
        return False, "Title must be less than 200 characters."
    
    if not author or not author.strip():
        return False, "Author is required."
    
    if len(author.strip()) > 100:
        return False, "Author must be less than 100 characters."
    
    if len(isbn) != 13:
        return False, "ISBN must be exactly 13 digits."
    
    if not isinstance(total_copies, int) or total_copies <= 0:
        return False, "Total copies must be a positive integer."
    
    # Check for duplicate ISBN
    existing = get_book_by_isbn(isbn)
    if existing:
        return False, "A book with this ISBN already exists."
    
    # Insert new book
    success = insert_book(title.strip(), author.strip(), isbn, total_copies, total_copies)
    if success:
        return True, f'Book "{title.strip()}" has been successfully added to the catalog.'
    else:
        return False, "Database error occurred while adding the book."

def borrow_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Allow a patron to borrow a book.
    Implements R3 as per requirements  
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists and is available
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    if book['available_copies'] <= 0:
        return False, "This book is currently not available."
    
    # Check patron's current borrowed books count
    current_borrowed = get_patron_borrow_count(patron_id)
    
    if current_borrowed > 5:
        return False, "You have reached the maximum borrowing limit of 5 books."
    
    # Create borrow record
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)
    
    # Insert borrow record and update availability
    borrow_success = insert_borrow_record(patron_id, book_id, borrow_date, due_date)
    if not borrow_success:
        return False, "Database error occurred while creating borrow record."
    
    availability_success = update_book_availability(book_id, -1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."
    
    return True, f'Successfully borrowed "{book["title"]}". Due date: {due_date.strftime("%Y-%m-%d")}.'

def return_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Process book return by a patron.
    
    TODO: Implement R4 as per requirements
    """
    
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    

    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    if book['available_copies'] <= 0:
        return False, "This book is currently not available."
    
    patrons_borrows = get_patron_borrowed_books(patron_id)
    has_borrows = False

    for i in patrons_borrows:
        if i.get("book_id") == book_id:
            has_borrows = True
            due_date = i.get("due_date")
            break

    if not has_borrows:
        return False, "Patron has no books borrowed."
    
    fee_info = calculate_late_fee_for_book(patron_id, book_id)
    fee_amount = fee_info.get("fee_amount", 0.0)
    days_overdue = fee_info.get("days_overdue", 0)
    
    
    time = datetime.now()
    update_return = update_borrow_record_return_date(patron_id, book_id, time)
    if not update_return:
        return False, "Database error while updating the return."
    
    updated_available_books = update_book_availability(book_id, +1)
    if not updated_available_books:
        return False, "Database error while updating book availability."
    
    title = book.get("title", "the book")
    if fee_amount > 0:
        return True, "Returned " + title + ". Overdue by " + str(days_overdue) + " day(s). Late fee: $" + str(fee_amount) +"'."
    else:
        return True, 'Returned "' + title + '" on time. No late fee.'
    
    

def calculate_late_fee_for_book(patron_id: str, book_id: int) -> Dict:
    """
    Calculate late fees for a specific book.
    
    TODO: Implement R5 as per requirements 
    
    
    return { // return the calculated values
        'fee_amount': 0.00,
        'days_overdue': 0,
        'status': 'Late fee calculation not implemented'
    }
    """
    
    patrons_borrows = get_patron_borrowed_books(patron_id)
    record = None
    for i in patrons_borrows:
        if i.get('book_id') == book_id:
            record = i
            break

    if record is None:
        return {'fee_amount': 0.00, 'days_overdue': 0}

    time = datetime.now()
    due_date = record.get('due_date')  
    days_overdue = (time.date() - due_date.date()).days
    
    if days_overdue < 0:
        days_overdue = 0

    total_fee = 0.0
    if days_overdue > 0:
        first7 = days_overdue
        if first7 > 7:
            first7 = 7
        first_fee = first7 * 0.50

        after7 = days_overdue - 7
        if after7 < 0:
            after7 = 0
        after_fee = after7 * 1.00

        total_fee = first_fee + after_fee

        if total_fee > 15.00:
            total_fee = 15.00

    total_fee = round(total_fee, 2)

    return {'fee_amount': total_fee, 'days_overdue': days_overdue}
    

def search_books_in_catalog(search_term: str, search_type: str) -> List[Dict]:
    """
    Search for books in the catalog.
    
    TODO: Implement R6 as per requirements
    """
    
    if search_term is None:
        return []
    if search_type is None:
        return []
    
    q = search_term.strip()
    if q == "":
        return []

    books = get_all_books()
    results: List[Dict] = []

    q_lowercase = q.lower()

    type = search_type.strip().lower()
    if type not in ["title", "author", "isbn"]:
        return []
    
    for book in books:
        title = book.get("title", "")
        author = book.get("author", "")
        isbn = book.get("isbn", "")

        if type == "title":
            if q_lowercase in title.lower():
                results.append(book)

        elif type == "author":
            if q_lowercase in author.lower():
                results.append(book)

        elif type == "isbn":
            if q == isbn:
                results.append(book)

    return results
    

def get_patron_status_report(patron_id: str) -> Dict:
    """
    Get status report for a patron.
    
    TODO: Implement R7 as per requirements
    """
    
    books_borrowed = get_patron_borrowed_books(patron_id)  
    num_borrowed = get_patron_borrow_count(patron_id)
    
    
    total_fees = 0.0
    current_book_info = []

    for book in books_borrowed:
        fee_info = calculate_late_fee_for_book(patron_id, book.get('book_id'))
        fee_amount = fee_info.get('fee_amount', 0.0)

        total_fees = total_fees + fee_amount

        borrow_date = book.get('borrow_date')
        due_date = book.get('due_date')

        borrow_date_string_format = ""
        due_date_string_format = ""
        if borrow_date is not None:
            borrow_date_string_format = borrow_date.isoformat()
        if due_date is not None:
            due_date_string_format = due_date.isoformat()


        current_book_info.append({
            'book_id': book.get('book_id'),
            'title': book.get('title'),
            'author': book.get('author'),
            'borrow_date': borrow_date_string_format,
            'due_date': due_date_string_format,
            'is_overdue': book.get('is_overdue', False),
            'late_fee': round(fee_amount, 2)
        })

    total_fees = round(total_fees, 2)
    
    # Im not sure how i would get the borrowing history as required by R7, so R7 is only partialy complete
    # Theres no function in the database to access the borrowing history
    
    report = {
        'patron_id': patron_id,
        'number_borrowed': num_borrowed,
        'currently_borrowed': current_book_info,
        'total_late_fees_owed': total_fees
    }
    return report
    
    