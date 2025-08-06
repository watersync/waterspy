from waterspy.core.client import WatersyncClient


def delete_logger_records(client: WatersyncClient,
                          measurement_type: str,
                          station: str | None = None,
                          logger: str | None = None,
                          timestamp_start: str | None = None,
                          timestamp_end: str | None = None) -> None:
    """
    Deletes logger groundwater level measurements for the given filters.

    Parameters
    ----------
    client : WaterDataClient
        An instance of WaterDataClient used to make requests to the WaterSync API.
    logger : str
        The name of the logger to delete data for.
    measurement_type : str
        The type of measurement to delete. For options, run get_options(client, "logger-types").
    timestamp_start : str | None, optional
        The start date of the data to delete. If not provided, data from the beginning of time will be deleted.
    timestamp_end : str | None, optional
        The end date of the data to delete. If not provided, data up to the current date will be deleted.

    Raises
    ------
    Exception
        If the deletion operation fails.
    """

    if not station and not logger:
        raise Exception(
            'Either station, logger or combination of both have to be provided')

    params = {
        'logger': logger,
        'station': station,
        'measurement_type': measurement_type,
        'timestamp_start': timestamp_start,
        'timestamp_end': timestamp_end
    }

    params = {k: v for k, v in params.items() if v is not None}

    response = client.delete_data(
        endpoint='groundwater/loggerrecords/bulkdelete', params=params)

    print(response)
