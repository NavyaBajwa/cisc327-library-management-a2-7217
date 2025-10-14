"""
Library Service Module - Business Logic Functions
Contains all the core business logic for the Library Management System
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import (
    get_book_by_id, get_book_by_isbn, get_patron_borrow_count,
    insert_book, insert_borrow_record, update_book_availability,
    update_borrow_record_return_date, get_all_books, get_patron_borrowed_books, get_book_by_title, get_book_by_author,
    get_patron_borrowing_history
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
    if not isbn.isdigit():
        return False, "ISBN is not numeric, should be numeric."
    
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
    
    return True, f'Successfully borrowed "{book["title"]}". Due date: {due_date.strftime("%Y-%m-%d")}. Book id: {book_id}'

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
    
    borrowedBooks = get_patron_borrowed_books(patron_id)
    bookToReturn = None
    for book in borrowedBooks:
        if book["book_id"] == book_id:
            bookToReturn = book
            break
    if not bookToReturn:
        return False, "This book is not currently borrowed by the patron."
    
    returnDate = datetime.now()
    dateSuccess = update_borrow_record_return_date(patron_id, book_id, returnDate)
    if not dateSuccess:
        return False, "Database error occurred while updating the return record."
    
    availability_success = update_book_availability(book_id, +1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."
    
    feeInfo = calculate_late_fee_for_book(patron_id, book_id)
    feeAmount = feeInfo.get("fee_amount")
    daysOverdue = feeInfo.get("days_overdue")

    if daysOverdue > 0:
        message = (
            f'The book, "{bookToReturn["title"]}" was returned successfully. '
            f'{daysOverdue} days overdue. Late fee: ${feeAmount:.2f}.'
        )
    else:
        message = (
            f'The book, "{bookToReturn["title"]}" was returned successfully. There are no late fees.'
        )

    return True, message

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
    borrowedBooks = get_patron_borrowed_books(patron_id)

    bookToReturn = None
    for book in borrowedBooks:
        if book["book_id"] == book_id:
            bookToReturn = book
            break
    if not bookToReturn:
        return {
            'fee_amount': 0.00,
            'days_overdue': 0,
            'status': "This book is not currently borrowed by the patron."
        }
    
    returnDate = datetime.now()
    
    dueDate = bookToReturn["due_date"]
    feeAmount = 0.00
    daysOverdue = 0
    
    if not bookToReturn["is_overdue"]:
        return {
            'fee_amount': feeAmount,
            'days_overdue': daysOverdue,
            'status': "No late fee: returned on time."
        }
   
    daysOverdue = (returnDate - dueDate).days
    if daysOverdue <= 7:
        feeAmount = daysOverdue * 0.50
    else:
        feeAmount = (7 * 0.50) + ((daysOverdue - 7) * 1.00)
        if feeAmount > 15:
            feeAmount = 15
    
    return {
            'fee_amount': feeAmount,
            'days_overdue': daysOverdue,
            'status': f"{daysOverdue} days overdue"
        }


def search_books_in_catalog(search_term: str, search_type: str) -> List[Dict]:
    """
    Search for books in the catalog.
    
    TODO: Implement R6 as per requirements
    """
    search_term = search_term.strip()

    if not search_term: 
        return []

    if search_type == "title" and len(search_term) > 200:
        return []
    
    if search_type == "author" and len(search_term) > 100:
        return []
    
    if search_type == "isbn" and len(search_term) != 13:
        return []
    
    results = []
    if search_type == "title":
        results = get_book_by_title(search_term)
    elif search_type == "author":
        results = get_book_by_author(search_term)
    elif search_type == "isbn":
        book = get_book_by_isbn(search_term)
        if book:
            results = [book]
    else:
        return []
    
    return results

def get_patron_status_report(patron_id: str) -> Dict:
    """
    Get status report for a patron.
    
    TODO: Implement R7 as per requirements
    """
    currentBooks = get_patron_borrowed_books(patron_id)
    borrowingHistory = get_patron_borrowing_history(patron_id)
    currentBorrowCount = get_patron_borrow_count(patron_id)

    totalFees = 0.0
    for book in currentBooks:
        if book["is_overdue"]:
            feeInfo = calculate_late_fee_for_book(patron_id, book["book_id"])
            totalFees += feeInfo["fee_amount"]

    patronReport = {
        "totalLateFees": totalFees,
        "currentBorrowCount": currentBorrowCount,
        "borrowingHistory": borrowingHistory,
        "currentBooks": currentBooks
    }

    return patronReport
