import pytest
from library_service import (
    return_book_by_patron
)

def test_aaccepts_patron_and_book():
    """Accept patron ID and book ID as parameters."""
    success, message = return_book_by_patron("123456", 1)
    assert success == True
    assert "return" in message.lower()
    

def test_rejects_empty_patron_id():
    """Empty patron ID shouldnt work."""
    success, message = return_book_by_patron("", 1)
    assert success == False
    assert "patron" in message.lower()
    
def test_rejects_when_not_borrowed_by_patron():
    """Should fail if patron didnt borrow book 999999."""
    success, message = return_book_by_patron("123456", 999999)
    assert success == False
    assert "not borrowed" in message.lower()
    
def test_displays_late_fees():
    """If the book is returned late, there should be late fee info"""
    success, message = return_book_by_patron("123456", 3)
    assert success == True
    assert "fee" in message.lower()