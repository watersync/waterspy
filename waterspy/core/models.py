"""Models getting basic data from WaterSync API."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Literal
from gensor.core.timeseries import Timeseries as GWLTimeseries
from gensor.core.dataset import Dataset as GWLDataset
from waterspy.core.client import WatersyncClient, WatersyncRequest
from waterspy.core.utils.handle_errors import handle_errors
from pydantic import BaseModel, field_serializer, field_validator
from shapely.geometry import Point, mapping
from waterspy.core.waterquality.models import *


class Option(BaseModel):
    target: str
    object: dict

    OPTIONS: dict = {
        'units': {"endpoint": 'base/units', "fields": ["unit"]},
        'analytes': {"endpoint": 'waterquality/analytes', "fields": ["analyte", "detail"]},
        'parameters': {"endpoint": 'waterquality/parameters', "fields": ["parameter"]},
        'analytical-techniques': {"endpoint": 'waterquality/techniques', "fields": ["technique", "detail"]},
        'methods': {"endpoint": 'waterquality/methods', "fields": ["method", "detail"]},
        'institutions': {"endpoint": 'base/institutions', "fields": ["institution"]},
        'piezometer-materials': {"endpoint": 'groundwater/materials', "fields": ["material"]},
        'drilling-techniques': {"endpoint": 'groundwater/techniques', "fields": ["technique"]},
        'logger-models': {"endpoint": 'logger/models', "fields": ["model", 'manufacturer']},
        'logger-measurement-types': {"endpoint": 'logger/measurementtypes', "fields": ["measurement_type"]},
        'waterquality-parameters': {"endpoint": 'waterquality/parameters', "fields": ["parameter"]},
        'waterquality-analytes': {"endpoint": 'waterquality/analytes', "fields": ["analyte"]},
        'waterquality-methods': {"endpoint": 'waterquality/methods', "fields": ["method"]},
    }

    def upload(self,
               target: str,
               client: WatersyncClient):

        endpoint_info = self.OPTIONS.get(target)

        if not endpoint_info:
            return {"error": "Invalid target specified"}

        request = WatersyncRequest(
            **client.model_dump(),
            endpoint=endpoint_info['endpoint'],
            data=self.object
        )

        print(f'Option {self.object} saved!')

        response = request.post()

        print(response)

        # if 'error' in response:
        #     print(f"Error uploading data: {response['error']}")

        return response


class Project(BaseModel):

    name: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_active: Optional[str] = None

    @handle_errors
    def upload(self,
               client: WatersyncClient):

        endpoint = 'base/projects'

        request = WatersyncRequest(
            **client.model_dump(),
            endpoint=endpoint,
            data=self.model_dump(exclude_none=True)
        )

        print(f'Project {self.name} saved!')

        response = request.post()

        print(response)

        # if 'error' in response:
        #     print(f"Error uploading data: {response['error']}")

        return response


class StationDetail(BaseModel):

    total_len: Optional[float] = None
    height: Optional[float] = None
    depth_mbgl: Optional[float] = None
    filter_bottom: Optional[float] = None
    filter_top: Optional[float] = None
    diameter: Optional[float] = None
    material: Optional[str] = None
    technique: Optional[str] = None

    @field_validator('total_len', 'height', 'depth_mbgl', 'filter_bottom', 'filter_top', 'diameter')
    @classmethod
    def round_float(cls, v: float) -> float:
        if v is not None:
            return round(v, 2)
        return v


class Station(BaseModel):

    class Config:
        arbitrary_types_allowed = True

    name: str
    type: Literal['surfacewater', 'groundwater',
                  'meteorological', 'wastewater', 'other']
    geom: Point
    altitude: float
    description: Optional[str] = None
    institution: Optional[str] = None
    detail: Optional[StationDetail] = None

    @field_serializer('geom')
    def serialize_geom(self, value):
        geom_mapping = mapping(value)

        if 'coordinates' in geom_mapping:
            geom_mapping['coordinates'] = list(geom_mapping['coordinates'])
        return geom_mapping

    def upload(self,
               client: WatersyncClient):

        endpoint = 'base/station'

        request = WatersyncRequest(
            **client.model_dump(),
            endpoint=endpoint,
            data=self.model_dump(exclude_none=True)
        )

        print(f'Station {self.name} saved!')

        response = request.post()

        print(response.content)

        return response


class Logger(BaseModel):
    identifier: str
    available: Optional[bool] = None
    owner: Optional[list] = None
    measurement_type: Optional[list] = None
    model: Optional[dict] = None
    comment: Optional[str] = None

    def upload(self,
               client: WatersyncClient):

        endpoint = 'logger/loggers'

        request = WatersyncRequest(
            **client.model_dump(),
            endpoint=endpoint,
            data=[self.model_dump(exclude_none=True)]
        )

        print(f'Logger with sn {self.identifier} saved!')

        response = request.post()

        print(response.content)

        return response


class LoggerDeployment(BaseModel):
    logger: str
    station: str
    deployed_at: Optional[str] = None
    decommissioned_at: Optional[str] = None
    measurement_type: Optional[list] = None
    iot: Optional[bool] = None
    logger_altitude: Optional[float] = None
    comment: Optional[str] = None

    def upload(self,
               client: WatersyncClient):

        endpoint = 'logger/loggers'

        request = WatersyncRequest(
            **client.model_dump(),
            endpoint=endpoint,
            data=[self.model_dump(exclude_none=True)]
        )

        print(f'Logger with sn {self.identifier} saved!')

        response = request.post()

        print(response.content)

        return response


class LoggerDataset(GWLDataset):
    """Class to store a collection of timeseries.

    The Dataset class is used to store a collection of Timeseries objects. It is meant to be created when the van Essen CSV file is parsed.

    Attributes:
        timeseries (list[Timeseries]): A list of Timeseries objects.

    Methods:
        align: Aligns the timeseries to a common time axis.
        plot: Plots the timeseries data.
    """


@dataclass
class Timeseries:
    """Base class for all timeseries data.

    The timeseries argument should be filled with a pd.Dataframe containig timestamp and value columns.
    """

    timeseries: Series


@dataclass
class GWLevelManualMeasurement(Timeseries):
    """
    Stores the manual groundwater level measurements. The main timeseries represents the groundwater levels measured
    from the top of casing (TOC) to the groundwater level.

    Attributes:
        station (str): The station name.
        toc_altitude (float): The altitude of the top of casing (TOC).
        toc_height (float): The height of the top of casing (TOC) above the ground.

    Properties:
        groundwater_depth (Series): The groundwater depth.
        groundwater_elevation (Series): The groundwater elevation.

    Note:
        The API and this particular function will have to change eventually to account for cases when the TOC is not
        constant.
    """

    station: str
    toc_altitude: float
    toc_height: float

    def __repr__(self):
        return self.station

    @property
    def groundwater_depth(self) -> Series:
        return self.timeseries.sub(self.toc_height)

    @property
    def groundwater_elevation(self) -> Series:
        return self.timeseries.sub(self.toc_altitude)


@dataclass
class MeteoLoggerMeasurement(GWLTimeseries):
    """Subclass of Timeseries for meteo data.
    """


@dataclass
class LoggerMeasurement(GWLTimeseries):
    """Subclass of PiezometerTimeseries for logger data.

    The reason why this is separated from the logger is that the manula measurement also need to be stored
    somewhere, and they are not associated with a logger.
    """

    logger_alt: Optional[float] = None

    @handle_errors
    def upload(self,
               client: WatersyncClient):

        params = {
            'station': self.station,
            'logger': self.logger,
            'measurement_type': self.measurement_type,
            'unit': self.unit
        }

        endpoint = 'meteo/loggerrecords' if self.barometric else 'groundwater/loggerrecords'

        request = WatersyncRequest(
            **client.model_dump(),
            endpoint=endpoint,
            params=params,
            data=self.ts_to_dict()
        )

        print(f'Uploading timeseries: {self}')

        response = request.post()

        print(response)

        # if 'error' in response:
        #     print(f"Error uploading data: {response['error']}")

        return response


@dataclass
class SubirriTimeseries(Timeseries):
    """Subclass of Timeseries for Subirri data.
    """
    measurement_type: str
    logger: str
    subirri_location: str
    unit: str

    def __repr__(self):
        return f"{self.measurement_type} at {self.subirri_location}"
