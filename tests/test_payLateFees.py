import pytest
from services.library_service import pay_late_fees, refund_late_fee_payment
from services.payment_service import PaymentGateway
from unittest.mock import Mock
import time


def test_payLateFees_Successful(mocker):
    # 
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
    fake_patron_id = "123456"

    mock_payment_gateway.process_payment.return_value = (True, f"txn_{fake_patron_id}_{int(time.time())}", f"Payment of ${fee_amount:.2f} processed successfully")
    success, message, transaction_id = pay_late_fees(patron_id=fake_patron_id, book_id=77, payment_gateway=mock_payment_gateway)
    
    assert success == True
    assert "payment of $1.50 processed successfully" in message.lower()
    assert transaction_id is not None
    
    mock_payment_gateway.process_payment.assert_called_once()
    mock_payment_gateway.process_payment.assert_called_with( 
        patron_id=fake_patron_id,
        amount=1.50,
        description=f"Late fees for '{bookTitle}'"
    )

def test_payLateFees_InvalidPatron(mocker):
    # 
    mock_calc_fee = mocker.patch(
        "services.library_service.calculate_late_fee_for_book", 
        return_value={'fee_amount': 1.5, 'days_overdue': 3, 'status': '3 days overdue'}
    )

    mock_get_book = mocker.patch(
        "services.library_service.get_book_by_id",
        return_value={"id":77,"title":"Test Book"}
    ) 
    
    mock_payment_gateway = Mock(spec=PaymentGateway)

    success, message, transaction_id = pay_late_fees(patron_id="123456789", book_id=77, payment_gateway=mock_payment_gateway)
    
    assert success == False
    assert "invalid patron id" in message.lower()
    assert transaction_id is None

    mock_payment_gateway.process_payment.assert_not_called()

def test_payLateFees_noFeesOwed(mocker):
    # 
    mock_calc_fee = mocker.patch(
        "services.library_service.calculate_late_fee_for_book", 
        return_value={'fee_amount': 0.00, 'days_overdue': 0, 'status': '0 days overdue'}
    )

    mock_get_book = mocker.patch(
        "services.library_service.get_book_by_id",
        return_value={"id":88,"title":"Test Book"}
    ) 
    
    mock_payment_gateway = Mock(spec=PaymentGateway)

    success, message, transaction_id = pay_late_fees(patron_id="112233", book_id=88, payment_gateway=mock_payment_gateway)
    
    assert success == False
    assert "no late fees" in message.lower()
    assert transaction_id is None

    mock_payment_gateway.process_payment.assert_not_called()

def test_payLateFees_gatewayDenies_amountLow(mocker):
    # test when the gateway declines the payment --> bc/ amount is too low
    mock_calc_fee = mocker.patch(
        "services.library_service.calculate_late_fee_for_book", 
        return_value={'fee_amount': 1.00, 'days_overdue': 2, 'status': '2 days overdue'}
    )

    mock_get_book = mocker.patch(
        "services.library_service.get_book_by_id",
        return_value={"id":88,"title":"Test Book"}
    ) 
    
    bookTitle = mock_get_book.return_value["title"]

    mock_payment_gateway = Mock(spec=PaymentGateway)

    mock_payment_gateway.process_payment.return_value = (False, "", "Invalid amount: must be greater than 0")
    success, message, transaction_id = pay_late_fees(patron_id="112233", book_id=88, payment_gateway=mock_payment_gateway)
    
    assert success == False
    assert "payment failed" in message.lower()
    assert transaction_id is None

    mock_payment_gateway.process_payment.assert_called_once()
    mock_payment_gateway.process_payment.assert_called_with( 
        amount = 1.00,
        patron_id="112233",
        description=f"Late fees for '{bookTitle}'"
    )

def test_payLateFees_gatewayExceptionError(mocker):
    # test when the gateway declines the payment --> bc/ amount is too low
    mock_calc_fee = mocker.patch(
        "services.library_service.calculate_late_fee_for_book", 
        return_value={'fee_amount': 3, 'days_overdue': 6, 'status': '6 days overdue'}
    )

    mock_get_book = mocker.patch(
        "services.library_service.get_book_by_id",
        return_value={"id":99,"title":"Test Book"}
    ) 
    
    bookTitle = mock_get_book.return_value["title"]

    mock_payment_gateway = Mock(spec=PaymentGateway)

    mock_payment_gateway.process_payment.side_effect = Exception("network error")
    success, message, transaction_id = pay_late_fees(patron_id="445566", book_id=99, payment_gateway=mock_payment_gateway)
    
    assert success == False
    assert "payment processing error" in message.lower()
    assert transaction_id is None

    mock_payment_gateway.process_payment.assert_called_once()
    mock_payment_gateway.process_payment.assert_called_with( 
        amount = 3.00,
        patron_id="445566",
        description=f"Late fees for '{bookTitle}'"
    )



