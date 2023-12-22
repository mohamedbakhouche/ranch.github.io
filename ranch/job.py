"""Module describing a Job."""


class Job(object):
    default_email = ""

    def __init__(self, connection, data: dict) -> None:
        """_summary_
        
        
        
        :param connection: _description_
        :type connection: Connect
        :param data: _description_
        :type data: dict
        """
        self._connection = connection
        self._data = data

    def create(self) -> dict:
        """_summary_
        
        
        
        :return: _description_
        :rtype: dict
        """
        self._data["email"] = self._data.get("email", self.default_email)
        return self._connection._post("api/projects", self._data)
