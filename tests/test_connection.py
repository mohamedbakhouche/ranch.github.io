import os

import pytest
import requests
from dotenv import load_dotenv

from ranch import connection
from .mock_connection import MockConnection

# from .mock_job import data

# renderer id
# https://www.ranchcomputing.com/api/ranchtools/ranchecker/cinema4d.json
# priority
# "cpu": "https://www.ranchcomputing.com/api/ranchtools/farms/cpu.json",
# "gpu": "https://www.ranchcomputing.com/api/ranchtools/farms/gpu.json"

load_dotenv()

# RANCH_API_KEY = os.environ["RANCH_API_KEY"]
RANCH_API_KEY = os.getenv("RANCH_API_KEY")


class TestConnection:
    def setup_method(self, method):
        self.conn = connection.Connect(RANCH_API_KEY)
        self.mock_conn = MockConnection()

    def teardown_method(self, method):
        del self.conn

    def test_mock_connection(self):
        res = self.mock_conn._post("ranchcomputing.com", {})
        assert res.status_code == 200

    def test_connection_empty_api_key(self):
        assert self.conn.api_key != ""

    def test_connection_unauthorize_message(self, data):
        self.conn._api_key = "key"
        res = self.conn.create_job(data=data)
        assert res.json() == {"message": "wrong X-Auth-Token"}

    def _test_connection_unauthorize_status(self, data):
        self.conn._api_key = "key"
        res = self.conn.create_job(data=data)
        assert res.status_code == 401

    def test_create_job(self, data):
        res = self.conn.create_job(data=data)
        assert res.status_code == 200

    def test_submit_job(self):
        archive_path = "C:\\Users\\mohbakh\\Pictures\\car\\sdk.vuc"
        res = self.conn.submit(archive_path, "sdk", 598, 13)
        # assert res.status_code == 200

    def _test_connection_upload(self):
        self.conn.upload()
        # assert res.status_code == 401

    def _test_create_job_status_code(self, data):
        res = self.conn.create_job(data=data)
        assert res.status_code == 200

    def _test_create_job_success(self, data):
        res = self.conn.create_job(datat=data)
        assert res.json().get("success") == True
