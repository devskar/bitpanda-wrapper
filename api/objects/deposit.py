class Deposit:
    def __init__(self, transaction_id, account_id, amount, type, funds_source, time, currency, fee_amount, fee_currency):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.amount = amount
        self.type = type
        self.funds_source = funds_source
        self.time = time
        self.currency = currency
        self.fee_amount = fee_amount
        self.fee_currency = fee_currency

    @staticmethod
    def from_json(json):
        """
        Returns Deposit instance based on json

        Parameters
        ----------
        json (str) : json

        Returns
        -------
        Deposit : Returning Deposit instance
        """

        return Deposit(json['transaction_id'],
                       json['account_id'],
                       json['amount'],
                       json['type'],
                       json['funds_source'],
                       json['time'],
                       json['currency'],
                       json['fee_amount'],
                       json['fee_currency'])
