import ccxt
import ta
from ta import momentum, volatility

import pandas as pd
import datetime as dt

from typing import List


class Calc:
    def __init__(self, symbol: str, timeframe: str) -> None:
        self.symbol = symbol
        self.timeframe = timeframe

        self.ohlcv_df = self._collect_ohlcv_data()

    @property
    def _candle_params(self) -> List[str]:
        return ['open', 'high', 'low', 'close', 'volume']

    @property
    def _date_param(self) -> str:
        return 'date'

    def _collect_ohlcv_data(self) -> pd.DataFrame:

        # Initialize the Binance exchange API
        binance = ccxt.binance()
        raw_data = binance.fetch_ohlcv(self.symbol, self.timeframe)

        df = pd.DataFrame(data=raw_data, columns=[self._date_param] + self._candle_params)
        df['date'] = df['date'].apply(lambda x: dt.datetime.fromtimestamp(x/1000))

        final_df = df.set_index(self._date_param)
        return final_df

    def rsi_calc(self, days_period: int, parameter: str) -> pd.DataFrame:
        relevant_data = self.ohlcv_df[parameter]
        rsi_df = ta.momentum.rsi(relevant_data, days_period).to_frame()

        final_df = rsi_df.merge(relevant_data.to_frame(), left_index=True, right_index=True)
        return final_df

    def bollinger_calc(self, days_period: int, std_dev: int, parameter: str) -> pd.DataFrame:
        relevant_data = self.ohlcv_df[parameter]

        upper_bb = ta.volatility.bollinger_hband(relevant_data, days_period, std_dev).to_frame()
        lower_bb = ta.volatility.bollinger_lband(relevant_data, days_period, std_dev).to_frame()

        final_df = upper_bb.merge(
            lower_bb, left_index=True, right_index=True
        ).merge(
            relevant_data.to_frame(), left_index=True, right_index=True
        )
        return final_df



