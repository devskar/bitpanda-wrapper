class Wallet:
    """
    A class used to hold CryptoWallets

    Attributes
    ----------
    id: str
        unique id by https://exchange.bitpanda.com/.com
    wallets : set(Wallet)
        set of wallets

    Methods
    -------
    from_json(json)
        Returns wallet instance based on json
    """
    def __init__(self, id, wallets):
        self.id = id
        self.wallets = wallets

    @staticmethod
    def from_json(json):
        """
        Returns account instance based on json

        Parameters
        ----------
        json (str) : json

        Returns
        -------
        Wallet : Returning wallet instance
       """

        wallets = set()

        for wallet in json['balances']:
            wallets.add(CryptoWallet(wallet['account_id'], wallet['currency_code'], wallet['change'],
                                     wallet['available'], wallet['locked'], wallet['sequence'], wallet['time']))

        return Wallet(json['account_id'], wallets)


class CryptoWallet:
    """
    Stores a cryptocurrency
    ...
    Attributes
    ----------
    id: str
        unique id by https://exchange.bitpanda.com/.com

    currency_code : str
        represents the name of the currency

    change : str
        todo

    available : str
        todo

    locked : str
        todo

    sequence : int
        todo

    time : str
        todo


    """

    def __init__(self, id, currency_code, change, available, locked, sequence, time):
        self.id = id
        self.currency_code = currency_code
        self.change = change
        self.available = available
        self.locked = locked
        self.sequence = sequence
        self.time = time

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.id == other.id
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.id)