import os
from pybit.unified_trading import HTTP
from typing import Union

from bll.constants import (
    BYBIT_SYMBOL, BYBIT_ORDER_TYPE, BYBIT_BUYING_METHOD_NAME, BYBIT_SELLING_METHOD_NAME,
)


class Bybit:

    def __init__(self, initial_capital: Union[int, float]) -> None:

        self.initial_capital = initial_capital

        self._symbol = BYBIT_SYMBOL
        self._order_type = BYBIT_ORDER_TYPE

        self._buy_method_name = BYBIT_BUYING_METHOD_NAME
        self._sell_method_name = BYBIT_SELLING_METHOD_NAME

        self.dry_run = os.environ['DRY_RUN_USER_ANSWER'] == 'Y'
        self.api_key = os.environ['API_KEY']
        self.api_secret = os.environ['API_SECRET']

        # Initialize the Bybit exchange API
        self.bybit = HTTP(
            testnet=False,
            # Optional: Add your API key and secret if you have them
            api_key=self.api_key,
            api_secret=self.api_secret
        )

    def buy(self, quantity: Union[int, float]) -> None:
        if not self.dry_run:
            self.bybit.place_order(
                symbol=self._symbol, side=self._buy_method_name, quantity=quantity, price=self.initial_capital
            )

    def sell(self, quantity: Union[int, float]) -> None:
        if not self.dry_run:
            self.bybit.place_order(
                symbol=self._symbol, side=self._sell_method_name, quantity=quantity, price=self.initial_capital
            )

    def get_positions(self) -> int:
        return self.bybit.get_positions(symbol=self._symbol)['result'][0]['size']
