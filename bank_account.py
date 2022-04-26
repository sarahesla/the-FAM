"""
Contains class definitions for all BankAccount types as well as
relevant abstract classes and supporting methods.
"""

from user import User
from abc import ABC
from abc import abstractmethod
from transaction import Transaction


class BankAccount(ABC):
    """
    An abstract base class that represents a BankAccount. Defines
    the general interface of all BankAccounts which must include:
        - account owner,
        - account name,
        - account number,
        - balance,
        - budget, and
        - transactions
    """

    def __init__(self, account_owner: User, account_name: str,
                 account_number: str, balance: float, budget: dict):
        """
        Initializes a BankAccount.
        :param account_owner: a User object
        :param account_name: a string
        :param account_number: a string
        :param balance: a float
        :param budget: a dictionary
        """
        self.account_owner = account_owner
        self.account_name = account_name
        self.account_number = account_number
        self.balance = balance
        self.budget = budget
        self.transactions = {
            "Gaming": [],
            "Clothing": [],
            "Eating Out": [],
            "Miscellaneous": []
        }

    def view_budgets(self) -> None:
        """
        Displays information relating to each budget category.
        """
        print("\n------ Budgets -----\n")
        for category in self.budget:
            allocated = self.budget[category].amount
            spent = self.get_budget_total(category)
            remaining = allocated - spent
            if remaining < 0:
                remaining = 0
            print(f"| {category} |")
            print(f"Amount Allocated: ${allocated:.2f}")
            print(f"Amount Spent: ${spent:.2f}")
            print(f"Amount Remaining: ${remaining:.2f}")
            print(f"Locked: {self.budget[category].locked}\n")

    def get_budget_total(self, category) -> float:
        """
        Calculates the total amount spent in a particular budget
        category.
        :param category: a string
        :return: a float representing the total
        """
        total = 0
        for transaction in self.transactions[category]:
            total += transaction.amount
        return total

    def get_transaction_details(self) -> Transaction:
        """
        Prompts the user for details relating to their transaction.
        :return: a Transaction object
        """
        print("Please enter your transaction details")
        print("-------------------------------------")
        store = input("Store: ")
        amount = float(input("Amount: $"))
        transaction = Transaction(amount, store)

        return transaction

    def validate_transaction(self, transaction: Transaction,
                             category: str) -> bool:
        """
        Determines the validity of a Transaction. A Transaction is valid
        if the amount does not exceed the BankAccount's current balance,
        and the category of the transaction is not locked.
        :param transaction: a Transaction object
        :param category: a string
        :return: a boolean flag representing validity
        """
        if transaction.amount > self.balance:
            print("---> Unable to process transaction, insufficient funds.")
            return False
        if self.budget[category].locked:
            print("---> Unable to process transaction, this category is "
                  "locked.")
            return False
        return True

    @abstractmethod
    def check_thresholds(self, category: str) -> float:
        """
        Provides a partial implementation for checking a budget's total
        spending against the thresholds of each BankAccount type.
        Calculates the percentage used of a budget category.
        :param category: a string
        :return: a float
        """
        budget_total = 0
        for transaction in self.transactions[category]:
            budget_total += transaction.amount
        budget_percentage = (budget_total /
                             self.budget[category].amount) * 100
        return budget_percentage

    def add_transaction(self, category: str) -> None:
        """
        Executes the necessary steps for adding a transaction. If
        the transaction proceeds through each step successfully,
        it is added to the dictionary of transactions and then the
        spending in that category is checked against the
        BankAccount's thresholds.
        :param category: a string
        """
        transaction = self.get_transaction_details()
        valid = self.validate_transaction(transaction, category)

        if valid:
            print("---> Transaction Added!")
            self.transactions[category].append(transaction)
            self.balance -= transaction.amount
            self.check_thresholds(category)

    @abstractmethod
    def warning_message(self, percentage: float) -> str:
        """
        Contains a message warning the user that they have hit
        their warning threshold.
        :param percentage: a float representing the percentage used of
        a budget category
        :return: a string
        """
        pass

    @abstractmethod
    def exceed_message(self) -> str:
        """
        Contains a message notifying the user that they have exceeded
        a budget category.
        :return: a string
        """
        pass

    def view_budget_transactions(self, category) -> None:
        """
        Displays transactions from a particular budget category
        :param category: a string
        """
        print(f"\n----- {category} Transactions -----\n")
        for transaction in self.transactions[category]:
            print(f"{transaction}\n")

    def __str__(self):
        # Account Details
        formatted = "\n----- Account Details -----\n"
        formatted += f"\nAccount Name: {self.account_name}"
        formatted += f"\nAccount Number: {self.account_number}"
        formatted += f"\nBalance: ${self.balance:.2f}"

        # Account Owner
        formatted += f"\n{self.account_owner}\n"

        # Budget Details
        formatted += "\n------ Budgets -----\n"
        for category in self.budget:
            allocated = self.budget[category].amount
            spent = self.get_budget_total(category)
            remaining = allocated - spent
            if remaining < 0:
                remaining = 0
            formatted += f"\n| {category} |\n"
            formatted += f"Amount Allocated: ${allocated:.2f}\n"
            formatted += f"Amount Spent: ${spent:.2f}\n"
            formatted += f"Amount Remaining: ${remaining:.2f}\n"
            formatted += f"Locked: {self.budget[category].locked}\n"

        # Transaction Details
        for category in self.transactions:
            if len(self.transactions[category]) > 0:
                formatted += f"\n----- {category} Transactions -----\n"
                for transaction in self.transactions[category]:
                    formatted += f"\n{transaction}\n"

        return formatted


