from enum import IntEnum


class OrderType(IntEnum):
    ASK = 0
    BID = 1


class Order:
    updatable = ('price', 'volume')

    def __init__(self, id_: int, type_: OrderType, price: int, volume: int):
        if id_ <= 0:
            raise ValueError(f'Unexpected id value: {id_}')
        if not isinstance(type_, OrderType):
            raise ValueError(f'Unexpected type value {type_}')
        if price <= 0:
            raise ValueError(f'Price unexpected value: {price}')
        if volume <= 0:
            raise ValueError(f'Volume unexpected value: {volume}')

        self.id_ = id_
        self.type_ = type_
        self.price = price
        self.volume = volume

    def update(self, **params: (str, int)):
        for key, val in params.items():
            if key in self.updatable:
                setattr(self, key, val)
            else:
                raise ValueError(f'Not updatable key {key}')
        return self

    @property
    def as_dict(self) -> dict:
        return {
            'id': self.id_,
            'type': self.type_.name,
            'price': self.price,
            'volume': self.volume,
        }
