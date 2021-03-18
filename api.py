from static import Scope
import requests
import pprint
printer = pprint.PrettyPrinter()


BASE_URL = 'https://api.exchange.bitpanda.com/public/v1'


class Api:
    """
    A class used to make HTTP requests to https://exchange.bitpanda.com/
    ...
    Attributes
    ----------
    scope : api.Scope
        scope your api key is set to

    Methods
    -------
    get_currencies()
        Returns currencies with their precision
    """

    def __init__(self, scope=Scope.READ):
        self._api_key = ''
        self._scope = scope

    @property
    def scope(self):
        """Get the current scope."""
        return self._scope

    @scope.setter
    def scope(self, value):
        self._scope = value

    @scope.deleter
    def scope(self):
        del self._scope

    @property
    def api_key(self):
        """Get the current api key."""
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    @api_key.deleter
    def api_key(self):
        del self._api_key

    def get_fees(self):
        """
        Returns bitpanda fees

        Returns:
        -------
        string/json: fees

        """

        url = BASE_URL + '/fees'

        response = requests.request('GET', url)

        return response.json()


    def get_currencies(self):
        """
        Returns currencies with their precision

        Returns:
        -------
        set(**tuple()): list with tuples containing code and precision of currency

        """

        url = BASE_URL + '/currencies'

        response = requests.request('GET', url)

        json = response.json()

        currencies = set()

        for currency in json:
            currencies.add((currency['code'], currency['precision']))

        return currencies

