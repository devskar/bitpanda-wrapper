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

    Methods
    -------
    to_dict()
        Returns the attributes in a dictionary to use in a POST request
    """

    def __init__(self, curr_code, amount, recipient):
        self.currency_code = curr_code
        self.amount = amount
        self.recipient = recipient

    def to_dict(self):
        return {
            'currency': self.currency_code,
            'amount': self.amount,
            'recipient': {
                'address': self.recipient.address,
                'destination_tag': self.recipient.destination_tag
            }
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
    transaction_id : string(uuid)
        Transaction id of the executed withdrawal

    Methods
    -------
    from_json(json)
        Returns CryptoWithdraw instance based on json

    """

    def __init__(self, amount, fee, recipient, transaction_id):
        self.amount = amount
        self.fee = fee
        self.recipient = recipient
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

        return CryptoWithdraw(json['amount'],
                              json['fee'],
                              Recipient(json['recipient'], json['destination_tag']),
                              json['transaction_id'])


class WithdrawFiatBody:
    """
    Body of an POST request used for fiat withdrawal


    Attributes
    ----------
    curr_code : str
        Currency code of fiat asset
    amount : str
        Amount to withdraw
    payout_account_id : str
        Id of an payout account which is tied to specific IBAN.

    Methods
    -------
    to_dict()
        Returns the attributes in a dictionary to use in a POST request
    """

    def __init__(self, curr_code, amount, payout_account_id):
        self.currency_code = curr_code
        self.amount = amount
        self.payout_account_id = payout_account_id

    def to_dict(self):
        return {
            'currency': self.currency_code,
            'amount': self.amount,
            'payout_account_id': self.payout_account_id
        }


class Recipient:
    """
    Address of the recipient

    Parameters
    ----------
    address : str
        Crypto address to which should be the transfer executed.
    destination_tag : string
        Destination tag for the transaction, if the transaction requires it.

    """

    def __init__(self, address, destination_tag=''):
        self.address = address
        self.destination_tag = destination_tag
