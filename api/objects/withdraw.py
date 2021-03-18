class WithdrawCryptoBody:
    """
    Body of an POST request used for crypto withdrawal


    Attributes
    ----------
    curr_code : str
        Currency code of crypto asset
    amount : str
        Amount to withdraw
    recipient : str
        None todo
    address : string
        Crypto address to which should be the transfer executed.
    destination_tag : string optional
        Destination tag for the transaction, if the transaction requires it.

    Methods
    -------
    get_as_dict()
        Returns the attributes in a dictionary to use in a POST request
    """

    def __init__(self, curr_code, amount, recipient, address, destination_tag = None):
        self.currency_code = curr_code
        self.amount = amount
        self.recipient = recipient
        self.address = address
        self.destination_tag = destination_tag

    def get_as_dict(self):
        return {
            'currency': self.currency_code,
            'amount': self.amount,
            'recipient': self.recipient,
            'address': self.address,
            'destination_tag': self.destination_tag
        }
