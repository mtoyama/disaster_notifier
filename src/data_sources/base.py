from enum import Enum
import logging
import inspect

LOGGER = logging.getLogger(__name__)

class DataSource:
    def __init__(self):
        self.status = Status.INITIALIZED
        self.get_data_sequence = []
        self.filter_data_sequence = []
        self._current_payload = {}

    def register_get_data_func(self, index):
        def decorator(func):
            step_dict = {
                "func": func,
                "async" : inspect.iscoroutinefunction(func)
            }
            self.get_data_sequence.insert(index, step_dict)
        return decorator

    def register_filter_data_func(self, index):
        def decorator(func):
            step_dict = {
                "func": func,
                "async" : inspect.iscoroutinefunction(func)
            }
            self.filter_data_sequence.insert(index, step_dict)
        return decorator

    @property
    def status(self):
        return self._status
    
    @property.setter
    def status(self, new_status):
        if isinstance(new_status, [Status, int]):
            raise TypeError(f"New status {new_status} is invalid type {new_status.__class__.__name__}")
        if new_status not in Status:
            raise ValueError(f"New status {new_status} not present in Status!")
        LOGGER.info(f"Updating {self.__class__.__name__} object to Status {new_status}")
        self._status = new_status

class Status(Enum):
    INITIALIZED = 1
    GET_COMPLETED = 2
    FILTER_COMPLETED = 3