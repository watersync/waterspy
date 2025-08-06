"""Models getting basic data from WaterSync API."""
from __future__ import annotations
from ast import Param
from pandas import Series, DataFrame, concat, Timestamp
from waterspy.core.client import WatersyncClient, WatersyncRequest
from typing import Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, model_validator
from itertools import product
from waterspy.core.fields import AnalysisResult


class Measurement(BaseModel):
    """Base class for measurements."""
    value: float
    unit: str


class Parameter(Measurement):
    """Measurements of a parameter in water quality data.

    Example of a parameter is pH, temperature, etc. If are to be uploaded to the WaterSync API, the parameter must be in
    your defined parameter list.

    Attributes:
        value (float): The value of the parameter.
    """
    parameter: str


class Analyte(Measurement):
    """Measurements of an analyte in water quality data.

    Example of an analyte is nitrate, phosphate, etc. If are to be uploaded to the WaterSync API, the analyte must be
    in your defined analyte list.

    Attributes:
        value (float): The value of the analyte.
    """
    value: AnalysisResult
    parameter: str = Field(serialization_alias='analyte')

    @model_validator(mode='before')
    def convert_unit(cls, values: Any) -> Any:
        value = values.get('value')
        unit = values.get('unit')

        if unit in ['μg/L', 'µg/L']:
            # Convert from µg/L to mg/L
            values['value'] = value / 1000.0
            values['unit'] = 'mg/L'

        # Conversion for alkalinity from µM to mg/L HCO3-
        if values.get('parameter') == 'Alkalinity':
            values['value'] = cls.alkalinity_to_hco3(value)
            values['parameter'] = 'HCO3'
            values['unit'] = 'mg/L'

        return values

    @staticmethod
    def alkalinity_to_hco3(alkalinity_mM: float) -> float:
        """
        Convert alkalinity from µM to HCO3- concentration in mg/L.

        :param alkalinity_uM: Alkalinity in µM (micro moles per liter)
        :return: HCO3- concentration in mg/L
        """
        # Molecular weight of HCO3- in g/mol
        molecular_weight_HCO3 = 61.0  # g/mol

        # Convert µM to mg/L
        hco3_mg_per_L = alkalinity_mM * molecular_weight_HCO3  # µM to mg/L conversion

        return hco3_mg_per_L


class Sample(BaseModel):
    """Sample base model for water quality data.

    Attributes:
        station (str): The station where the sample was taken.
        timestamp (datetime): The timestamp of the sample collection.
        institution (str, optional): The institution that took the sample.
        measurements (list): The measurements taken.
        comment (str, optional): A comment on the sample.

    Methods:
        filter_measurements: Filter the measurements by parameter.    
    """
    station: str
    timestamp: datetime
    institution: Optional[str] = None
    measurements: list
    comment: Optional[str] = None

    def filter_measurements(self, parameters: str | list) -> Sample | None:
        """Pop the measurements for the given parameters.

        Args:
            parameters (str | list): The parameters to select from the measurements.
            inplace (bool): Whether to filter the measurements in place.

        Returns:
            sample: A new Sample object with only the filtered measurements.
        """

        if not isinstance(parameters, list):
            parameters = [parameters]

        filtered_measurements = [
            param for param in self.measurements if param.parameter in parameters]

        if not filtered_measurements:
            return None
        else:
            return Sample(
                station=self.station,
                timestamp=self.timestamp,
                institution=self.institution,
                measurements=filtered_measurements,
                comment=self.comment
            )


