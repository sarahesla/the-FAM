"""
Defines the FAM (Family Appointed Moderator) system which allows users
to track and control their spending.
"""

from bank_account import BankAccount, \
    AngelBankAccount, \
    TroublemakerBankAccount, \
    RebelBankAccount
from user import User
from budget import Budget
from transaction import Transaction
from random import randint


class FAM:
    """
    The FAM class drives the FAM system and allows the user to navigate
    their bank account and related actions.
    """

    def __init__(self, bank_account: BankAccount):
        """
        Initializes the FAM with a BankAccount and a dictionary of
        budget categories.
        :param bank_account: a BankAccount object
        """
        self.bank_account = bank_account
        self.budget_category_menu = {
            1: "Gaming",
            2: "Clothing",
            3: "Eating Out",
            4: "Miscellaneous",
            5: "Back"
        }

    def print_menu(self) -> int:
        """
        Prints menu options and allows user to input their choice.
        :return: an int
        """

        print("Welcome to the FAM!")
        print("-------------------")
        print("1. View Budgets")
        print("2. Record a Transaction")
        print("3. View Transactions by Budget")
        print("4. View Bank Account Details")
        print("5. Quit")
        print("-------------------")
        print("What would you like to do?")

        choice = int(input("---> "))
        return choice

    def print_budget_categories(self) -> str:
        """
        Displays the existing budget categories and prompts the user
        to make a choice.
        :return: a string representing the budget category
        """
        print("Please select a category")
        print("------------------------")

        user_choice = None
        while user_choice not in self.budget_category_menu:

            for key, value in self.budget_category_menu.items():
                print(f"{key}. {value}")

            print("------------------------")
            print("Which category?")
            user_choice = int(input("---> "))

            if user_choice not in self.budget_category_menu:
                print("Invalid choice.")
                self.print_budget_categories()
            elif self.budget_category_menu[user_choice] == "Back":
                self.simulate()

        return self.budget_category_menu[user_choice]

    def simulate(self):
        """
        Drives the program by executing the appropriate behaviour based
        on the user's input.
        """
        choice = -1
        while choice != 5:
            choice = self.print_menu()
            if choice == 1:
                self.bank_account.view_budgets()

            elif choice == 2:
                category = self.print_budget_categories()
                self.bank_account.add_transaction(category)

            elif choice == 3:
                category = self.print_budget_categories()
                self.bank_account.view_budget_transactions(category)

            elif choice == 4:
                print(self.bank_account)

            elif choice == 5:
                print("Thank you! Goodbye.")

            else:
                print("Please enter a valid choice (1-5).")

    @staticmethod
    def setup():
        """
        Initializes the FAM by leading the user through a series of
        questions to create a User and a BankAccount.
        :return:
        """
        print("Welcome to FAM!")
        print("Please enter the following details")
        print("----------------------------------")

        # Create a user
        name = input("Account Holder Name: ")
        age = int(input("Account Holder Age: "))
        user = User(name, age)

        # Account details
        account_name = input("Account Name: ")
        account_number = input("Account Number: ")
        balance = float(input("Account Balance: $"))

        # Get budgets
        print("------------------------")
        budget_categories = {
            1: "Gaming",
            2: "Clothing",
            3: "Eating Out",
            4: "Miscellaneous"
        }

        budget = {}
        for key, val in budget_categories.items():
            amount = float(input(f"{val} Budget: $"))
            budget[val] = Budget(amount)

        # Select account type
        types = {
            1: (AngelBankAccount, "Angel Bank Account"),
            2: (TroublemakerBankAccount, "Troublemaker Bank Account"),
            3: (RebelBankAccount, "Rebel Bank Account")
        }

        choice = None
        while choice not in types:
            print("------------------------")
            print("Please select an account type")
            print("------------------------")
            for key, val in types.items():
                print(f"{key}. {val[1]}")
            choice = int(input("---> "))

            if choice not in types:
                print("Invalid choice, please try again.")
                continue

        if choice == 1:
            bank_account = AngelBankAccount(user, account_name,
                                            account_number, balance,
                                            budget)
        elif choice == 2:
            bank_account = TroublemakerBankAccount(user, account_name,
                                                   account_number, balance,
                                                   budget)
        else:
            bank_account = RebelBankAccount(user, account_name,
                                            account_number, balance,
                                            budget)
        return bank_account

    @staticmethod
    def load_test_user():
        """
        Generates a test user and populates the BankAccount with
        randomized transactions.
        """
        user = User("Sarah", 22)
        budget = {
            "Gaming": Budget(200),
            "Clothing": Budget(300),
            "Eating Out": Budget(250),
            "Miscellaneous": Budget(500),
        }
        bank_account = RebelBankAccount(user,
                                        "Test Account",
                                        "A123",
                                        1500.98,
                                        budget)
        transactions = {
            "Gaming": [],
            "Clothing": [],
            "Eating Out": [],
            "Miscellaneous": []
        }

        for key in transactions:
            for i in range(1, 4):
                transaction = Transaction(randint(1, 50), f"Store {i}")
                transactions[key].append(transaction)

        bank_account.transactions = transactions
        return bank_account


if __name__ == '__main__':
    user = FAM.setup()
    FAM_one = FAM(user)
    FAM_one.simulate()
    # test_FAM = FAM(FAM.load_test_user())
    # test_FAM.simulate()
