from bll import TradingObj


def main() -> None:
    try:

        trader = TradingObj(
            initial_capital=68465, rsi_threshold_buy=30, rsi_threshold_sell=70, risk_percentage=0.02
        )

        # Place buy order if RSI is below the buy threshold and price touches lower Bollinger Band
        if trader.rsi < trader.rsi_threshold_buy and trader.close <= trader.lband:
            trader.buy_by_order_size()
        # Place sell order if RSI is above the sell threshold or price touches upper Bollinger Band
        elif trader.rsi > trader.rsi_threshold_sell or trader.close >= trader.hband:
            trader.sell_by_position_size()

    except Exception as e:
        print("An error occurred:", e)


if __name__ == '__main__':
    main()
