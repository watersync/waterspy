from waterspy.core.client import WatersyncClient, WatersyncRequest, WatersyncResponse
from waterspy.core.models import (LoggerMeasurement, GWLevelManualMeasurement,
                                     SampleTimeseries, SubirriTimeseries, Parameter, ParameterSample, Analyte, AnalysisSample)
from pandas import DataFrame
from functools import wraps
from typing import Optional, Literal
from waterspy.core.constants import API_ENDPOINTS


def get_options(client: WatersyncClient,
                target: str):
    """
    Fetches the list tables from the Watersync API.

    Args:
        client (WatersyncClient): The client to fetch data from.
        target (str): The target list to fetch.

    Returns:
        DataFrame: A DataFrame containing the fetched data.

    Note:
        The target parameter must be one of the following strings: 
        ['institutions', 'projects', 'units', 'meteo-stations', 'subirri-locations', 'wwtp-stations', 
        'piezometers', 'piezometer-materials', 'piezometer-construction-techniques', 'loggers', 'logger-models', 
        'logger-measurement-types', 'waterquality-parameters', 'waterquality-analytes', 'waterquality-methods']
    """
    endpoint = API_ENDPOINTS['lists'][target]

    request = WatersyncRequest(
        **client.model_dump(),
        endpoint=endpoint,
    )

    response = request.get()

    return DataFrame(response.content)


def get_samples(client: WatersyncClient,
                what: Literal['parameters', 'analytes'],
                sample_type: Literal['groundwater', 'wastewater', 'surfacewater'],
                stations: str | list[str] | None = None,
                timestamp_start: str | None = None,
                timestamp_end: str | None = None) -> SampleTimeseries:

    if what not in ['parameters', 'analytes']:
        raise ValueError(
            "Invalid value for 'what' parameter. Must be 'parameters' or 'analytes'")

    endpoint = 'waterquality/parametersamples/' if what == 'parameters' else 'waterquality/analyticalsamples/'

    if isinstance(stations, str):
        stations = [stations]

    params = {
        'stations': ','.join(stations) if stations else None,
        'timestamp_start': timestamp_start,
        'timestamp_end': timestamp_end,
        'sample_type': sample_type,
        'what': what,
    }

    params = {k: v for k, v in params.items() if v is not None}

    request = WatersyncRequest(
        **client.model_dump(),
        endpoint=endpoint,
        params=params
    )

    response = request.get()

    data = response.content

    def determine_models(what) -> tuple:
        return (Parameter, ParameterSample) if what == 'parameters' else (
            Analyte, AnalysisSample)

    def generate_analyte_objects(data: dict) -> list:
        measurements_data = data.pop('measurements', [])

        # Create measurement objects
        measurements = [models[0](**measurement)
                        for measurement in measurements_data]

        return measurements

    for sample in data:
        sample['station'] = sample.pop('content_object')

    models = determine_models(what)

    samples = []
    for sample in data:

        measurements = generate_analyte_objects(sample)

        sample_with_measurements = {**sample, 'measurements': measurements}

        samples.append(models[1](**sample_with_measurements))

    return SampleTimeseries(measurements=samples)


def fetch_timeseries(endpoint):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):

            if not kwargs.get('station') and not kwargs.get('logger'):
                raise Exception(
                    'At least station has to be provided. For logger records, a station, logger or combination of both can be provided.')

            params = {k: v for k, v in kwargs.items() if v is not None}

            request = WatersyncRequest(
                **params['client'].model_dump(),
                endpoint=endpoint,
                params=params
            )

            response = request.get()

            kwargs['response'] = response

            return func(*args, **kwargs)
        return inner
    return decorator


