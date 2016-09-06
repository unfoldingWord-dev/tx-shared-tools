import requests

class NetworkFailure(Exception):
    """
    Raised to signal a network-level failure
    """
    def __init__(self, cause=None):
        self._cause = cause

    def __str__(self):
        return "Caused by: {}".format(str(self._cause))

    @property
    def cause(self):
        """
        The exception causing the network failure

        :type: Exception
        """
        return self._cause
