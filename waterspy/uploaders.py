from waterspy.core.utils.handle_errors import handle_errors
from typing import Union
from pandas import Series, DataFrame, DatetimeIndex
from waterspy.core.client import WatersyncClient
from waterspy.core.models import SampleTimeseries, LoggerMeasurement, MeteoLoggerMeasurement, SampleTimeseries, SubirriTimeseries, GWLevelManualMeasurement
from datetime import datetime


def deploy_logger(client: WatersyncClient,
                  logger: str,
                  piezometer: str,
                  date_start: str,
                  measurement_types,
                  rope_len: float,
                  logger_alt: float | None = None,
                  comment: str | None = None):
    """
    Deploys a logger with the given parameters.

    Parameters
    ----------
    client : WatersyncClient
        The client used to interact with the backend.
    logger : str
        The identifier for the logger.
    piezometer : str
        The identifier for the piezometer.
    date_start : str
        The start date for the logger deployment.
    measurement_types : str or list
        A string or a list of measurement types.
    rope_len : float
        The length of the rope.
    logger_alt : float, optional
        The altitude of the logger.
    comment : str, optional
        Any additional comments.

    Returns
    -------
    dict
        A response from the server after deploying the logger.
    """

    # Convert measurement_types to a list if it is a string
    if isinstance(measurement_types, str):
        measurement_types = [measurement_types]

    # Building the data dictionary
    data = {
        'logger': logger,
        'piezometer': piezometer,
        'date_start': date_start,
        'measurement_types': measurement_types,
        'rope_len': rope_len,
        'logger_alt': logger_alt,
        'comment': comment
    }

    # Filter out None values
    data = {k: v for k, v in data.items() if v is not None}

    # Sending data to the client
    response = client.post_data(
        endpoint='groundwater/loggerdeployment', data=data)

    return response


def upload_logger(client: WatersyncClient,
                  serial_no: str,
                  type: str,
                  model: dict,
                  owner: list,
                  measurement_types: list,
                  comment: str,
                  available: bool):
    """
    Deploys a logger with the given parameters to the Django backend.

    Parameters
    ----------
    client : WatersyncClient
        The client used to interact with the backend.
    serial_no : str
        The serial number of the logger.
    type : str
        The type of the logger.
    model : dict
        The model information in a nested format.
    owner : list
        A list of owners.
    measurement_types : list
        A list of measurement types.
    comment : str
        Any additional comments.
    available : bool
        Availability status of the logger.

    Returns
    -------
    dict
        A response from the server after deploying the logger.
    """

    # Prepare the data payload
    data = [{
        "serial_no": serial_no,
        "type": type,
        "model": model,
        "owner": owner,
        "measurement_types": measurement_types,
        "comment": comment,
        "available": available
    }]

    response = client.post_data(endpoint='logger/logger', data=data)

    return response


@handle_errors
def upload_subirrigation_data(client: WatersyncClient,
                              timeseries: SubirriTimeseries) -> dict:
    """Load raw measurements data to the API."""

    params = {
        'station': timeseries.subirri_location,
        'logger': timeseries.logger,
        'measurement_type': timeseries.measurement_type,
        'unit': timeseries.unit
    }

    records = timeseries.timeseries.to_dict()

    print(f'Uploading subirrigation timeseries: {timeseries}')

    response = client.post_data(
        endpoint="subirri/measurement",
        data=[{'timestamp': k.isoformat(), 'value': v}
              for k, v in records.items() if isinstance(k, datetime)],
        params=params
    )

    if 'error' in response:
        print(f"Error uploading data: {response['error']}")

    return response


def upload_samples(client: WatersyncClient,
                   what: str,
                   timeseries: SampleTimeseries,
                   sample_type) -> dict:
    """Load raw measurements data to the API."""
    # structure objects to dictionary and match API

    print(f'Uploading parameters timeseries: {timeseries}')

    endpoint = "waterquality/parametersamples" if what == 'parameters' else "waterquality/analyticalsamples"

    data = timeseries.prepare_upload()

    response = client.post_data(
        endpoint=endpoint,
        data=data,
        params={'sample_type': sample_type}
    )

    if 'error' in response:
        print(f"Error uploading data: {response['error']}")

    return response


@handle_errors
def upload_manual_groundwater_levels(client: WatersyncClient, timeseries: GWLevelManualMeasurement) -> dict:

    if isinstance(timeseries.timeseries, Series):
        # make sure the index is a datetime object
        timeseries.timeseries.index = DatetimeIndex(
            timeseries.timeseries.index)

        data = [{'timestamp': k.isoformat(),
                 'depth': v,
                 'station': timeseries.piezometer,
                 }
                for k, v in timeseries.timeseries.items() if isinstance(k, datetime)]

    elif isinstance(timeseries.timeseries, DataFrame):
        # make sure the timestamp is a datetime object
        timeseries.timeseries['timestamp'] = timeseries.timeseries['timestamp'].apply(
            lambda x: x if isinstance(x, datetime) else datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

        data = [{'timestamp': row['timestamp'].isoformat(),
                 'depth': row['depth'],
                 'comment': row['comment'],
                 'station': timeseries.piezometer,
                 } for index, row in timeseries.timeseries.iterrows()]
    else:
        raise ValueError("Invalid timeseries type")

    response = client.post_data(
        endpoint="groundwater/manualmeasurements",
        data=data
    )

    return response
