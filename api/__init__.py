import requests

from .objects.currencies import Currency
from .objects.orders import Order, SuccessfulOrder
from .objects.withdraw import WithdrawCryptoBody, WithdrawFiatBody
from .static import Scope, Fiat
from api.objects.wallets import Wallet

BASE_URL = 'https://api.exchange.bitpanda.com/public/v1'


def get_currencies():
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
        currencies.add(Currency(currency['code'], currency['precision']))

    return currencies


# Todo Candlesticks


def get_fee_groups():
    """
    Returns details of all general Fee Groups.
    fee_discount_rate and minimum_price_value are applied when BEST fee collection is enabled.

    Returns:
    -------
    string/json: fees

    """

    url = BASE_URL + '/fees'

    response = requests.get(url)

    return response.json()


def get_instruments():
    """
    Get a list of all available trade instruments

    Returns:
    -------


    """

    url = BASE_URL + '/instruments'

    response = requests.get(url)

    return response.json()


def get_server_time_iso():
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


def get_server_time_millis():
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


class Account:
    """
    Class to make private related HTTP requests to https://exchange.bitpanda.com/
    """

    def __init__(self, api_key):
        self.api_key = api_key

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

        return Wallet.from_json(response.json())

    def deposit_crypto(self, curr_code):
        """
        Creates a new deposit address for the given currency code.
        Make sure to use a valid api key with the scope WITHDRAW, otherwise this operation will be rejected.
        The api key can be generated via the user interface at https://exchange.bitpanda.com/account/api/keys.

        Todo
            unavailable?

        Parameters
        ----------
        curr_code : str, optional
            Currency code of crypto asset

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

    def withdraw_crypto(self, withdraw_crypto_body: WithdrawCryptoBody):
        """
        Initiates a withdrawal.
        Make sure to use a valid api key with the scope WITHDRAW, otherwise this operation will be rejected.
        The api key can be generated via the user interface.
        2FA is disabled and the withdraw operation will not require an approval by email.
        It's best practice to limit the api key to one IP address and never give out the api key.
        Only crypto currencies are allowed to withdraw on this endpoint!

        Todo
            - unavailable?

        Parameters
        ----------
        withdraw_crypto_body : withdraw.WithdrawCryptoBody
            Withdrawal information


        """

        url = BASE_URL + '/account/withdraw/crypto'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        response = requests.post(url, headers=headers, params=withdraw_crypto_body.to_dict())

        print(response.json())

    def get_deposit_address(self, curr_code):
        """
        Returns a deposit address for the given crypto currency code.
        Fiat currency codes will not work! Make sure to use a valid API key with the scope WITHDRAW,
        otherwise this operation will be rejected. The api key can be generated via the user interface.

        Todo
            - not working?

        Parameters
        ----------
        curr_code : str
            Currency code of crypto asset

        Returns
        -------
        Account : account belonging to api_key

        """

        url = BASE_URL + '/account/deposit/crypto/' + curr_code

        params = {
            'currency_code': curr_code
        }

        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        response = requests.get(url, headers=headers, params=params)

        print(response.json())

        if not response.json()['enabled']:
            return None

        return response.json()['address']

    def get_deposit_fiat(self, fiat: Fiat):
        """
        Returns deposit information for SEPA payments.
        Make sure to use a valid API key with the scope WITHDRAW, otherwise this operation will be rejected.
        The API key can be generated via the user interface.

        Parameters
        ----------
        fiat : Fiat
            The fiat of the deposit wanted.

        Returns
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

    def withdraw_fiat(self, withdraw_fiat_body: WithdrawFiatBody):
        """
        Initiates a withdrawal.
        Make sure to use a valid api key with the scope WITHDRAW, otherwise this operation will be rejected.
        The api key can be generated via the user interface.
        2FA is disabled and the withdrawal operation will not require an approval by E-Mail.
        A best practice is to limit the api key to one IP and never hand out the api key.
        Only EUR can be withdrawn on this endpoint!

        Todo
            - unavailable?

        Parameters
        ----------
        withdraw_fiat_body : withdraw.WithdrawFiatBody
            Withdrawal information


        """

        url = BASE_URL + '/account/withdraw/fiat'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        response = requests.post(url, headers=headers, params=withdraw_fiat_body.to_dict())

        print(response.json())

        return response.json()['transaction_id']

    def get_account_deposits(self, start=None, end=None, currency_code=None, max_page_size=None, cursor=None):
        """
        Return a paginated report on past cleared deposits, sorted by timestamp (newest first).
        If no query parameters are defined, it returns the last 100 deposits.

        Parameters
        ----------
        start : str
            (Zoned date time value compliant with ISO 8601 which adheres to RFC3339. All market times are in UTC.)
            Defines start of a query search.
        end : str
            (Zoned date time value compliant with ISO 8601 which adheres to RFC3339. All market times are in UTC.)
            Defines end of a query search.
        currency_code : str
            Filter deposit history by currency code
        max_page_size : str
            Set max desired page size. If no value is provided, by default a maximum of 100 results per page
            are returned. The maximum upper limit is 100 results per page.
        cursor : str
            Pointer specifying the position from which the next pages should be returned.

        Returns
        -------
        list(json) : Returns the deposit history of account

        """

        params = {
            'from': start,
            'to': end,
            'currency_code': currency_code,
            'max_page_size': max_page_size,
            'cursor': cursor
        }

        url = BASE_URL + '/account/deposits'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        response = requests.get(url, headers=headers, params=params)

        return response.json()['deposit_history']

    def get_account_deposits_from_bitpanda(self, start=None, end=None, currency_code=None, max_page_size=None,
                                           cursor=None):
        """
        Return a paginated report on past cleared deposits which were transfers from Bitpanda.
        This endpoint returns only transfers from Bitpanda, if you wish to see all deposits use Deposits,
        sorted by timestamp (newest first). If no query parameters are defined, it returns the last 100 deposits.

        Parameters
        ----------
        start : str
            (Zoned date time value compliant with ISO 8601 which adheres to RFC3339. All market times are in UTC.)
            Defines start of a query search.
        end : str
            (Zoned date time value compliant with ISO 8601 which adheres to RFC3339. All market times are in UTC.)
            Defines end of a query search.
        currency_code : str
            Filter deposit history by currency code
        max_page_size : str
            Set max desired page size. If no value is provided, by default a maximum of 100 results per page
            are returned. The maximum upper limit is 100 results per page.
        cursor : str
            Pointer specifying the position from which the next pages should be returned.

        Returns
        -------
        list(json) : Returns the deposit history from Bitpanda of account

        """

        params = {
            'from': start,
            'to': end,
            'currency_code': currency_code,
            'max_page_size': max_page_size,
            'cursor': cursor
        }

        url = BASE_URL + '/account/deposits/bitpanda'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        response = requests.get(url, headers=headers, params=params)

        return response.json()['deposit_history']

    def get_account_withdrawals(self, start=None, end=None, currency_code=None, max_page_size=None, cursor=None):
        """
        Return a paginated report on past cleared deposits, sorted by timestamp (newest first).
        If no query parameters are defined, it returns the last 100 deposits.

        Parameters
        ----------
        start : str
            (Zoned date time value compliant with ISO 8601 which adheres to RFC3339. All market times are in UTC.)
            Defines start of a query search.
        end : str
            (Zoned date time value compliant with ISO 8601 which adheres to RFC3339. All market times are in UTC.)
            Defines end of a query search.
        currency_code : str
            Filter withdrawal history by currency code
        max_page_size : str
            Set max desired page size. If no value is provided, by default a maximum of 100 results per page
            are returned. The maximum upper limit is 100 results per page.
        cursor : str
            Pointer specifying the position from which the next pages should be returned.

        Returns
        -------
        list(json) : Returns the deposit history of account

        """

        params = {
            'from': start,
            'to': end,
            'currency_code': currency_code,
            'max_page_size': max_page_size,
            'cursor': cursor
        }

        url = BASE_URL + '/account/withdrawals'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        response = requests.get(url, headers=headers, params=params)

        return response.json()['withdrawal_history']

    def get_account_withdrawals_from_bitpanda(self, start=None, end=None, currency_code=None, max_page_size=None,
                                              cursor=None):
        """
        Return a paginated report on past cleared withdrawals which were transfers from Bitpanda.
        This endpoint returns only transfers from Bitpanda, if you wish to see all withdrawals use Withdrawals,
        sorted by timestamp (newest first). If no query parameters are defined, it returns the last 100 deposits.

        Parameters
        ----------
        start : str
            (Zoned date time value compliant with ISO 8601 which adheres to RFC3339. All market times are in UTC.)
            Defines start of a query search.
        end : str
            (Zoned date time value compliant with ISO 8601 which adheres to RFC3339. All market times are in UTC.)
            Defines end of a query search.
        currency_code : str
            Filter withdrawal history by currency code
        max_page_size : str
            Set max desired page size. If no value is provided, by default a maximum of 100 results per page
            are returned. The maximum upper limit is 100 results per page.
        cursor : str
            Pointer specifying the position from which the next pages should be returned.

        Returns
        -------
        list(json) : Returns the withdrawals history from Bitpanda of account

        """

        params = {
            'from': start,
            'to': end,
            'currency_code': currency_code,
            'max_page_size': max_page_size,
            'cursor': cursor
        }

        url = BASE_URL + '/account/withdrawals/bitpanda'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        response = requests.get(url, headers=headers, params=params)

        return response.json()['withdrawal_history']

    def get_fees(self):
        """
        Returns the fee tiers, the running trading volume, the active fee tier specific for an account and
        the BEST fee collection settings.

        Returns
        -------
        dict/json :     Returns the fee tiers, the running trading volume, the active fee tier specific for an account
                        and the BEST fee collection settings.

        """

        url = BASE_URL + '/account/fees'
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        response = requests.get(url, headers=headers)

        return response.json()

    def toggle_best_fee_collection(self, collect_fees_in_best: bool = None):
        """
        Updates the fee toggle to enable or disable fee collection with BEST (Bitpanda Ecosystem Token).
        When the BEST fee collection feature is enabled a discount defined in fee_discount_rate will be deducted.
        In the payload example the value would be 25%. Additionally a minimum_price_value will be used for
        calculating how much BEST is deducted. In the example payload a price of 0.12 EUR would be used.
        If the price of BEST is lower than this value, then the minimum_price_value will be used for the calculation.
        Make sure you have enough BEST when a trade is executed, otherwise the fee discount and the minimum price value
        will not be applied!

        TODO
            unavailable?

        Parameters
        ----------
        collect_fees_in_best : bool

        Returns
        -------
        dict : updated fees

        """

        url = BASE_URL + '/account/deposit/crypto'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        params = {
            'collect_fees_in_best': collect_fees_in_best
        }

        response = requests.post(url, headers=headers, params=params)

        return response.json()

    def get_orders(self, start=None, end=None, instrument_code=None, with_cancelled_and_rejected=None,
                   with_just_filled_inactive=None, with_just_orders=None, max_page_size=None, cursor=None):
        """
        Return a paginated report on currently open orders, sorted by creation timestamp (newest first).
        Query parameters and filters can be used to specify if historical orders should be reported as well.
        If no query filters are defined, all orders which are currently active will be returned.
        If you want to query specific time frame parameters, from and to are mandatory,
        otherwise it will start from the latest orders.
        The maximum time frame you can query at one time is 100 days.

        Parameters
        ----------
        start : str
            (Zoned date time value compliant with ISO 8601 which adheres to RFC3339. All market times are in UTC.)
            Defines start of a query search.

        end : str
            (Zoned date time value compliant with ISO 8601 which adheres to RFC3339. All market times are in UTC.)
            Defines end of a query search.

        instrument_code : str
            Filter order history by instrument code

        with_cancelled_and_rejected : bool
            Return orders which have been cancelled by the user before being filled or rejected by the system as
            invalid. Additionally, all inactive filled orders which would return with "with_just_filled_inactive".

        with_just_filled_inactive : bool
            Return order history for orders which have been filled and are no longer open.
            Use of "with_cancelled_and_rejected" extends "with_just_filled_inactive"
            and in case both are specified the latter is ignored.

        with_just_orders : bool
            Returns order history for orders but does not return any trades corresponding to the orders.
            It may be significantly faster and should be used if user is not interesting in trade information.
            Can be combined with any other filter.

        max_page_size : str
            Set max desired page size. If no value is provided, by default a maximum of 100 results per page
            are returned. The maximum upper limit is 100 results per page.

        cursor : str
            Pointer specifying the position from which the next pages should be returned.

        Returns
        -------
        list(json) : Returns the withdrawals history from Bitpanda of account

        """

        params = {
            'from': start,
            'to': end,
            'instrument_code': instrument_code,
            'with_cancelled_and_rejected': with_cancelled_and_rejected,
            'with_just_filled_inactive': with_just_filled_inactive,
            'with_just_orders': with_just_orders,
            'max_page_size': max_page_size,
            'cursor': cursor
        }

        url = BASE_URL + '/account/orders'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        response = requests.get(url, headers=headers, params=params)

        return response.json()

    def create_order(self, order: Order):
        """
        Create a new order of the type LIMIT, MARKET or STOP.

        Additionally, LIMIT Orders support GOOD_TILL_CANCELLED, GOOD_TILL_TIME, IMMEDIATE_OR_CANCELLED and
        FILL_OR_KILL which can be specified as time_in_force option.
        If none is specified GOOD_TILL_CANCELLED is assumed. If GOOD_TILL_TIME is set as time_in_force,
        client is also expected to provide time after which the limit order expires.

        There is a minimum size per order which can be looked up by querying the /instruments endpoint.
        Additionally, the precision limitations can be found there. Globally across all markets, at most 200 orders
        can be kept open at any given point in time.

        Optionally a client_id can be set by clients to track orders without waiting for the assigned order id.
        While an order with a set client_id is active other orders with the same client_id will be rejected as
        duplicates. As soon as the order is fully filled or cancelled by user or automatically by system,
        another order can be created using the same client_id. Therefore specifying a client_id is not a suitable
        protection against re-execution of an order.

        Make sure to have a valid api key with the scope TRADE, otherwise this operation will be rejected.
        The api key can be generated via the user interface at https://exchange.bitpanda.com/account/api/keys.

        Parameters
        ----------
        order : orders.Order
            (Zoned date time value compliant with ISO 8601 which adheres to RFC3339. All market times are in UTC.)
            Defines start of a query search.


        Returns
        -------
        SuccessfulOder : Returns a SuccessfulOrder instance

        """

        url = BASE_URL + '/account/orders'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        response = requests.get(url, headers=headers, params=order.as_dict())

        return SuccessfulOrder.from_json(response.json())

    def close_all_orders(self, instrument_code=None, *ids):
        """
        Submits a close request for all open orders of an account.

        Optionally the user can specify either the instrument_code or a list of ids as HTTP query parameters.
        The instrument_code parameter will only close orders for a given instrument,
        while the ids parameter can be used to specify various orders regardless to which markets they belong.
        Calling this endpoint without any of the optional parameters will close all orders of the account.
        Calling this endpoint with both query parameters set is not supported.

        There is an upper limit of 20 orders that can be closed at a time through the ids parameter.
        The orders must be submitted by the account that the API key has been created for.
        When the API returns 200 OK, it returns a list of UUIDs representing the orders that were submitted
        for cancellation.

        Bitpanda Pro will always fill orders with best effort. Therefore, when attempting to close all orders,
        these orders may be in the process of being filled. In this case,
        Bitpanda Pro will attempt to close the orders but the order may already be partially/fully filled.

        Make sure to have a valid API key with the scope TRADE, otherwise this operation will be rejected.
        The API key can be generated via the user interface at https://exchange.bitpanda.com/account/api/keys.

        Parameters
        ----------
        instrument_code : str
            Only close orders in given market (omit to close all orders)

        ids : *
            An array of comma separated UUIDs, of the form [UUID_1,UUID_2,UUID_3,...,UUID_N]

        Returns
        -------
        list : The following orders ids were submitted for closing

        """

        url = BASE_URL + '/account/orders'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        params = {
            'instrument_code': instrument_code,
            'ids': list(ids)
        }

        response = requests.get(url, headers=headers, params=params)

        return response.json()
