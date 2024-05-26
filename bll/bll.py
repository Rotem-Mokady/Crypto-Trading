from typing import Union
from dataclasses import dataclass

import pandas as pd
import datetime as dt

from bll.binance_calc import Calc
from bll.bybit_operation import Bybit
from bll import constants


@dataclass
class _MarketData:
    close: Union[int, float]
    rsi: Union[int, float]
    hband: Union[int, float]
    lband: Union[int, float]
    time: dt.datetime

    @classmethod
    def get_latest_values(cls):
        data = cls._fetch_market_data()
        last_row_values = data.sort_index(ascending=False).iloc[0]
        last_row_values['time'] = last_row_values.name.to_pydatetime()

        return cls(**last_row_values)

    @staticmethod
    def _fetch_market_data() -> pd.DataFrame:
        candle_relevant_value = constants.CANDLE_RELEVANT_VALUE
        calc_obj = Calc(symbol=constants.BINANCE_SYMBOL, timeframe=constants.TIMEFRAME)

        rsi_values = calc_obj.rsi_calc(days_period=constants.RSI_PERIOD, parameter=candle_relevant_value)
        bollinger_values = calc_obj.bollinger_calc(
            days_period=constants.BOLLINGER_PERIOD, std_dev=constants.BOLLINGER_STD_DEV, parameter=candle_relevant_value
        ).drop(candle_relevant_value, axis=1)

        final_df = rsi_values.merge(bollinger_values, left_index=True, right_index=True)
        return final_df


@dataclass
class MarketData(_MarketData):
    rsi_threshold_buy: Union[int, float]
    rsi_threshold_sell: Union[int, float]

    def __init__(
            self,
            rsi_threshold_buy: Union[int, float],
            rsi_threshold_sell: Union[int, float],
    ) -> None:
        market_data = _MarketData.get_latest_values()
        super().__init__(**market_data.__dict__)

        self.rsi_threshold_buy = rsi_threshold_buy
        self.rsi_threshold_sell = rsi_threshold_sell


@dataclass
class TradingObj(MarketData, Bybit):
    risk_percentage: Union[int, float]

    def __init__(
            self,
            rsi_threshold_buy: Union[int, float],
            rsi_threshold_sell: Union[int, float],
            initial_capital: Union[int, float],
            risk_percentage: Union[int, float]
    ) -> None:

        MarketData.__init__(self, rsi_threshold_buy=rsi_threshold_buy, rsi_threshold_sell=rsi_threshold_sell)
        Bybit.__init__(self, initial_capital=initial_capital)
        self.risk_percentage = risk_percentage

        self.risk_amount = self.initial_capital * self.risk_percentage
        self.position_size = self.bybit.get_positions()
        # Calculate position size based on available capital and desired risk percentage
        self.order_size = self.risk_amount / self.close

    def buy_by_order_size(self) -> None:
        self.buy(self.order_size)

    def sell_by_position_size(self) -> None:
        self.sell(self.position_size)

    @property
    def str_time(self) -> str:
        return self.time.strftime('%d/%m/%Y %H:%M')

    @property
    def buying_log_msg(self) -> str:
        return f"{self.str_time} - BUYING"

    @property
    def selling_log_msg(self) -> str:
        return f"{self.str_time} - SELLING"

