import os
import datetime as dt

from main import trading_logic_running


def run() -> None:
    os.environ['API_KEY'] = input("Please enter your API KEY")
    os.environ['API_SECRET'] = input("Please enter your API SECRET")

    continuing_user_response = True
    while continuing_user_response:

        now = dt.datetime.now()
        current_minute_in_hour = now.minute
        # run one minute after a new candle opened
        if current_minute_in_hour % 15 == 1:

            try:
                trading_logic_running()
                print(f"{dt.datetime.now()} - Finish Successfully!")

            except Exception as e:
                print(f"an error occurred: {repr(e)}")

                error_user_response = input("Do you want to continue? (Y/N)")
                while error_user_response not in ('Y', 'N'):
                    error_user_response = input("Please choose Y or N")

                if error_user_response == 'N':
                    continuing_user_response = False


if __name__ == '__main__':
    run()
