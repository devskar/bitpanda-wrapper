import requests
import pprint
from .static import Scope, Fiat
from .account import Account

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

        response = requests.get(url)

        return response.json()

    def get_currencies(self):
        """
        Returns currencies with their precision

        Returns:
        -------
        set(**tuple()): list with tuples containing code and precision of currency

        """

        url = BASE_URL + '/currencies'

        response = requests.get(url)

        json = response.json()

        currencies = set()

        for currency in json:
            currencies.add((currency['code'], currency['precision']))

        return currencies

    def get_server_time_iso(self):
        """
        Returns current server time of the bitpanda server in iso

        Returns:
        -------
        set(**tuple()): list with tuples containing code and precision of currency

        """

        url = BASE_URL + '/time'

        response = requests.get(url)

        json = response.json()

        return json['iso']

    def get_server_time_millis(self):
        """
        Returns elapsed milliseconds since Unix Epoch.

        Returns:
        -------
        int : list with tuples containing code and precision of currency

        """

        url = BASE_URL + '/time'

        response = requests.get(url)

        json = response.json()

        return json['epoch_millis']

    def get_account_balances(self):
        """
        Returns the balance details for an account.

        Returns:
        -------
        Account : account belonging to api_key

        """

        url = BASE_URL + '/account/balances'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        response = requests.get(url, headers=headers)

        return Account.from_json(response.json())

    def deposit_crypto(self, curr_code):
        """
        Creates a new deposit address for the given currency code.
        Make sure to use a valid api key with the scope WITHDRAW, otherwise this operation will be rejected.
        The api key can be generated via the user interface at https://exchange.bitpanda.com/account/api/keys.

        todo unavailbale?

        """

        url = BASE_URL + '/account/deposit/crypto'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        params = {
            'currency': curr_code
        }

        response = requests.post(url, headers=headers, params=params)

        print(response.json())

    def get_deposit_address(self, curr_code):
        """
        Returns a deposit address for the given crypto currency code.
        Fiat currency codes will not work! Make sure to use a valid API key with the scope WITHDRAW,
        otherwise this operation will be rejected. The api key can be generated via the user interface.

        todo

        Returns:
        -------
        Account : account belonging to api_key

        """

        url = BASE_URL + '/account/deposit/crypto/' + curr_code

        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        response = requests.get(url, headers=headers)

        if not response.json()['enabled']:
            return None

        return response.json()['address']

    def get_deposit_fiat(self, fiat: Fiat):
        """
        Returns deposit information for SEPA payments.
        Make sure to use a valid API key with the scope WITHDRAW, otherwise this operation will be rejected.
        The API key can be generated via the user interface.

        todo

        Returns:
        -------
        Account : account belonging to api_key

        """

        url = BASE_URL + '/account/deposit/fiat/' + fiat.value

        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()
