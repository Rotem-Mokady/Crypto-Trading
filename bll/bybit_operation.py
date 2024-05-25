from pybit.unified_trading import HTTP
from typing import Union

from constants import (
    API_KEY, API_SECRET, BYBIT_SYMBOL, BYBIT_ORDER_TYPE, BYBIT_BUYING_METHOD_NAME, BYBIT_SELLING_METHOD_NAME
)


class Bybit:

    def __init__(self, initial_capital: Union[int, float]) -> None:

        self.initial_capital = initial_capital

        # Initialize the Bybit exchange API
        self.bybit = HTTP(
            testnet=False,
            # Optional: Add your API key and secret if you have them
            # api_key=API_KEY,
            # api_secret=API_SECRET
        )

        self._symbol = BYBIT_SYMBOL
        self._order_type = BYBIT_ORDER_TYPE

        self._buy_method_name = BYBIT_BUYING_METHOD_NAME
        self._sell_method_name = BYBIT_SELLING_METHOD_NAME

    def buy(self, quantity: Union[int, float]) -> None:
        self.bybit.place_order(
            symbol=self._symbol, side=self._buy_method_name, quantity=quantity, price=self.initial_capital
        )

    def sell(self, quantity: Union[int, float]) -> None:
        self.bybit.place_order(
            symbol=self._symbol, side=self._sell_method_name, quantity=quantity, price=self.initial_capital
        )

    def get_positions(self) -> int:
        return self.bybit.get_positions(symbol=self._symbol)['result'][0]['size']
