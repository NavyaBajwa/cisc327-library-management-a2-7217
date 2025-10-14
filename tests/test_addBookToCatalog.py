import pytest
from library_service import (
    add_book_to_catalog
)

from database import init_database, reset_database, add_sample_data

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    init_database()
    reset_database()
    add_sample_data()

def test_add_book_valid_input():
    """Test adding a book with valid input."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1111111111111", 5)
    
    assert success == True
    assert "successfully added" in message.lower()

def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "222222222", 5)
    
    assert success == False
    assert "13 digits" in message.lower()

# Add more test methods for each function and edge case. You can keep all your test in a separate folder named `tests`.
"""My tests"""

def test_add_book_invalid_title_too_short():
    """Test adding a book with title is too short."""
    success, message = add_book_to_catalog("", "Navya", "3333333333333", 3)

    assert success == False
    #assert "Title too short, should be more than 0 less than 200 chars" in message
    assert "title is required" in message.lower()

def test_add_book_invalid_title_too_long():
    """Test adding a book with title is too long."""
    """Title has 208 characters"""
    success, message = add_book_to_catalog("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq" \
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq" \
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq", "Test Author", "4444444444444", 3)

    assert success == False
    #assert "Title too long, should be less than 200 chars" in message
    assert "less than 200 characters" in message.lower()

def test_add_book_invalid_author_too_long():
    """Test adding a book with title is too long."""
    """Author has 208 characters"""

    success, message = add_book_to_catalog("Percy Jackson", "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq" \
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq" \
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq", "5555555555555", 3)

    assert success == False
    #assert "Author too long, should be less than 100" in message
    assert "less than 100 characters" in message.lower()

def test_add_book_invalid_author_too_short():
    """Test adding a book with author too short."""

    success, message = add_book_to_catalog("Harry Potter", "", "6666666666666", 3)

    assert success == False
    #assert "Author too short, should be between 0 and 100 chars" in message
    assert "author is required" in message.lower()

def test_add_book_invalid_isbn_too_long():
    """Test adding a book with isbn too long."""

    success, message = add_book_to_catalog("Schoolbox", "Rick Riordan", "777777777777777", 3)

    assert success == False
    assert "exactly 13 digits" in message.lower()

def test_add_book_invalid_isbn_not_digits():
    """Test adding a book with isbn too long."""

    success, message = add_book_to_catalog("Lunch Meat", "Earnest Hemingway", "888abcdefghij", 4)

    assert success == False
    assert "isbn is not numeric, should be numeric" in message.lower()

def test_add_book_invalid_total_copies_negative():
    """Test adding a book with total copies is negative int."""

    success, message = add_book_to_catalog("Jump Rope", "Brick", "9999999999999", -3)

    assert success == False
    assert "positive integer" in message.lower()

def test_add_book_invalid_total_copies_null():
    """Test adding a book with total copies is 0"""

    success, message = add_book_to_catalog("DumbBum", "HumBum", "1010101010101", 0)

    assert success == False
    assert "positive integer" in message.lower()

def test_add_book_valid_max_title_length():
    """Test adding a book with title length of 200 chars"""

    success, message = add_book_to_catalog("a"*200, "West", "1212121212121", 2)

    assert success == True
    assert "successfully added" in message.lower()

def test_add_book_valid_max_author_length():
    """Test adding a book with author length of 100 chars"""

    success, message = add_book_to_catalog("Best", "b"*100, "1313131313131", 2)

    assert success == True
    assert "successfully added" in message.lower()

def test_add_book_valid_min_total_copies():
    """Test adding a book with 1 total copy"""

    success, message = add_book_to_catalog(" Title", "Writer", "1414141414141", 1)

    assert success == True
    assert "successfully added" in message.lower()