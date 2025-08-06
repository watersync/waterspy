import pytest
import requests
from waterspy.core.client import WatersyncResponse, WatersyncRequest, WatersyncClient
from unittest.mock import patch


def test_watersync_response_status_code():
    mock_response = requests.Response()
    mock_response.status_code = 200
    ws_response = WatersyncResponse(response=mock_response)
    assert ws_response.status_code == 200


def test_watersync_response_fail_message():
    mock_response = requests.Response()
    mock_response.status_code = 404
    mock_response._content = b'Not Found'
    ws_response = WatersyncResponse(response=mock_response)
    assert ws_response.fail == 'Status 404: Not Found'
