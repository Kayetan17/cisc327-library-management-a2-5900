import pytest
from services.payment_service import PaymentGateway
from services import library_service as libary


def test_payementgayeway_process_success():
    ok, txn, x = PaymentGateway().process_payment("123456", 15, "test")
    assert ok is True
    
def test_paymentgateway_process_invalid_patron():
    ok, x, msg = PaymentGateway().process_payment("12345", 15, "Test")
    assert ok is False and "Invalid patron ID" in msg
    
def test_paymentgateway_process_amount_is_zero():
    ok, x, msg = PaymentGateway().process_payment("123456", 0.0, "Test")
    assert ok is False and "Invalid amount" in msg

def test_payementgateway_refund_success():
    ok, msg = PaymentGateway().refund_payment("txn_123456", 15)
    assert ok is True and "Refund of $15" in msg

def test_borrow_not_available(mocker):
    mocker.patch("services.library_service.get_book_by_id", return_value={"available_copies": 0, "title": "Test"})
    ok, x = libary.borrow_book_by_patron("123456", 1)
    assert ok is False
    
def test_borrow_success(mocker):
    mocker.patch("services.library_service.get_book_by_id", return_value={"available_copies": 1, "title": "Test"})
    mocker.patch("services.library_service.get_patron_borrow_count", return_value=1)
    mocker.patch("services.library_service.insert_borrow_record", return_value=True)
    mocker.patch("services.library_service.update_book_availability", return_value=True)
    ok, x = libary.borrow_book_by_patron("123456", 1)
    assert ok is True
    
def test_add_book_success(mocker):
    mocker.patch("services.library_service.get_book_by_isbn", return_value=None)
    mocker.patch("services.library_service.insert_book", return_value=True)
    ok, x = libary.add_book_to_catalog("Test", "Test", "1234567890123", 1)
    assert ok is True