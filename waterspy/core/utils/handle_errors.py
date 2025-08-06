from functools import wraps
from requests import RequestException


def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            print(response)
            return response
        except RequestException as e:
            # Assuming the timeseries is the second argument
            timeseries = args[1]
            print(f"Error: {e}")

            if e.response is not None:
                print(f"Response content: {e.response.content.decode()}")
            else:
                print("No response received from the request.")

            print(
                f"Skipping {timeseries.measurement_type} data from {timeseries.station} - {timeseries.logger}")
            # No return statement here means that when an exception is caught, this will return None

    return wrapper
