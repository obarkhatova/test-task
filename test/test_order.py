import pytest
from copy import deepcopy
from ..lib.order import Order, OrderType
from .fixtures.orders import tst_order


@pytest.mark.ORDER
@pytest.mark.UNIT
@pytest.mark.parametrize('id_, type_, price, volume, scenario',
                         [
                            (1, OrderType.BID, 2, 3, 'New bid'),
                            (10, OrderType.ASK, 50, 60, 'New ask')
                         ],
                         )
def test_create_order_positive(id_, type_, price, volume, scenario):
    """
        Scenario: New order creation
        Given: Order attributes
        When:
        Then:  A new Order instance is created, each attribute is initialised
    """
    new_order = Order(id_, type_, price, volume)
    assert isinstance(new_order, Order), f'{scenario}: unexpected object type'
    assert new_order.id_ == id_, "Unexpected id value"
    assert new_order.type_ == type_, "Unexpected type value"
    assert new_order.price == price, "Unexpected price value"
    assert new_order.volume == volume, "Unexpected volume value"


@pytest.mark.ORDER
@pytest.mark.UNIT
@pytest.mark.parametrize('id_, type_, price, volume, scenario',
                         [
                            (0, OrderType.BID, 2, 3, 'Zero id'),
                            (-1, OrderType.ASK, 50, 60, 'Negative id'),
                            (1, 'ASK', 50, 60, 'Unknown type value'),
                            (1, OrderType.ASK, 0, 60, 'Zero price'),
                            (1, OrderType.BID, 10, 0, 'Zero volume'),
                         ],)
def test_create_order_negative(id_, type_, price, volume, scenario):
    """
           Scenario: An attempt to create an Order with incorrect attributes passed
           Given: Incorrect Order attributes
           When: A new Order instance is created
           Then:  A new Order instance is not created, an exception is raised
    """
    with pytest.raises(ValueError) as e:
        Order(id_, type_, price, volume)


@pytest.mark.ORDER
@pytest.mark.UNIT
@pytest.mark.parametrize('tst_order, new_price, new_volume, scenario',
                         [
                            ({'id_': 1, 'type_': OrderType.ASK, 'price': 100, 'volume': 11}, 300, 20, 'ASK update'),
                            ({'id_': 2, 'type_': OrderType.BID, 'price': 200, 'volume': 22}, 50, 1, 'BID update')
                         ],
                         indirect=['tst_order'])
def test_update_order_positive(new_price, new_volume, scenario, tst_order):
    """
       Scenario: Order update
       Given: Order instance, correct attribute values to update
       When: Test Order instance is updated with new values
       Then:  Order instance is successfully updated, not editable arguments remain the same
    """
    original_obj = deepcopy(tst_order)
    tst_order.update(price=new_price, volume=new_volume)
    assert tst_order.price == new_price, f'{scenario}: Attribute has not been changed'
    assert tst_order.volume == new_volume, f'{scenario}: Attribute has not been changed'
    assert tst_order.id_ == original_obj.id_, f'{scenario}: Attribute must not be changed'
    assert tst_order.type_ == original_obj.type_, f'{scenario}: Attribute must not be changed'


@pytest.mark.ORDER
@pytest.mark.UNIT
@pytest.mark.parametrize('tst_order, new_attr, scenario',
                         [
                            ({'id_': 1, 'type_': OrderType.ASK, 'price': 100, 'volume': 11},
                             {'id_': 111}, 'id of ASK order update '),

                            ({'id_': 2, 'type_': OrderType.BID, 'price': 200, 'volume': 22},
                             {'type_': OrderType.ASK}, 'type of BID order update')
                         ],
                         indirect=['tst_order'])
def test_update_order_not_allowed(new_attr, scenario, tst_order):
    """
       Scenario: Not allowed Order attributes update
       Given: Order instance, not allowed attribute values
       When: Test Order instance is updated with new values of attributes which are not allowed to be changed
       Then:  Exception is raised
    """
    with pytest.raises(ValueError) as e:
        tst_order.update(**new_attr)


@pytest.mark.ORDER
@pytest.mark.UNIT
@pytest.mark.parametrize('tst_order, new_price, new_volume, scenario',
                         [
                            (None, 0, 20, 'Order update with zero price'),
                            (None, 20, 0, 'Order update with zero volume'),
                         ],
                         indirect=['tst_order'])
def test_update_order_negative(tst_order, new_price, new_volume, scenario):
    """
       Scenario: Update Order with incorrect attribute values
       Given: Order instance
       When: Order is updated with incorrect values
       Then: Exception is raised. The object remains in the initial state
    """
    with pytest.raises(ValueError):
        tst_order.update(price=new_price, volume=new_volume)

