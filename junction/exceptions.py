# -*- coding: utf-8 -*-


class BaseException(Exception):
    def __init__(self, error):
        Exception.__init__(self, error)
        if isinstance(error, dict):
            self.error = error
        else:
            self.error = None


class ClientException(BaseException):
    """Exception is raised when 4xx response is received from server.
    """


class ServerException(BaseException):
    """Exception is raised when the response status is 5xx from server.
    """


class ValidationException(BaseException):
    """Exception is raised when the received data didn't match the
    excepted structure.
    """
