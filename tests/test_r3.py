import pytest
from services.library_service import (
    borrow_book_by_patron
)

def test_patron_id_null():
    """No patron ID it shouldnt work."""
    success, message = borrow_book_by_patron("", 1)
    assert success == False
    assert "patron" in message.lower()
    
def test_patron_id_must_be_numbers():
    """Patron id with letters shouldnt work."""
    success, message = borrow_book_by_patron("12ab56", 1)
    assert success == False
    assert "patron" in message.lower()
    
def test_patron_id_too_short():
    """Patron ID shorter than 6 shouldnt work."""
    success, message = borrow_book_by_patron("12345", 1) 
    assert success == False
    assert "patron" in message.lower()
    
def test_patron_id_too_long():
    """Patron ID longer than 6 shouldnt work"""
    success, message = borrow_book_by_patron("12342222222567", 1) 
    assert success == False
    assert "patron" in message.lower()

def test_book_not_found():
    """Testing looking for a non existent book, should fail'"""
    # Assume 9999999 is not a book
    success, message = borrow_book_by_patron("123456", 9999999)
    assert success == False
    assert "book" in message.lower()


