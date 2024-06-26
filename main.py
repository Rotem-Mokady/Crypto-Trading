import logging
import datetime as dt
from typing import Union

from bll import TradingObj


logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define the format of log messages
    # Specify the filename for the log file
    filename=f'logs/trading_logs_{dt.datetime.now().date().strftime("%Y%m%d")}.txt',
    filemode='a'  # Append mode to append logs to the file (use 'w' to overwrite)
)


def trading_logic_running(initial_capital: Union[int, float]) -> None:
    trader = TradingObj(
        initial_capital=initial_capital, rsi_threshold_buy=30, rsi_threshold_sell=70, risk_percentage=0.02
    )

    # Place buy order if RSI is below the buy threshold and price touches lower Bollinger Band
    if trader.rsi < trader.rsi_threshold_buy and trader.close <= trader.lband:
        trader.buy_by_order_size()
        logging.info(trader.buying_log_msg)
    # Place sell order if RSI is above the sell threshold or price touches upper Bollinger Band
    elif trader.rsi > trader.rsi_threshold_sell or trader.close >= trader.hband:
        trader.sell_by_position_size()
        logging.info(trader.selling_log_msg)


if __name__ == '__main__':
    trading_logic_running(initial_capital=68465)

