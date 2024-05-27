import os
import datetime as dt
import time

from main import trading_logic_running


def _initial_capital_handler() -> float:
    while True:
        initial_capital = input("Please enter the initial capital")

        try:
            return float(initial_capital)

        except Exception as e:
            print(f"inappropriate initial capital, error occurred: {repr(e)}")


def _dry_run_handler() -> str:
    dry_run_answer = input('Do you want to process a dry run? (Y/N)\n'
                           '*** "dry" means to run the algo without actually buying or selling. ***')

    while dry_run_answer not in ('Y', 'N'):
        dry_run_answer = input("Please choose Y or N")

    return dry_run_answer


def _error_response_handler() -> bool:
    error_user_response = input("Do you want to continue? (Y/N)")

    while error_user_response not in ('Y', 'N'):
        error_user_response = input("Please choose Y or N")

    return error_user_response == 'Y'


def run() -> None:
    os.environ['API_KEY'] = input("Please enter your API KEY")
    os.environ['API_SECRET'] = input("Please enter your API SECRET")

    os.environ['DRY_RUN_USER_ANSWER'] = _dry_run_handler()
    initial_capital = _initial_capital_handler()

    continuing_user_response = True
    while continuing_user_response:

        now = dt.datetime.now()
        current_minute_in_hour = now.minute
        # run one minute after a new candle opened
        if current_minute_in_hour % 15 == 1:

            try:
                trading_logic_running(initial_capital=initial_capital)
                print(f"{dt.datetime.now()} - Finish Successfully!")
                # there is no reason to run the logic more than once a minute
                time.sleep(60)

            except Exception as e:
                print(f"an error occurred: {repr(e)}")

                continuing_user_response = _error_response_handler()


if __name__ == '__main__':
    run()
