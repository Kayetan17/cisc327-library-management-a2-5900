import pytest
from services.payment_service import PaymentGateway
from services import library_service as libary   

def test_pay_late_fees_success(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 15.00, "days_overdue": 100},)
    
    mocker.patch("services.library_service.get_book_by_id", return_value={"id": 1, "title": "Test"},)

    gateway = mocker.Mock(spec=PaymentGateway)
    gateway.process_payment.return_value = (True, "txn_123456", "Ok")

    ok, msg, txn = libary.pay_late_fees("123456", 42, payment_gateway=gateway)
    gateway.process_payment.assert_called_once_with(
        patron_id="123456",
        amount=15.00,                       
        description="Late fees for 'Test'", 
    )
    assert ok is True and txn == "txn_123456"


def test_pay_late_fees_declined(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 15.00, "days_overdue": 100},)
    
    mocker.patch("services.library_service.get_book_by_id", return_value={"id": 1, "title": "Test"})
    
    gateway = mocker.Mock(spec=PaymentGateway)
    gateway.process_payment.return_value = (False, "txn_123456", "declined")

    ok, msg, txn = libary.pay_late_fees("123456", 1, gateway)

    gateway.process_payment.assert_called_once()
    assert ok is False and txn == None
    
def test_pay_late_fees_invalid_patron_id(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 15.00, "days_overdue": 100},)

    mocker.patch("services.library_service.get_book_by_id", return_value={"id": 1, "title": "Test"})

    gateway = mocker.Mock(spec=PaymentGateway)

    ok, msg, txn = libary.pay_late_fees("aaaaaaaaaaaaaaaaaa", 1, gateway)

    gateway.process_payment.assert_not_called()
    assert ok is False and txn is None
    

def test_pay_late_fees_zero_fee(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 0, "days_overdue": 0},)

    mocker.patch("services.library_service.get_book_by_id", return_value={"id": 1, "title": "Test"})

    gateway = mocker.Mock(spec=PaymentGateway)

    ok, msg, txn = libary.pay_late_fees("123456", 1, gateway)

    gateway.process_payment.assert_not_called()
    assert ok is False and txn is None
    
    
def test_pay_late_fees_exception(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 15.00, "days_overdue": 100},)

    mocker.patch("services.library_service.get_book_by_id", return_value={"id": 1, "title": "Test"})

    gateway = mocker.Mock(spec=PaymentGateway)
    gateway.process_payment.side_effect = ConnectionError("timeout")

    ok, msg, txn = libary.pay_late_fees("123456", 5, gateway)

    gateway.process_payment.assert_called_once()
    assert ok is False and txn is None