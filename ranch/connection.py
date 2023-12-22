"""Module describing a connection."""
import os
from ranch.exceptions import RanchException
from ranch.uploadJob import UploadJob
from ranch.job import Job
from ._retry import retry
import requests
from requests.adapters import HTTPAdapter


SWEB_URL = "https://www.ranchcomputing.com/"
TIME_OUT = 5  # TODO add time out to the env variable


class Connect(object):
    
    # DEFAULT_MAIL = ""

    def __init__(self, api_key: str) -> None:
        """_summary_



        :param api_key: _description_
        :type api_key: str
        """
        self.api_key = api_key.strip()
        self._session = requests.session()

    @property
    def _api_key(self) -> str:
        """_summary_



        :return: _description_
        :rtype: str
        """
        return self.api_key

    @_api_key.setter
    def _api_key(self, api_key: str) -> None:
        """_summary_



        :param api_key: _description_
        :type api_key: str
        """
        self.api_key = api_key.strip()

    def _set_header(self, api_key: str) -> dict:
        """_summary_



        :return: _description_
        :rtype: dict
        """
        headers = {"x-auth-token": api_key, "Content-type": "application/json", "Accept": "application/json"}
        return headers

    def _create_job(self, data: dict) -> dict:
        return Job(self, data=data).create()

    # @retry
    def _post(self, url: str, data: dict) -> dict:
        """_summary_



        :param url: _description_
        :type url: str
        :param data: _description_
        :type data: dict
        """
        _url = SWEB_URL + url
        # self._session.mount(SWEB_URL, HTTPAdapter(max_retries=50))
        headers = self._set_header(self._api_key)
        self._session.headers.update(headers)
        try:
            return self._session.post(_url, headers=headers, json=data, timeout=TIME_OUT)
        except requests.ConnectionError as e:
            raise RanchException("Internet connection check failed")

    def submit(self, archive_path: str, job_name: str, renderer_id: int, priority_id: int) -> bool:
        job_name_extension = os.path.splitext(os.path.basename(archive_path))[1]
        job_name_ext = job_name + job_name_extension

        data = {"disclaimer": True, "email": "flouguet@wanadoo.fr"}
        data["renderer_id"] = renderer_id
        data["priority_id"] = priority_id

        if not os.path.exists(archive_path):
            # TODO
            return False
        response = self._create_job(data)
        if not response.json().get("success"):
            # TODO
            return False

        metadata = response.json().get("metadata")
        metadata["uploader_name"] = "racnhcomputing python SDK"
        metadata["uploader_version"] = "2.0.0"
        metadata["filename"] = job_name_ext

        tuspload = response.json().get("tuspload")
        upload = UploadJob(
            endpoint=tuspload["endpoint"],
            chunk_size=tuspload.get("chunkSize", None),
            file_path=archive_path,
            metadata=metadata,
        )
        upload.run()
        return True

    def _call_api(self, url: str, request) -> dict:
        pass
