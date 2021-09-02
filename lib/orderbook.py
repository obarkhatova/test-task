from collections import defaultdict
from orderbook.lib.order import Order, OrderType


class OrderBook:
    def __init__(self, *orders: Order):
        self.prices = defaultdict(list)
        self.ids = dict()
        self.append(*orders)

    def _add_to_ids(self, order: Order):
        if self.get(order.id_):
            raise ValueError(f'Order {order.id_} exists')
        self.ids.update({order.id_: order})

    def append(self, *orders: Order):
        for new_order in orders:
            self._add_to_ids(new_order)
            self.prices[new_order.price].append(new_order)

    def get(self, id_: int) -> Order:
        return self.ids.get(id_)

    def remove(self, id_: int):
        order_to_del = self.get(id_)
        if not order_to_del:
            return
        orders_of_price = self.prices.get(order_to_del.price)
        for idx, o in enumerate(orders_of_price):
            if o.id_ == order_to_del.id_:
                orders_of_price.pop(idx)
                break
        self.ids.pop(id_)

    def update(self, id_: int, **params: (str, int)) -> Order:
        order_to_upd = self.get(id_)
        if order_to_upd:
            return order_to_upd.update(**params)

    def snapshot(self) -> dict:
        asks = []
        bids = []
        for price in sorted(self.prices.keys()):
            orders_per_price = self.prices.get(price)
            print(price)
            print(orders_per_price)
            asks_vol = sum([order.volume for order in orders_per_price if order.type_ == OrderType.ASK])
            bids_vol = sum([order.volume for order in orders_per_price if order.type_ == OrderType.BID])
            asks.append(dict((('price', price), ('volume', asks_vol))))
            bids.insert(0, dict((('price', price), ('volume', bids_vol))))

        return {
            'Asks': asks,
            'Bids': bids
        }

    def get_as_dict(self, id_) -> dict:
        ord = self.get(id_)
        if ord:
            return ord.as_dict
