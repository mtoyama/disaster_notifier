from enum import Enum
import logging
import inspect

LOGGER = logging.getLogger(__name__)

class DataSource:
    def __init__(self):
        self.status = Status.INITIALIZED
        self._current_payload = {}
        self.get_data_sequence = []
        self.filter_data_sequence = []

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
            LOGGER.info(f"Updating {self.__class__.__name__} object to {new_status}")
            self._status = new_status

    def get_payload(self):
        payload = self._current_payload
        self._current_payload = {}
        return payload

    @staticmethod
    def add_method_to_register(method, list, index):
        if "triggers" in inspect.getfullargspec(method)[0]:
            triggers_present = True
        else:
            triggers_present = False

        step_dict = {
            "func": method,
            "triggers": triggers_present,
            "async": inspect.iscoroutinefunction(method)
        }
        LOGGER.info(f"Registering method: {step_dict}")
        list.insert(index, step_dict)

class Status(Enum):
    INITIALIZED = 1
    GET_COMPLETED = 2
    FILTER_COMPLETED = 3