class SampleTimeseries(BaseModel):
    """A timeseries of water quality samples.

    Contains a list of samples and provides methods to filter the samples and create timeseries. It is also the
    class used for plotting the data.

    Attributes:
        samples (list): A list of samples.

    Methods:
        filter_samples: Filter the samples based on the given criteria.
        create_ts: Create a timeseries of the measurements for a given parameter and station.
        timeseries_list: Creates a list of pd.Series for a given parameter and list of stations.
        wide_ts: Stack the timeseries into a single DataFrame.
        long_ts: Stack the timeseries into a long form DataFrame.

    Properties:
        unique_stations: Get the unique stations in the sample timeseries.
        unique_parameters: Get the unique parameters in the sample timeseries.
        statistics: Get the statistics of the measurements in the sample timeseries.
    """

    class Config:
        arbitrary_types_allowed = True

    samples: List[Sample]

    @property
    def unique_stations(self) -> List[str]:
        return list(set([sample.station for sample in self.samples]))

    @property
    def unique_parameters(self) -> List[str]:
        return list(set([param.parameter for sample in self.samples for param in sample.measurements]))

    @property
    def statistics(self) -> DataFrame:
        """Get the statistics of the measurements in the sample timeseries.

        Returns:
            DataFrame: The statistics of the measurements.
        """

        long_ts = self.long_ts()
        grouped = long_ts.groupby(level=['station', 'parameter'])

        stats = grouped.agg(
            ['mean', 'std', 'min', 'max', 'count', 'median'])

        return stats

    def __repr__(self):
        return f'SampleTimeseries({len(self.samples)})'

    def __getitem__(self, idx: int) -> Sample:
        return self.samples[idx]

    def _return_type(self):
        return type(self.samples[0])

    def filter_samples(self,
                       stations: Optional[str | list] = None,
                       parameters: Optional[str | list] = None,
                       institutions: Optional[str | list] = None,
                       start: Optional[datetime | None] = None,
                       end: Optional[datetime | None] = None) -> SampleTimeseries:
        """Filter the samples based on the given criteria.

        Args:
            stations Optional(str | list): The station(s) to filter by.
            parameters Optional(str | list): The parameter(s) to filter by.
            institutions Optional(str | list): The institution(s) to filter by.
            start Optional(datetime): The start date to filter by.
            end Optional(datetime): The end date to filter by.
        """

        if isinstance(stations, str):
            stations = [stations]
        if isinstance(institutions, str):
            institutions = [institutions]
        if isinstance(parameters, str):
            parameters = [parameters]
        if start and not isinstance(start, datetime):
            start = Timestamp(start)
        if end and not isinstance(end, datetime):
            end = Timestamp(end)

        def sample_matches(sample: Sample) -> bool:
            if stations is not None and sample.station not in stations:
                return False
            if institutions is not None and sample.institution not in institutions:
                return False
            if start is not None and sample.timestamp < start:
                return False
            if end is not None and sample.timestamp > end:
                return False
            return True

        filtered_samples = [
            sample for sample in self.samples if sample_matches(sample)]

        if parameters:
            filtered_samples = [
                sample.filter_measurements(parameters) for sample in filtered_samples if sample.filter_measurements(parameters) is not None]

        if not filtered_samples:
            raise ValueError('No samples found for the given criteria.')

        return SampleTimeseries(samples=filtered_samples)  # type: ignore

    def create_ts(self, parameter: str, station: str) -> Series:
        """Create a timeseries of the measurements for a given parameter and station.

        Args:
            parameter (str): The parameter to create the timeseries for.
            station (str): The station to create the timeseries for.

        Returns:
            Series: The timeseries of the measurements.
        """

        extracted_measurements = []
        for item in self.samples:

            extracted_measurements.extend([{item.timestamp: param.value}
                                           for param in item.measurements if param.parameter == parameter and item.station == station])

        # Flatten the list of dictionaries into a single dictionary
        data = {list(d.keys())[0]: list(d.values())[0]
                for d in extracted_measurements}

        ts = Series(data, name=f'{station}-{parameter}')

        return ts.sort_index()

    def timeseries_list(self) -> list:
        """Creates a list of pd.Series for a given parameter and list of stations.

        Returns:
            list: A list of pd.Series for all combinations of stations and 
            parameters in the sample timeseries.
        """

        options = list(product(self.unique_parameters, self.unique_stations))
        return [self.create_ts(*item) for item in options]

    def wide_ts(self) -> DataFrame:
        """Stack the timeseries into a single DataFrame.

        Returns:
            wide_df: The wide dataframe of the timeseries.
        """

        ts_list = self.timeseries_list()

        wide_df = concat(ts_list, axis=1)

        return wide_df

    def long_ts(self) -> DataFrame:
        """Stack the timeseries into a long form DataFrame"""

        ts_list = self.timeseries_list()
        keys = [tuple(ts.name.split('-')) for ts in ts_list]
        long_df = concat(ts_list, axis=0, keys=keys, names=[
                         'station', 'parameter', 'timestamp'])

        return long_df

    def upload(self,
               client: WatersyncClient):

        endpoint = 'waterquality/parametersamples' if self._return_type(
        ) == ParameterSample else 'waterquality/analyticalsamples'

        request = WatersyncRequest(
            **client.model_dump(),
            endpoint=endpoint,
            data=self.model_dump(exclude_none=True, mode='json')['samples']
        )

        response = request.post()

        print(response)

        return response


class ParameterSample(Sample):

    def __repr__(self):
        return f'ParameterSample({self.station}, {self.timestamp})'


class AnalysisSample(Sample):

    method: str
