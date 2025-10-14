import pytest
from library_service import (
    search_books_in_catalog
)
import database

# Assume data base already has books in it and i dont manualy have to add it in


def test_invalid_search():
    """invalid search type should return an empty list of books."""
    results = search_books_in_catalog("invalid", "invalid")
    assert results == []
    

def test_title_partial_search_by_title():
    books = database.get_all_books()
    b = books[0]
    title = b.get("title")
    partial = title[:3]
    results = search_books_in_catalog(partial, "title")
    found = False
    for i in results:
        if i.get("id") == b["id"]:
            found = True
            break

    assert found
    
def test_author_partial_search_by_author():
    books = database.get_all_books()
    b = books[0]
    author = b.get("author")
    partial = author[:3] 
    results = search_books_in_catalog(partial, "author")
    found = False
    for i in results:
        if i.get("id") == b["id"]:
            found = True
            break

    assert found
    
def test_isbn_exact_match():
    books = database.get_all_books()
    b = books[0]
    isbn = b.get("isbn")
    results = search_books_in_catalog(isbn, "isbn")
    found = False
    for i in results:
        if i.get("isbn") == isbn:
            found = True
            break

    assert found