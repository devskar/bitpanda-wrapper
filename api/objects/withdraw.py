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
        Address of the recipient
    address : string
        Crypto address to which should be the transfer executed.
    destination_tag : string optional
        Destination tag for the transaction, if the transaction requires it.

    Methods
    -------
    get_as_dict()
        Returns the attributes in a dictionary to use in a POST request
    """

    def __init__(self, curr_code, amount, recipient, address, destination_tag=None):
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


class CryptoWithdraw:
    """
    Response for an crypto withdrawal request.


    Attributes
    ----------
    amount : str
        Amount of withdrawal
    fee : str
        Fee of the withdrawal
    recipient : str
        Address of the recipient
    destination_tag : string
        Destination tag used if required.
    transaction_id : string(uuid)
        Transaction id of the executed withdrawal

    Methods
    -------
    from_json(json)
        Returns CryptoWithdraw instance based on json

    """

    def __init__(self, amount, fee, recipient, destination_tag, transaction_id):
        self.amount = amount
        self.fee = fee
        self.reipient = recipient
        self.destination_tag = destination_tag
        self.transaction_id = transaction_id

    @staticmethod
    def from_json(json):
        """
        Returns CryptoWithdraw instance based on json

        Parameters
        ----------
        json (str) : json

        Returns
        -------
        CryptoWithdraw : Returning CryptoWithdraw instance
       """

        return CryptoWithdraw(json['amount'], json['fee'], json['recipient'], json['destination_tag'], json['transaction_id'])