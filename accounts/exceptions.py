class MultipleUserAccountException(Exception):
    """
    Exception to deny a user from being a merchant and a customer
    at the same time.
    :exception
    """
    def __str__(self):
        return 'Multi-User mode cannot be enabled for this account. ' \
               'The account can only support one type of account.'
