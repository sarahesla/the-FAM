"""
Contains code related to the Budget class.
"""


class Budget:
    """
    Represents a budget. A budget contains a dollar amount representing
    an upper limit. A budget can also be locked to halt spending within
    that budget.
    """

    def __init__(self, amount: float):
        """
        Initializes a Budget with a dollar amount and sets locked to false.
        :param amount: a float
        """
        self.amount = amount
        self.locked = False

    def __str__(self):
        return f"\nAmount: ${self.amount:.2f}" \
               f"\nLocked: {self.locked}"
