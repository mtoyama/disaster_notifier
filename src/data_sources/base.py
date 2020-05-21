from enum import Enum
import logging
import inspect

LOGGER = logging.getLogger(__name__)

class DataSource:
    def __init__(self):
        self.status = Status.INITIALIZED
        self._current_payload = {}

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, new_status):
        if not isinstance(new_status, (Status, int)):
            raise TypeError(f"New status {new_status} is invalid type {new_status.__class__.__name__}")
        elif new_status not in Status:
            raise ValueError(f"New status {new_status} not present in Status!")
        else:
            LOGGER.info(f"Updating {self.__class__.__name__} object to Status {new_status}")
            self._status = new_status

class Status(Enum):
    INITIALIZED = 1
    GET_COMPLETED = 2
    FILTER_COMPLETED = 3