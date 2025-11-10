import pytest
from services.library_service import pay_late_fees, refund_late_fee_payment
from services.payment_service import PaymentGateway
from unittest.mock import Mock
import time


#TESTS FOR PAYING LATE FEES
def test_payLateFees_Successful(mocker):
    # test paying fees with valid input
    mock_calc_fee = mocker.patch(
        "services.library_service.calculate_late_fee_for_book", 
        return_value={'fee_amount': 1.5, 'days_overdue': 3, 'status': '3 days overdue'}
    )

    mock_get_book = mocker.patch(
        "services.library_service.get_book_by_id",
        return_value={"id":77,"title":"Test Book"}
    )

    bookTitle = mock_get_book.return_value['title']
    fee_amount = mock_calc_fee.return_value['fee_amount']
    
    mock_payment_gateway = Mock(spec=PaymentGateway)

    mock_payment_gateway.process_payment.return_value = (True, f"txn_123456_{int(time.time())}", f"Payment of ${fee_amount:.2f} processed successfully")
    success, message, transaction_id = pay_late_fees("123456", 77, mock_payment_gateway)
    
    assert success == True
    assert "payment of $1.50 processed successfully" in message.lower()
    assert transaction_id is not None
    
    mock_payment_gateway.process_payment.assert_called_once()
    mock_payment_gateway.process_payment.assert_called_with( 
        patron_id="123456",
        amount=1.50,
        description=f"Late fees for '{bookTitle}'"
    )

def test_payLateFees_InvalidPatron(mocker):
    # test paying fees with invalid patron id
    mocker.patch(
        "services.library_service.calculate_late_fee_for_book", 
        return_value={'fee_amount': 1.5, 'days_overdue': 3, 'status': '3 days overdue'}
    )

    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value={"id":67,"title":"Test Book"}
    ) 
    
    mock_payment_gateway = Mock(spec=PaymentGateway)

    success, message, transaction_id = pay_late_fees("123456789", 67, mock_payment_gateway)
    
    assert success == False
    assert "invalid patron id" in message.lower()
    assert transaction_id is None

    mock_payment_gateway.process_payment.assert_not_called()

def test_payLateFees_noFeesOwed(mocker):
    # test paying fees when nothing is owed
    mocker.patch(
        "services.library_service.calculate_late_fee_for_book", 
        return_value={'fee_amount': 0.00, 'days_overdue': 0, 'status': '0 days overdue'}
    )

    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value={"id":88,"title":"Test Book"}
    ) 
    
    mock_payment_gateway = Mock(spec=PaymentGateway)

    success, message, transaction_id = pay_late_fees("112233", 88, mock_payment_gateway)
    
    assert success == False
    assert "no late fees" in message.lower()
    assert transaction_id is None

    mock_payment_gateway.process_payment.assert_not_called()

def test_payLateFees_gatewayDenies_amountLow(mocker):
    # test when the gateway declines the payment --> bc/ amount is too low
    mocker.patch(
        "services.library_service.calculate_late_fee_for_book", 
        return_value={'fee_amount': 1.00, 'days_overdue': 2, 'status': '2 days overdue'}
    )

    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value={"id":88,"title":"Test Book"}
    ) 

    mock_payment_gateway = Mock(spec=PaymentGateway)

    mock_payment_gateway.process_payment.return_value = (False, "", "Invalid amount: must be greater than 0")
    success, message, transaction_id = pay_late_fees("112233", 88, mock_payment_gateway)
    
    assert success == False
    assert "payment failed" in message.lower()
    assert transaction_id is None

    mock_payment_gateway.process_payment.assert_called_once()
    mock_payment_gateway.process_payment.assert_called_with( 
        amount = 1.00,
        patron_id="112233",
        description=f"Late fees for 'Test Book'"
    )

def test_payLateFees_gatewayExceptionError(mocker):
    # test when a network error occurs in the payment gateway
    mocker.patch(
        "services.library_service.calculate_late_fee_for_book", 
        return_value={'fee_amount': 3, 'days_overdue': 6, 'status': '6 days overdue'}
    )

    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value={"id":99,"title":"Test Book"}
    ) 

    mock_payment_gateway = Mock(spec=PaymentGateway)

    mock_payment_gateway.process_payment.side_effect = Exception("network error")
    success, message, transaction_id = pay_late_fees("445566", 99, mock_payment_gateway)
    
    assert success == False
    assert "payment processing error" in message.lower()
    assert transaction_id is None

    mock_payment_gateway.process_payment.assert_called_once()
    mock_payment_gateway.process_payment.assert_called_with( 
        amount = 3.00,
        patron_id="445566",
        description=f"Late fees for 'Test Book'"
    )

def test_payLateFees_gatewayDenies_amountHigh(mocker):
    # test when the gateway declines the payment --> bc/ amount is too low
    mocker.patch(
        "services.library_service.calculate_late_fee_for_book", 
        return_value={'fee_amount': 1.00, 'days_overdue': 2, 'status': '2 days overdue'}
    )

    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value={"id":88,"title":"Test Book"}
    ) 

    mock_payment_gateway = Mock(spec=PaymentGateway)

    mock_payment_gateway.process_payment.return_value = (False, "", "Payment declined: amount exceeds limit")
    success, message, transaction_id = pay_late_fees("112233", 88, mock_payment_gateway)
    
    assert success == False
    assert "payment failed" in message.lower()
    assert transaction_id is None

    mock_payment_gateway.process_payment.assert_called_once()
    mock_payment_gateway.process_payment.assert_called_with( 
        amount = 1.00,
        patron_id="112233",
        description=f"Late fees for 'Test Book'"
    )

def test_payLateFees_feeInfoMissing(mocker):
    mocker.patch(
        "services.library_service.calculate_late_fee_for_book", 
        return_value=None
    )
    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value={"id":44,"title":"Test Book"}
    ) 

    mock_payment_gateway = Mock(spec=PaymentGateway)
    success, message, transaction_id = pay_late_fees("123456", 44, mock_payment_gateway)

    assert success == False
    assert "unable to calculate late fees" in message.lower()
    assert transaction_id is None

    mock_payment_gateway.process_payment.assert_not_called()

def test_payLateFees_bookNotFound(mocker):
    mocker.patch(
        "services.library_service.calculate_late_fee_for_book", 
        return_value={'fee_amount': 1.00, 'days_overdue': 2, 'status': '2 days overdue'}
    )
    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value=None
    ) 

    mock_payment_gateway = Mock(spec=PaymentGateway)
    success, message, transaction_id = pay_late_fees("123456", 44, mock_payment_gateway)

    assert success == False
    assert "book not found" in message.lower()
    assert transaction_id is None

    mock_payment_gateway.process_payment.assert_not_called()



# Tests for Refunding Late Payment

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






    
