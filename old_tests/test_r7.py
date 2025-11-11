import pytest
from services.library_service import (
    get_patron_status_report
)

# Assume 123456 is a exists in data base as a patron

def test__has_required_feilds():
    """The report should have borrowed books, late fees owed,
    num books currently borrowed and and borrowing history"""
    report = get_patron_status_report("123456")
    assert "currently borrowed" in report
    assert "late fees" in report
    assert "borrow " in report
    assert "history" in report


def test_late_fees_non_negative():
    """Late fees cant be a negative number"""
    report = get_patron_status_report("123456")
    fees = report.get("total_late_fees")
    assert fees >= 0
    
def test_borrowed_items_have_due_date():
    """The borrowed books should have due dayes"""
    report = get_patron_status_report("123456")
    borrowed = report.get("currently_borrowed", [])
    for item in borrowed:
        assert "due date" in item
        
def test_borrow_count_matches_current_borrows_length():
    """borrow_count shouuld equal the legnth of current borrows list"""
    report = get_patron_status_report("123456")
    current_borrow_list = report.get("currently_borrowed", [])
    books_borrowed = report.get("borrow_count")
    assert books_borrowed == len(current_borrow_list)