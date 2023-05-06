
import pytest
from App.calculations import add, substract, multiply, devide, Bank_Account, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return Bank_Account()

@pytest.fixture
def bank_account():
    return Bank_Account(50)

@pytest.mark.parametrize("num1, num2, expected",[
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
    ])

def test_add(num1, num2, expected):
    print("test add function")
    # sum = add(5, 3)
    assert add(num1, num2) == expected

def test_substract():
    print("test add function")
    # sum = add(5, 3)
    assert substract(10, 5) == 5

def test_multiply():
    print("test add function")
    # sum = add(5, 3)
    assert multiply(5, 3) == 15

def test_devide():
    print("test add function")
    # sum = add(5, 3)
    assert devide(30, 3) == 10

def test_bank_set_initial_amount(bank_account):
    # bank_account = Bank_Account(50)
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    # bank_account = Bank_Account(50)
    bank_account.withdraw(50)
    assert bank_account.balance == 0

def test_deposit(bank_account):
    # bank_account = Bank_Account(50)
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_collect_interest(bank_account):
    # bank_account = Bank_Account(50)
    bank_account.collect_interest()
    assert round(bank_account.balance,0) == 55


@pytest.mark.parametrize("deposited, withdrew, expected",[
    (200, 100, 100),
      (250, 110, 140),
        (120, 40, 80)
        ])

def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)