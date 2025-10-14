import pytest
from library_service import (
    add_book_to_catalog
)

def test_author_required():
    """Empty author shouldnt work"""
    success, message = add_book_to_catalog("Title", "", "1234567890123", 1)
    assert success == False
    assert "author" in message.lower()
    

def test_add_book_invalid_ISBN():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    
    assert success == False
    assert "13 digits" in message
    

def test_author_max_length():
    """Testing author name being to long"""
    bad_author_name = "A" * 101  
    success, message = add_book_to_catalog("Title", bad_author_name, "1234567890123", 1)
    assert success == False
    assert "100" in message

def test_total_copies_0():
    """Testing total copies being 0 Should fail"""
    success, message = add_book_to_catalog("Title", "Author", "1234567890123", 0)
    assert success == False
    assert "positive" in message.lower()
