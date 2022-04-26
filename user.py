"""
Contains code relating to the User class.
"""


class User:
    """
    Represents a User. A User has a name and age.
    """

    def __init__(self, name: str, age: int):
        """
        Initializes a User with a name and age.
        :param name: a string
        :param age: an int
        """
        self.name = name
        self.age = age

    def __str__(self):
        return f"\n----- Account Holder Details -----\n" \
               f"\nName: {self.name}" \
               f"\nAge: {self.age}"
