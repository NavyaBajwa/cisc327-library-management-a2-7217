import pytest
from library_service import (
    calculate_late_fee_for_book
)

def test_book_not_overdue():
    """Test late fee for a book that is not overdue."""
    resultDict = calculate_late_fee_for_book("123456", 1)
    
    assert resultDict["days_overdue"] == 0
    assert resultDict["late_fee"] == 0.00

def test_book_one_day_overdue():
    """Test late fee for a book that is one day overdue."""
    resultDict = calculate_late_fee_for_book("234567", 2)
    
    assert resultDict["days_overdue"] == 1
    assert resultDict["late_fee"] == 0.50

def test_book_seven_days_overdue():
    """Test late fee for a book that is seven days overdue."""
    resultDict = calculate_late_fee_for_book("444444", 3)
    
    assert resultDict["days_overdue"] == 7
    assert resultDict["late_fee"] == 3.50

def test_book_nine_days_overdue():
    """Test late fee for a book that is nine days overdue."""
    resultDict = calculate_late_fee_for_book("654219", 4)
    
    assert resultDict["days_overdue"] == 9
    # fee = (0.5 * 7) + (1.00 * 2) = $5.5
    assert resultDict["late_fee"] == 5.50

def test_fee_max_15():
    """Test late fee for a book that is nine days overdue."""
    resultDict = calculate_late_fee_for_book("654266", 5)
    # if the book is more than 11 days overdue, the fee owed will be $15
    assert resultDict["days_overdue"] >= 12
    assert resultDict["late_fee"] == 15