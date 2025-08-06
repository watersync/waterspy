"""Module containing the API endpoints and validation functions."""

API_ENDPOINTS = {
    "login": "auth/token/login/",
    "groundwater-logger-measurements": "groundwater/loggerrecords/",
    "groundwater-manual-measurements": "groundwater/manualmeasurements/",
    "meteo-logger-measurements": "meteo/loggerrecords/",
    "subirrigation-logger-records": "subirri/loggerrecords/",
    "lists": {
        "institutions": "base/institutions/",
        "projects": "base/projects/",
        "units": "base/units/",
        "meteo-stations": "meteo/station/",
        "subirri-locations": "subirri/location/",
        "wwtp-stations": "wwtp/station/",
        "piezometers": "groundwater/piezometers/",
        "piezometer-materials": "groundwater/materials/",
        "piezometer-construction-techniques": "groundwater/techniques/",
        "loggers": "logger/loggers/",
        "logger-models": "logger/models/",
        "logger-measurement-types": "logger/measurementtypes/",
        "waterquality-parameters": "waterquality/parameters/",
        "waterquality-analytes": "waterquality/analytes/",
        "waterquality-methods": "waterquality/methods/"},
}
