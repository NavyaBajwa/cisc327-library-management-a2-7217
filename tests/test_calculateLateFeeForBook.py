import pytest
#from library_service import (
#    calculate_late_fee_for_book
#)

import library_service as ls
import datetime

def test_book_not_overdue(monkeypatch):
    """Test late fee for a book that is not overdue."""
    fake_books = [{
        "book_id": 1,
        "title": "Book A",
        "author": "Author A",
        "borrow_date": datetime.datetime.now() - datetime.timedelta(days=3),
        "due_date": datetime.datetime.now() - datetime.timedelta(days=14),
        "is_overdue": False
    }]
    monkeypatch.setattr(ls, "get_patron_borrowed_books", lambda patron_id :fake_books)
    resultDict = ls.calculate_late_fee_for_book("123456", 1)
    
    assert resultDict["days_overdue"] == 0
    assert resultDict["fee_amount"] == 0.00


def test_book_one_day_overdue(monkeypatch):
    """Test late fee for a book that is one day overdue."""
    fake_books = [{
        "book_id": 2,
        "title": "Book B",
        "author": "Author B",
        "borrow_date": datetime.datetime.now() - datetime.timedelta(days=15),
        "due_date": datetime.datetime.now() + datetime.timedelta(days=-1),
        "is_overdue": True
    }]
    monkeypatch.setattr(ls, "get_patron_borrowed_books", lambda patron_id :fake_books)    
    resultDict = ls.calculate_late_fee_for_book("234567", 2)
    
    assert resultDict["days_overdue"] == 1
    assert resultDict["fee_amount"] == 0.50


def test_book_seven_days_overdue(monkeypatch):
    """Test late fee for a book that is seven days overdue."""
    fake_books = [{
        "book_id": 3,
        "title": "Book C",
        "author": "Author C",
        "borrow_date": datetime.datetime.now() - datetime.timedelta(days=14),
        "due_date": datetime.datetime.now() + datetime.timedelta(days=-7),
        "is_overdue": True
    }]
    monkeypatch.setattr(ls, "get_patron_borrowed_books", lambda patron_id :fake_books) 
    resultDict = ls.calculate_late_fee_for_book("444444", 3)
    
    assert resultDict["days_overdue"] == 7
    assert resultDict["fee_amount"] == 3.50


def test_book_nine_days_overdue(monkeypatch):
    """Test late fee for a book that is nine days overdue."""
    fake_books = [{
        "book_id": 4,
        "title": "Book D",
        "author": "Author D",
        "borrow_date": datetime.datetime.now() - datetime.timedelta(days=14),
        "due_date": datetime.datetime.now() + datetime.timedelta(days=-9),
        "is_overdue": True
    }]
    monkeypatch.setattr(ls, "get_patron_borrowed_books", lambda patron_id :fake_books) 
    resultDict = ls.calculate_late_fee_for_book("654219", 4)
    
    assert resultDict["days_overdue"] == 9
    # fee = (0.5 * 7) + (1.00 * 2) = $5.5
    assert resultDict["fee_amount"] == 5.50


def test_fee_max_15(monkeypatch):
    """Test late fee for a book that is 20 days overdue."""
    fake_books = [{
        "book_id": 5,
        "title": "Book E",
        "author": "Author E",
        "borrow_date": datetime.datetime.now() - datetime.timedelta(days=40),
        "due_date": datetime.datetime.now() + datetime.timedelta(days=-20),
        "is_overdue": True
    }]
    monkeypatch.setattr(ls, "get_patron_borrowed_books", lambda patron_id :fake_books) 
    resultDict = ls.calculate_late_fee_for_book("654266", 5)

    # if the book is more than 17 days overdue, the fee owed will be $15
    assert resultDict["days_overdue"] >= 12
    assert resultDict["fee_amount"] == 15
