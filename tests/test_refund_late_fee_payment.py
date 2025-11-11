import pytest
from services.payment_service import PaymentGateway
from services import library_service as libary   

def test_refund_success(mocker):
    gateway = mocker.Mock(spec=PaymentGateway)
    gateway.refund_payment.return_value = (True, "ok")
    ok, msg = libary.refund_late_fee_payment("txn_123456", 15, gateway)
    gateway.refund_payment.assert_called_once_with("txn_123456", 15)
    assert ok is True and "ok" in msg
    
def test_refund_invalid_transaction_id(mocker):
    gateway = mocker.Mock(spec=PaymentGateway)
    ok, msg = libary.refund_late_fee_payment("aaaaa123457788", 15, gateway)
    gateway.refund_payment.assert_not_called()
    assert ok is False and "Invalid transaction ID" in msg
    


def test_refund_invalid_amount_negative(mocker):
    gateway = mocker.Mock(spec=PaymentGateway)
    ok, msg = libary.refund_late_fee_payment(transaction_id="txn_123456", amount=-1.0, payment_gateway=gateway)
    gateway.refund_payment.assert_not_called()
    assert ok is False and "greater than 0" in msg
    
    
def test_refund_invalid_amount_is_0(mocker):
    gateway = mocker.Mock(spec=PaymentGateway)
    ok, msg = libary.refund_late_fee_payment(transaction_id="txn_123456", amount=0, payment_gateway=gateway)
    gateway.refund_payment.assert_not_called()
    assert ok is False and "greater than 0" in msg
    

def test_refund_invalid_amount_is_more_then_15(mocker):
    gateway = mocker.Mock(spec=PaymentGateway)
    ok, msg = libary.refund_late_fee_payment(transaction_id="txn_123456", amount=100, payment_gateway=gateway)
    gateway.refund_payment.assert_not_called()
    assert ok is False and "exceeds maximum" in msg