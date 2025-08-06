from waterspy.core.models import LoggerMeasurement
from gensor import read_from_csv as _load_from_csv
from pathlib import Path


def load_from_csv(path: Path) -> list[LoggerMeasurement]:

    return _load_from_csv(path=path,
                          file_format='vanessen')
