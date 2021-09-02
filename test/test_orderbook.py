import pytest
from copy import deepcopy
from ..lib.order import Order, OrderType
from ..lib.orderbook import OrderBook
from .fixtures.orders import tst_order, tst_ordbook


@pytest.mark.ORDERBOOK
@pytest.mark.UNIT
@pytest.mark.parametrize('orders,scenario',
                         [
                             (Order(1, OrderType.BID, 2, 3), 'One order append'),
                             ([Order(1, OrderType.BID, 2, 3),
                               Order(2, OrderType.ASK, 2, 3),
                               Order(3, OrderType.BID, 3, 4),
                               ],
                              'List of orders are added into Order book')
                         ],
                         )
def test_orderbook_constructor(orders, scenario):
    """
        Scenario: Create a new order book
        Given: Order items
        When:  Order book is created with order instances passed
        Then:  A new Order book instance is created, each attribute is initialised
    """
    # Constructor verification
    obook = None
    if isinstance(orders, Order):
        obook = OrderBook(orders)
        orders = [orders, ]
    elif isinstance(orders, list):
        obook = OrderBook(*orders)

    for ord in orders:
        assert ord == obook.get(ord.id_), f'{scenario}: Order {ord.id_} not found'


@pytest.mark.ORDERBOOK
@pytest.mark.UNIT
@pytest.mark.parametrize('orders,scenario',
                         [
                             (Order(1, OrderType.BID, 2, 3),  'One order append'),
                             ([Order(1, OrderType.BID, 2, 3),
                               Order(2, OrderType.ASK, 2, 3),
                               Order(3, OrderType.BID, 3, 4),
                               ],
                               'List of orders are added into Order book')
                         ],
                         )
def test_orderbook_append_order_positive(orders, scenario):
    """
        Scenario: Append an order into an Order book
        Given: Order items
        When:  Orders are appended
        Then:  Order book contains the appended items
    """
    obook = OrderBook()

    if isinstance(orders, Order):
        obook.append(orders)
        orders = [orders,]
    elif isinstance(orders, list):
        obook.append(*orders)

    for ord in orders:
        assert ord == obook.get(ord.id_), f'{scenario}: Order {ord.id_} not found'


@pytest.mark.ORDERBOOK
@pytest.mark.UNIT
def test_orderbook_append_order_into_not_empty_obook():
    """
        Scenario: Be sure that an appended orders don't corrupt order book
        Given: Not empty order book
        When:  Orders are appended
        Then:  New instances are appended, old instances remain untouched
    """
    old_orders = [Order(1, OrderType.BID, 2, 3),
                  Order(2, OrderType.ASK, 2, 3),
                  Order(3, OrderType.BID, 3, 4)
                  ]
    obook = OrderBook(*old_orders)
    new_orders = [Order(4, OrderType.BID, 2, 3),
                  Order(5, OrderType.ASK, 2, 3),
                  Order(6, OrderType.BID, 3, 4)
                  ]
    obook.append(*new_orders)
    for ord in (old_orders+new_orders):
        assert ord == obook.get(ord.id_), f'Order {ord.id_} not found'


@pytest.mark.ORDERBOOK
@pytest.mark.UNIT
@pytest.mark.parametrize('test_type, scenario',
                         [('constructor', 'ID duplication, constructor'),
                          ('append', 'ID duplication, constructor'),
                         ]
                         )
def test_orderbook_id_duplication(test_type, scenario):
    """
        Scenario: Order book doesn't allow id duplication
        Given: Orders with the same id value
        When:  Orders are appended
        Then:  Exception is raised
    """
    orders = [Order(1, OrderType.BID, 2, 3),
              Order(2, OrderType.ASK, 2, 3),
              ]
    obook = OrderBook(*orders)
    new_orders = deepcopy(orders)

    if test_type == 'constructor':
        with pytest.raises(ValueError):
            OrderBook(Order(1, OrderType.BID, 2, 3), Order(1, OrderType.ASK, 2, 3),)

    elif test_type == 'append':
        with pytest.raises(ValueError):
            obook.append(*new_orders)


@pytest.mark.ORDERBOOK
@pytest.mark.UNIT
@pytest.mark.parametrize('tst_ordbook, scenario',
                         [
                            ({'num': 5}, 'All instances removal'),
                         ],
                         indirect=['tst_ordbook'])
