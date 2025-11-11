import pytest
from services.library_service import (
    calculate_late_fee_for_book
)
import database

# I cant figure out how i would set the database to be a certain ammount overdue for each unit tests
# So assume that its already set for the book ID and Patron

def test_fee_3_days_overdue():
    """3 days overdue, fee should be 1.50"""
    result = calculate_late_fee_for_book("123456", 1)
    assert result["days_overdue"] == 3
    assert result["fee_amount"] == 1.50
    
def test_fee_10_days_overdue():
    """10 days overdue fee should be 6.50"""
    result = calculate_late_fee_for_book("123456", 2)
    assert result["days_overdue"] == 10
    assert result["fee_amount"] == 6.50
    
def test_fee_100_days_overdue():
    """100 days overdue fee should be capped at a 15$ fee"""
    result = calculate_late_fee_for_book("123456", 3)
    assert result["days_overdue"] == 100
    assert result["fee_amount"] == 15
    
def test_not_overdue():
    """0 days over due, fee should be 0"""
    result = calculate_late_fee_for_book("123456", 4)
    assert result["days_overdue"] == 0
    assert result["fee_amount"] == 0
