from abc import ABC, abstractmethod


class BankAccount(ABC):

    def __init__(
        self,
        account_number,
        name,
        pin,
        starting_balance,
        savings_goal=0.0
    ):
        self.account_number = account_number
        self.account_name = name

        # Encapsulation
        self._pin = pin
        self._balance = starting_balance
        self._savings_goal = savings_goal


    def set_pin(self, new_pin):
        self._pin = new_pin


    def get_savings_goal(self):
        return self._savings_goal


    def set_savings_goal(self, amount):
        if amount <= 0:
            return False
        self._savings_goal = amount
        return True

    def check_balance(self):
        return self._balance

    def deposit(self, amount):

        if amount <= 0:
            return False

        self._balance += amount

        return True

    def withdraw(self, amount):

        if amount <= 0:
            return False

        # Polymorphism: each account type decides its own floor
        # for what the balance is allowed to drop to.
        if (self._balance - amount) < self.get_minimum_balance():
            return False

        self._balance -= amount

        return True

    def verify_pin(self, pin):

        return self._pin == pin

    def get_pin(self):

        return self._pin

    # Abstraction
    @abstractmethod
    def get_account_type(self):
        pass

    # Abstraction — subclasses define their own withdrawal floor
    # instead of overriding withdraw() itself.
    @abstractmethod
    def get_minimum_balance(self):
        pass


# Inheritance
class SavingsAccount(BankAccount):

    # Polymorphism
    def get_account_type(self):
        return "Savings Account"

    def get_minimum_balance(self):
        return 0.0


# Inheritance
class StudentAccount(BankAccount):

    # Polymorphism
    def get_account_type(self):
        return "Student Account"

    def get_minimum_balance(self):
        return 0.0


# Inheritance
class BusinessAccount(BankAccount):

    OVERDRAFT_LIMIT = 5000.0

    # Polymorphism
    def get_account_type(self):
        return "Business Account"

    def get_minimum_balance(self):
        # Allowed to dip into overdraft, unlike the other account types.
        return -self.OVERDRAFT_LIMIT