def test_delete_order(scenario, tst_ordbook):
    """
       Scenario: Order removal
       Given: Not empty Order book
       When: Orders are removed one by one
       Then:  Empty Order Book instance
    """
    num = len(tst_ordbook.ids)
    # try end delete not existed order
    assert tst_ordbook.remove(num + 1) is None, f"Non existent Order removal error"

    for i in range(num):
        tst_ordbook.remove(i+1)

    for i in range(num):
        assert tst_ordbook.get(i+1) is None, f"Not removed Order, Order id = {i+1}"

    # try end delete an Order from an empty Order book
    assert tst_ordbook.remove(num) is None, f"Order removal error"


@pytest.mark.ORDERBOOK
@pytest.mark.UNIT
@pytest.mark.parametrize('tst_ordbook, scenario',
                         [
                            ({'num': 5}, 'Get Order by id'),
                         ],
                         indirect=['tst_ordbook'])
def test_get_order(scenario, tst_ordbook):
    """
       Scenario: Get Order by id
       Given: Not empty Order book
       When: Get Order by id
       Then: Retrieved Order satisfies the requested id
       When: Get Order by not existed id
       Then: return value is None
    """
    id_ = len(tst_ordbook.ids)+10
    new_order = Order(id_, OrderType.BID, 2, 3)
    tst_ordbook.append(new_order)
    assert tst_ordbook.get(id_) == new_order, "Can't get Order by id"
    assert tst_ordbook.get(id_+100) is None, "Unexpected GET response"


@pytest.mark.ORDERBOOK
@pytest.mark.UNIT
@pytest.mark.parametrize('tst_ordbook, scenario',
                         [
                            ({'num': 5}, 'Get Order by id as dict'),
                         ],
                         indirect=['tst_ordbook'])
def test_get_order_as_dict(scenario, tst_ordbook):
    """
       Scenario: Get Order by id in dict format
       Given: Not empty Order book
       When: Get Order by id as dict
       Then: Retrieved dict data satisfies the requested id
       When: Get Order by not existed id
       Then: returned value is None
    """
    new_id = len(tst_ordbook.ids)+10
    new_order = Order(new_id, OrderType.BID, 2, 3)
    tst_ordbook.append(new_order)
    obj = tst_ordbook.get_as_dict(new_id)
    assert isinstance(obj, dict), "Order by id can't be received"
    assert obj['id'] == new_order.id_, "Unknown object received"
    assert obj['type'] == new_order.type_.name, "Unknown object received"
    assert obj['price'] == new_order.price, "Unknown object received"
    assert obj['volume'] == new_order.volume, "Unknown object received"

    assert tst_ordbook.get(new_id+100) is None, "Unexpected GET response"


@pytest.mark.ORDERBOOK
@pytest.mark.UNIT
@pytest.mark.parametrize('tst_ordbook, param, scenario',
                         [
                            ({'num': 5}, 'price', 'Update Order price'),
                            ({'num': 5}, 'volume', 'Update Order volume'),
                         ],
                         indirect=['tst_ordbook'])
def test_update_positive(scenario, param, tst_ordbook):
    """
       Scenario: Update Order. Updatable params are price and value
       Given: Not empty Order book
       When: Update each Order from the book
       Then: Each Order is successfully updated
    """
    num = len(tst_ordbook.ids)
    for i in range(1, num+1):
        ord = tst_ordbook.get(i)
        new_val = getattr(ord, param) + 10
        tst_ordbook.update(i, **{param: new_val})
        assert getattr(ord, param) == new_val, f'Attribute {param} not updated'


def test_snapshot():
    """
          Scenario: Order book snapshot
          Given: Not empty Order book
          When: Get snapshot
          Then: Snaphot values are correct
       """
    ordbook = OrderBook(
        Order(1, OrderType.ASK, 1, 2),
        Order(2, OrderType.ASK, 1, 2),
        Order(3, OrderType.ASK, 3, 4),
        Order(4, OrderType.ASK, 3, 4),
        Order(5, OrderType.ASK, 5, 6),
        Order(6, OrderType.ASK, 5, 6),
        Order(7, OrderType.BID, 1, 2),
        Order(8, OrderType.BID, 1, 2),
        Order(9, OrderType.BID, 3, 4),
        Order(10, OrderType.BID, 3, 4),
        Order(11, OrderType.BID, 5, 6),
        Order(12, OrderType.BID, 5, 6),
        Order(13, OrderType.BID, 5, 6),
    )
    assert ordbook.snapshot() == {
        'Asks': [
           {
            'price': 1,
            'volume': 4
           },
            {
                'price': 3,
                'volume': 8
            },
            {
                'price': 5,
                'volume': 12
            }
        ],
        'Bids': [
            {
                'price': 5,
                'volume': 18
            },
            {
                'price': 3,
                'volume': 8
            },
            {
                'price': 1,
                'volume': 4
            }
        ]
    }


