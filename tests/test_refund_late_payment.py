import pytest
from services.library_service import pay_late_fees, refund_late_fee_payment
from services.payment_service import PaymentGateway
from unittest.mock import Mock
import time

def test_refundPayment_Successful(mocker):
    # test refunding a with valid inputs
    stubTransactionID = f"txn_123456_{int(time.time())}"
    stubAmount = 3.00
    mock_payment_gateway = Mock(spec=PaymentGateway)

    mock_payment_gateway.refund_payment.return_value = (True, f"Refund of ${stubAmount:.2f} processed successfully. Refund ID: {stubTransactionID}")
    success, message = refund_late_fee_payment(stubTransactionID, stubAmount, mock_payment_gateway)

    assert success == True
    assert f"refund of ${stubAmount:.2f} processed successfully." in message.lower()

    mock_payment_gateway.refund_payment.assert_called_once()
    mock_payment_gateway.refund_payment.assert_called_with(stubTransactionID, stubAmount)

def test_refundPayment_invalidTransactionID(mocker):
    # test refunding a with an invalid transaction id
    stubTransactionID = f"weeeeeee_123456_{int(time.time())}"
    stubAmount = 2.00
    mock_payment_gateway = Mock(spec=PaymentGateway)

    success, message = refund_late_fee_payment(stubTransactionID, stubAmount, mock_payment_gateway)

    assert success == False
    assert "invalid transaction id." in message.lower()

    mock_payment_gateway.refund_payment.assert_not_called()

def test_refundPayment_amountTooLow(mocker):
    # test refunding when the amount is <= 0
    stubTransactionID = f"txn_567125_{int(time.time())}"
    stubAmount = -2.00
    mock_payment_gateway = Mock(spec=PaymentGateway)

    success, message = refund_late_fee_payment(stubTransactionID, stubAmount, mock_payment_gateway)

    assert success == False
    assert "refund amount must be greater than 0." in message.lower()

    mock_payment_gateway.refund_payment.assert_not_called()

def test_refundPayment_amountTooHigh(mocker):
    # test refunding when the amound > 15
    stubTransactionID = f"txn_567625_{int(time.time())}"
    stubAmount = 20.00
    mock_payment_gateway = Mock(spec=PaymentGateway)

    success, message = refund_late_fee_payment(stubTransactionID, stubAmount, mock_payment_gateway)

    assert success == False
    assert "refund amount exceeds maximum late fee." in message.lower()

    mock_payment_gateway.refund_payment.assert_not_called()

def test_refundPayment_networkException(mocker):
    # test refunding when the amound > 15
    stubTransactionID = f"txn_567445_{int(time.time())}"
    stubAmount = 2.00
    mock_payment_gateway = Mock(spec=PaymentGateway)

    mock_payment_gateway.refund_payment.side_effect = Exception("network error")
    success, message = refund_late_fee_payment(stubTransactionID, stubAmount, mock_payment_gateway)

    assert success == False
    assert "refund processing error" in message.lower()

    mock_payment_gateway.refund_payment.assert_called_once()
    mock_payment_gateway.refund_payment.assert_called_with(stubTransactionID, stubAmount) 

def test_refundPayment_refundFails(mocker):
    # test refunding when the amound > 15
    stubTransactionID = f"txn_227445_{int(time.time())}"
    stubAmount = 5.00
    mock_payment_gateway = Mock(spec=PaymentGateway)

    mock_payment_gateway.refund_payment.return_value = (False, "invalid")
    success, message = refund_late_fee_payment(stubTransactionID, stubAmount, mock_payment_gateway)

    assert success == False
    assert "refund failed" in message.lower()

    mock_payment_gateway.refund_payment.assert_called_once()
    mock_payment_gateway.refund_payment.assert_called_with(stubTransactionID, stubAmount)     






    
