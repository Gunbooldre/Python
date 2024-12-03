from calculation import add, subtract, multiply, divide, BanckAccount
import pytest


@pytest.fixture
def zero_bank_account():
    return BanckAccount()


@pytest.fixture
def bank_account():
    return BanckAccount(50)


@pytest.mark.parametrize("num1, num2, result", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, result):
    print("Testing add function")
    assert add(num1, num2) == result


def test_subtract():
    print("Testing subtract function")
    assert subtract(9, 4) == 5


def test_multiply():
    print("Testing multiply function")
    assert multiply(5, 3) == 15


def test_divide():
    print("Testing divide function")
    assert divide(6, 3) == 2


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55