class AngelBankAccount(BankAccount):
    """
    Defines an AngelBankAccount. Angels never get locked out of a budget
    category. They receive a warning once they've exceeded 90% of a budget
    category, and are politely notified if the exceeded it fully.
    """

    def __init__(self, *args):
        """
        Initializes an AngelBankAccount. Contains all attributes
        from the ABC BankAccount, plus a warning threshold of 90.
        :param args: all arguments get passed up to the ABC BankAccount
        """
        super().__init__(*args)
        self.warning_threshold = 90

    def warning_message(self, percentage: float) -> str:
        """
        Returns a polite warning message notifying the Angel that they
        have hit their warning threshold.
        :param percentage: a float
        :return: a string
        """
        return f"You have used up {int(percentage)}% of your budget for " \
               f"this category. Please be mindful.\n"

    def exceed_message(self) -> str:
        """
        Returns a polite message notifying the Angel that they have exceeded
        a budget category.
        :return: a string
        """
        return "You have exceeded this budget category. Please " \
               "be mindful.\n"

    def check_thresholds(self, category: str) -> None:
        """
        Checks the total spending of a particular budget category against
        the Angel's thresholds. Displays any relevant messages.
        :param category: a string
        """
        percentage = super().check_thresholds(category)

        if percentage > self.warning_threshold:
            if percentage > 100:
                print(self.exceed_message())
            else:
                print(self.warning_message(percentage))

    def __str__(self):
        formatted = "----- Account Type: Angel -----\n"
        formatted += f"\nWarning Threshold: {self.warning_threshold}%\n"
        formatted += super().__str__()

        return formatted


