from enum import Enum
import logging
import inspect
import datetime
import os

LOGGER = logging.getLogger(__name__)

class DataSource:
    def __init__(self):
        self.status = Status.INITIALIZED
        self._last_get_dt = datetime.datetime.now() - datetime.timedelta(seconds=60)
        self._current_payload = {}
        self.filter_cache_path = os.path.join(
            os.getenv("HOME"),
            f"{self.__class__.__name__}_filter_cache.txt"
        )
        if os.path.exists(self.filter_cache_path):
            self._checked_ids = self.read_cached_filter_list()
        else:
            self._checked_ids = []

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
            if new_status == Status.GET_COMPLETED:
                self.last_get_dt = datetime.datetime.now()
            self._status = new_status

    def get_payload(self):
        LOGGER.info("Getting payload and resetting data source status")
        payload = self._current_payload
        self._current_payload = {}
        self.status = Status.INITIALIZED
        return payload
    
    def cache_filter_list(self):
        with open(self.filter_cache_path, 'w') as cache_file:
            LOGGER.info(f"Writing out {self._checked_ids} to cache!")
            cache_file.write('\n'.join(self._checked_ids))
    
    def read_cached_filter_list(self):
        LOGGER.info(f"Initializing checked ids from file {self.filter_cache_path}")
        with open(self.filter_cache_path, 'r') as cache_file:
            items = [item.rstrip() for item in cache_file]
        LOGGER.info(f"Adding the following items to the list: {items}")
        return items

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