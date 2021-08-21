class UserNotAMerchant(Exception):
    """
    Raises an exception if a user is not a merchant.
    :exception
    """
    def __str__(self):
        return 'User not a merchant'
