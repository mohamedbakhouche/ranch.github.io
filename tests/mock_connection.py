class PostRequest:
    def __init__(self, url, body):
        self._url = url
        self._body = body


class MockResponse:
    def __init__(self, status_code: int, data: dict = None) -> None:
        self.status_code = status_code
        self._json = data

    def json(self) -> dict:
        return self._json


class MockConnection:
    def __init__(self) -> None:
        pass

    def _post(self, url: str, data: dict) -> dict:
        return MockResponse(200)
