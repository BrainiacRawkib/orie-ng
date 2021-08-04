class UserNotAMerchant(Exception):

    def __str__(self):
        return 'User not a merchant'
