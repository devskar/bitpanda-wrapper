from enum import Enum


class Side(Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class Type(Enum):
    LIMIT = 'LIMIT'
    MARKET = 'MARKET'
    STOP = 'STOP'


class Time_In_Force(Enum):
    GOOD_TILL_CANCELLED = 'GOOD_TILL_CANCELLED'
    GOOD_TILL_TIME = 'GOOD_TILL_TIME'
    IMMEDIATE_OR_CANCELLED = 'IMMEDIATE_OR_CANCELLED'
    FILL_OR_KILL = 'FILL_OR_KILL'
    NONE = None


class Order:
    """
    A wrapper for accepted order types which can be submitted for execution.

    ...
    Attributes
    ----------
    instrument_code: str
        The instrument denotes unique market identifier.
        Both base and quote must be valid currency codes.

    type : Type
        The type of the order

    side : Side
        Direction of the Order

    amount : str
        The number of units to open order for

    price : str
        Is mandatory for LIMIT and STOP orders.
        Setting price for MARKET order type is ignored as this order type is always executed against instrument pricing
        available at the execution time.

    client_id : str
        The optional client order id prevents duplicated orders. Should be a unique and valid UUID of version 4.
        An order, with a client order id that already has been processed, will be rejected.

    time_in_force : Time_In_Force
        Only applicable to LIMIT orders. If IMMEDIATE_OR_CANCELLED is specified then the order must be filled
        immediately, only at the limit price or better. If the order cannot be filled immediately or fully,
        the unfilled portion will be cancelled. Alternatively, FILL_OR_KILL instructs the the exchange to either
        fully-fill the limit order at the desired price of cancel it automatically. If none is specified then
        GOOD_TILL_CANCELLED is considered.

    expire_after : str
        Only applicable to GOOD_TILL_TIME as time-in-force.
        The expiration time must be a valid MarketTime in the future relative to observed server time adjusted to
        minutely granularity.

    is_post_only : bool
        Only applicable to GOOD_TILL_CANCELLED and GOOD_TILL_TIME as time-in-force.
        When set to true (defaults to false), the order will be executed with a booking guarantee unless it results
        in a price match in which case it gets automatically cancelled.

    trigger_price : str
        Is mandatory for STOP orders.
        A stop-limit order will be executed at a specified price (see price), or better, after the given trigger price
        has been reached.

    order_id : str
        Id of a successful order given by Bitpanda

    account_id : str
        Id of account the order was made from given by Bitpanda

    time : str
        Time where an order was made

    filled_amount : str
        todo

    """

    def __init__(self, instrument_code: str, type: Type, side: Side, amount: str, price: str = None,
                 client_id: str = None, time_in_force: Time_In_Force = Time_In_Force.NONE, expire_after: str = None,
                 is_post_only: bool = False, trigger_price: str = None, order_id: str = None, account_id: str = None,
                 time: str = None, filled_amount: str = None):
        self.instrument_code = instrument_code
        self.type = type
        self.side = side
        self.amount = amount
        self.price = price
        self.client_id = client_id
        self.time_in_force = time_in_force
        self.expire_after = expire_after
        self.is_post_only = is_post_only
        self.trigger_price = trigger_price
        self.order_id = order_id
        self.account_id = account_id
        self.time = time
        self.filled_amount = filled_amount

    def as_dict(self):
        dictionary = {
            'instrument_code': self.instrument_code,
            'type': self.type.value,
            'side': self.side.value,
            'amount': self.amount,
            'price': self.price,
            'client_id': self.client_id,
            'time_in_force': self.time_in_force.value,
            'expire_after': self.expire_after,
            'is_post_only': self.is_post_only,
            'trigger_price': self.trigger_price,
            'order_id': self.order_id,
            'account_id': self.account_id,
            'time': self.time,
            'filled_amount': self.filled_amount
        }

        return {k: v for k, v in dictionary.items() if v is not None}


class LimitOrder(Order):
    def __init__(self, instrument_code: str, side: Side, amount: str, price: str = None,
                 client_id: str = None, time_in_force: Time_In_Force = Time_In_Force.NONE, expire_after: str = None,
                 is_post_only: bool = False):
        super().__init__(instrument_code=instrument_code, type=Type.LIMIT, side=side, amount=amount, price=price,
                         client_id=client_id, time_in_force=time_in_force, expire_after=expire_after,
                         is_post_only=is_post_only)


class StopOrder(Order):
    def __init__(self, instrument_code: str, side: Side, amount: str, price: str = None,
                 client_id: str = None, trigger_price: str = None):
        super().__init__(instrument_code=instrument_code, type=Type.STOP, side=side, amount=amount, price=price,
                         client_id=client_id, trigger_price=trigger_price)


class MarketOrder(Order):
    def __init__(self, instrument_code: str, side: Side, amount: str, price: str = None,
                 client_id: str = None):
        super().__init__(instrument_code=instrument_code, type=Type.MARKET, side=side, amount=amount, price=price,
                         client_id=client_id)


class SuccessfulOrder(Order):
    def __init__(self, order_id: str, client_id: str, account_id: str, instrument_code: str, time: str, side: Side,
                 price: str, amount: str, filled_amount: str, type: Type, time_in_force: Time_In_Force):
        super().__init__(order_id=order_id, client_id=client_id, account_id=account_id, instrument_code=instrument_code,
                         time=time, side=side, price=price, amount=amount, filled_amount=filled_amount,
                         type=type, time_in_force=time_in_force)

    @staticmethod
    def from_json(json):
        return SuccessfulOrder(order_id=json['order_id'], client_id=json['client_id'], account_id=json['account_id'],
                               instrument_code=json['instrument_code'], time=json['time'], side=Side[json['side']],
                               price=json['price'], amount=json['amount'], filled_amount=json['filled_amount'],
                               type=Type[json['type']], time_in_force=Time_In_Force[json['time_in_force']])
