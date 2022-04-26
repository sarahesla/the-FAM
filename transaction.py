"""
Contains code relating to the Transaction class.
"""

from datetime import datetime


class Transaction:
    """
    Represents a Transaction object. Each Transaction contains a dollar
    amount, store name (representing the place the transaction took place),
    and a timestamp of when the Transaction was created.
    """

    def __init__(self, amount: float,  store: str):
        """
        Initializes a Transaction with a dollar amount, store name, and
        timestamp.
        :param amount: a float
        :param store: a string
        """
        self.amount = amount
        self.store = store.title()
        self.timestamp = datetime.now()

    def __str__(self):
        return f"| {self.store} |" \
               f"\nAmount: ${self.amount:.2f}" \
               f"\nAdded: {self.timestamp.strftime('%B %d, %Y at %H:%M PST')}"

