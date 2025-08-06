from waterspy.core.models import (Parameter, ParameterSample, SampleTimeseries,
                                     Analyte, AnalysisSample)
from pandas import DataFrame, to_datetime, NA
from typing import Tuple


def get_sampling_events(df: DataFrame,
                        what: str) -> DataFrame:
    """Returns a DataFrame with the sampling events, dropping duplicates and irrelevant columns."""

    # columns to drop from the sampling events (those that are only relevant to the measurements)
    PARAM_DROP_COLS = ['value', 'unit', 'parameter']
    ANALYSIS_DROP_COLS = ['value', 'unit', 'parameter']

    PARAM_DUPLICATE_COLS = ['station', 'timestamp', 'institution']
    ANALYSIS_DUPLICATE_COLS = ['station', 'timestamp', 'institution', 'method']

    # remove samples taken at the same time and place by the same institution
    sampling_events = df.drop_duplicates(subset=PARAM_DUPLICATE_COLS if what == 'parameters' else ANALYSIS_DUPLICATE_COLS)\
        .drop(columns=PARAM_DROP_COLS if what == 'parameters' else ANALYSIS_DROP_COLS)

    return sampling_events.reset_index(drop=True)


def match_sampling_events_to_measurement(df: DataFrame,
                                         what: str) -> Tuple[DataFrame, DataFrame]:
    """Matches the sampling events to the measurements, dropping irrelevant columns.
    Also converts the timestamp to a datetime object.
    """

    PARAM_DROP_COLS = ['timestamp', 'station', 'institution', 'comment']
    ANALYSIS_DROP_COLS = ['timestamp', 'station',
                          'institution', 'method', 'comment']

    df.loc[:, 'timestamp'] = to_datetime(df['timestamp']).dt.round('D')

    sampling_events = get_sampling_events(df, what).replace({NA: None})

    raw_measurements = df.drop(columns=['comment'])

    PARAM_MERGE_COLS = ['timestamp', 'station', 'institution']
    ANALYSIS_MERGE_COLS = ['timestamp', 'station', 'institution', 'method']

    measurements = raw_measurements.merge(sampling_events.reset_index(),
                                          on=PARAM_MERGE_COLS if what == 'parameters' else ANALYSIS_MERGE_COLS, how='left')\
        .drop(columns=PARAM_DROP_COLS if what == 'parameters' else ANALYSIS_DROP_COLS)

    return (sampling_events, measurements)


def generate_parameter_objects(sampling_events: DataFrame,
                               measurements: DataFrame, what: str) -> SampleTimeseries:
    samples = []
    for _, row in sampling_events.iterrows():

        models = (Parameter, ParameterSample) if what == 'parameters' else (
            Analyte, AnalysisSample)

        measurement_set = measurements[measurements['index'] == row.name]\
            .drop(columns='index')\
            .to_dict(orient='records')

        samples.append(models[1](**row.to_dict(),
                                measurements=[models[0](**measurement) for measurement in measurement_set]))  # type: ignore # noqa

    return SampleTimeseries(samples=samples)


def create_parameter_timeseries(df: DataFrame, what: str) -> SampleTimeseries:
    """Creates a timeseries of parameter or analysis measurements from a DataFrame."""
    if what not in ['parameters', 'analysis']:
        raise ValueError(f'Invalid parameter type: {what}')

    sampling_events, measurements = match_sampling_events_to_measurement(
        df, what)

    return generate_parameter_objects(sampling_events, measurements, what)
