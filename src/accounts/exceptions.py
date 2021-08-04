class MultipleUserAccountException(Exception):

    def __str__(self):
        return 'Multi-User mode cannot be enabled for this account. ' \
               'The account can only support one type of account.'