class TroublemakerBankAccount(BankAccount):
    """
    Defines a TroublemakerBankAccount. A Troublemaker receives a warning
    message when they exceed 75% of a budget category. They receive
    a polite warning message when they exceed a budget fully, and get
    locked out of that category if they exceed it by 120%.
    """

    def __init__(self, *args):
        """
        Initializes a TroublemakerBankAccount. Contains all attributes
        from the ABC BankAccount, plus a warning threshold of 75 and
        a lock threshold of 120.
        :param args: all arguments get passed up to the ABC BankAccount
        """
        super().__init__(*args)
        self.warning_threshold = 75
        self.lock_threshold = 120

    def warning_message(self, percentage: float) -> str:
        """
        Returns a polite warning message notifying the Troublemaker that
        they have hit their warning threshold.
        :param percentage: a float
        :return: a string
        """
        return f"You have used up {int(percentage)}% of your budget " \
               f"for this category. Please be mindful.\n"

    def exceed_message(self) -> str:
        """
        Returns a polite message notifying the Troublemaker that they have
        exceeded a budget category.
        :return: a string
        """
        return "You have exceeded this budget category. Please " \
               "be mindful.\n"

    def lock_out(self) -> str:
        """
        Returns a message notifying the Troublemaker they have exceeded
        their lock threshold.
        :return: a string
        """
        return "You have exceeded this budget category by over 120%. " \
               "As such, this category has been locked.\n"

    def check_thresholds(self, category: str) -> None:
        """
        Checks the total spending of a particular budget category against
        the TroubleMaker's thresholds. Displays any relevant messages and
        locks the budget category if necessary.
        :param category: a string
        """
        percentage = super().check_thresholds(category)

        if percentage > self.warning_threshold:
            if percentage > self.lock_threshold:
                print(self.lock_out())
                self.budget[category].locked = True
            elif percentage > 100:
                print(self.exceed_message())
            else:
                print(self.warning_message(percentage))

    def __str__(self):
        formatted = "----- Account Type: Troublemaker -----\n"
        formatted += f"\nWarning Threshold: {self.warning_threshold}%"
        formatted += f"\nLock Threshold: {self.lock_threshold}%\n"
        formatted += super().__str__()

        return formatted


class RebelBankAccount(BankAccount):
    """
    Defines a RebelBankAccount. A Rebel receives an aggressive warning
    message whenever they exceed a budget category by 50%. A budget
    category is locked if they use 100% of it. Should they exceed two
    budget categories, the whole account is locked.
    """
    def __init__(self, *args):
        """
        Initializes a RebelBankAccount. Contains all attributes
        from the ABC BankAccount, plus a warning_threshold of 50 and
        a lock_threshold of 100.
        :param args: all arguments get passed up to the ABC BankAccount
        """
        super().__init__(*args)
        self.warning_threshold = 50
        self.lock_threshold = 100

    def warning_message(self, percentage: float) -> str:
        """
        Returns an aggressive warning message notifying the Rebel
        that they have hit their warning threshold.
        :param percentage: a float
        :return: a string
        """
        return f"WARNING!\nYou have used up {int(percentage)}% of " \
               f"this category's budget! DON'T BE STUPID.\n"

    def exceed_message(self) -> str:
        """
        Returns an aggressive message notifying the Rebel that they have
        exceeded a budget category.
        :return: a string
        """
        return "YOU HAVE EXCEEDED THIS BUDGET! IT IS NOW LOCKED. " \
               "SHAME ON YOU!\n"

    def lock_out(self) -> None:
        """
        Displays an aggressive warning message notifying the Rebel that
        they have been locked out of their account, and locks each
        budget category.
        """
        print("You have now exceeded two budgets! SHAME ON YOU.")
        print("Your account is now FULLY locked.\n")
        for category in self.budget:
            self.budget[category].locked = True

    def check_budgets(self) -> None:
        """
        Counts the number of budgets that have been exceeded/locked.
        """
        locked_count = 0
        for category in self.budget:
            if self.budget[category].locked:
                locked_count += 1

        if locked_count >= 2:
            self.lock_out()

    def check_thresholds(self, category: str) -> None:
        """
        Checks the total spending of a particular budget category against
        the Rebel's thresholds. Displays any relevant messages and
        locks the budget category if necessary. If a budget is exceeded,
        the check_budgets method is called.
        :param category: a string
        """
        percentage = super().check_thresholds(category)

        if percentage > self.warning_threshold:
            if percentage > self.lock_threshold:
                print(self.exceed_message())
                self.budget[category].locked = True
                self.check_budgets()
            else:
                print(self.warning_message(percentage))

    def __str__(self):
        formatted = "----- Account Type: Rebel -----\n"
        formatted += f"\nWarning Threshold: {self.warning_threshold}%"
        formatted += f"\nLock Threshold: {self.lock_threshold}%\n"
        formatted += super().__str__()

        return formatted
