from pytest import fixture
from random import choice, randint

from orderbook.lib.order import Order, OrderType
from orderbook.lib.orderbook import OrderBook


@fixture(scope="function")
def tst_order(request):
    """
        Fixture creates a new Order instance
        Fixture must be parametrized via request.param object.

        Format of request.param
        -----------------------
        Parameter must be a dict with the following keys
        'id_' : `int` - id of a new Order, id > 0
        'type_' : `OrderType` - OrderType.ASK or OrderType.BID
        'price' : 'int' - price value, price > 0
        'volume' : 'int' - volume, volume > 0
    """
    params = request.param
    if params:
        return Order(params['id_'], params['type_'], params['price'], params['volume'])
    else:
        return Order(randint(1, 1000), choice([OrderType.ASK, OrderType.BID]), randint(10, 100), randint(1, 100))


@fixture(scope="function")
def tst_ordbook(request):
    """
        Fixture creates a new Order book instance. Order book contains N random Orders,
        where N value is passed in. Order ids are set from 1 to N+1
        Fixture must be parametrized via request.param object.

        Format of request.param
        -----------------------
        Parameter must be
        'num' : `int` - number of Orders in the Order book, if num is omitted or equal to 0,
        then an empty OrderBook instance is returned
    """
    num = request.param.get('num')
    if not num or num == 0:
        return OrderBook()
    orders = [Order(i+1, choice([OrderType.ASK, OrderType.BID]), randint(10, 100), randint(1, 100))
              for i in range(num)]
    return OrderBook(*orders)


