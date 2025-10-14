import pytest
from library_service import (
    get_patron_status_report, get_patron_borrowed_books, get_patron_borrow_count, calculate_late_fee_for_book, get_patron_borrowing_history
)

def test_report_structure():
    report = get_patron_status_report("875324")
    
    assert "currentBooks" in report
    assert "totalLateFees" in report
    assert "currentBorrowCount" in report
    assert "borrowingHistory" in report


def test_currently_borrowed_books():
    """Test adding a book with valid input."""
    report = get_patron_status_report("123456")
    expected = get_patron_borrowed_books("123456")

    assert report["currentBooks"] == expected
    
def test_number_of_borrowed_books():
    """Test adding a book with valid input."""
    report = get_patron_status_report("456321")
    expected = get_patron_borrow_count("456321")

    assert report["currentBorrowCount"] == expected

def test_total_fees_owed():
    report = get_patron_status_report("897543")

    expectedFees = 0
    for book in report["currentBooks"]:
        bookId = book["book_id"]
        fee = calculate_late_fee_for_book("897543", bookId)
        expectedFees += fee["fee_amount"]
    
    assert report["totalLateFees"] == expectedFees

def test_patron_has_not_borrowed():
    report = get_patron_status_report("999999")
    assert report["currentBooks"] == []
    assert report["totalLateFees"] == 0.00
    assert report["currentBorrowCount"] == 0
    assert report["borrowingHistory"] == []