@fetch_timeseries(endpoint=API_ENDPOINTS['groundwater-manual-measurements'])
def get_manual_groundwater_levels(client: WatersyncClient,
                                  station: str,
                                  timestamp_start: Optional[str] = None,
                                  timestamp_end: Optional[str] = None,
                                  **kwargs) -> GWLevelManualMeasurement:
    """
    Fetches groundwater manual measurement data from the WatersyncClient API.

    Args:
        client (WatersyncClient): The client to fetch data from.
        station (str, optional): The station name to filter by. Defaults to None.
        timestamp_start (str, optional): The start date to filter by. Defaults to None.
        timestamp_end (str, optional): The end date to filter by. Defaults to None.

    Returns:
        GWLevelManualMeasurement: A GWLevelManualMeasurement object containing the fetched data.

    """

    response = kwargs.get('response')

    if not isinstance(response, WatersyncResponse):
        raise ValueError('Invalid response object')

    return GWLevelManualMeasurement(
        timeseries=response.timeseries,
        station=response.headers['X-Station'],
        toc_altitude=response.headers['X-TOCAltitude'],
        toc_height=response.headers['X-TOCHeight']
    )


@fetch_timeseries(endpoint=API_ENDPOINTS['groundwater-logger-measurements'])
def get_groundwater_logger(client: WatersyncClient,
                           station: str,
                           measurement_type: str,
                           timestamp_start: Optional[str] = None,
                           timestamp_end: Optional[str] = None,
                           **kwargs):
    """Fetches groundwater logger data from the API.

    Args:
        client (WatersyncClient): The client to fetch data from.
        station (str): The station name to filter by.
        measurement_type (str): The type of measurement to filter by.
        timestamp_start (str, optional): The start date to filter by. Defaults to None.
        timestamp_end (str, optional): The end date to filter by. Defaults to None.

    Returns:
        LoggerMeasurement: A LoggerMeasurement object containing the fetched data.
    """
    response = kwargs.get('response')

    if not isinstance(response, WatersyncResponse):
        raise ValueError('Invalid response object')
    if response.status_code == 200:

        return LoggerMeasurement(
            timeseries=response.timeseries,
            measurement_type=response.headers['X-MeasurementType'],
            unit=response.headers['X-Unit'],
            station=response.headers['X-Station'],
            logger=response.headers['X-Logger'],
            logger_alt=response.headers['X-LoggerAltitude']
        )
    else:
        return None


@fetch_timeseries(endpoint=API_ENDPOINTS['meteo-logger-measurements'])
def get_meteo_logger(client: WatersyncClient,
                     station: str,
                     measurement_type: str,
                     timestamp_start: Optional[str] = None,
                     timestamp_end: Optional[str] = None,
                     **kwargs):
    """Fetches meteo logger data from the API.

    Args:
        client (WatersyncClient): The client to fetch data from.
        station (str): The station name to filter by.
        measurement_type (str): The type of measurement to filter by.
        timestamp_start (str, optional): The start date to filter by. Defaults to None.
        timestamp_end (str, optional): The end date to filter by. Defaults to None.

    Returns:
        LoggerMeasurement: A LoggerMeasurement object containing the fetched data.
    """
    response = kwargs.get('response')
    if not isinstance(response, WatersyncResponse):
        raise ValueError('Invalid response object')

    return LoggerMeasurement(
        timeseries=response.timeseries,
        measurement_type=response.headers['X-MeasurementType'],
        unit=response.headers['X-Unit'],
        station=response.headers['X-Station'],
        logger=response.headers['X-Logger'],
    )


@fetch_timeseries(endpoint=API_ENDPOINTS['subirrigation-logger-records'])
def get_subirri_logger(client: WatersyncClient,
                       station: str,
                       logger: str,
                       measurement_type: str,
                       timestamp_start: Optional[str] = None,
                       timestamp_end: Optional[str] = None,
                       period: Optional[str] = None,
                       **kwargs):
    """Fetches subirri logger data from the API.

    Args:
        client (WatersyncClient): The client to fetch data from.
        station (str): The station name to filter by.
        measurement_type (str): The type of measurement to filter by.
        timestamp_start (str, optional): The start date to filter by. Defaults to None.
        timestamp_end (str, optional): The end date to filter by. Defaults to None.
        period (str, optional): The period to aggregate the data by. Defaults to None.

    Returns:
        SubirriTimeseries: A SubirriTimeseries object containing the fetched data.
    """
    response = kwargs.get('response')

    if not isinstance(response, WatersyncResponse):
        raise ValueError('Invalid response object')

    return SubirriTimeseries(
        timeseries=response.timeseries,
        measurement_type=measurement_type,
        unit='m3/h',
        subirri_location=station,
        logger=logger
    )
