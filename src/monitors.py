import functools
import datetime
import logging
LOGGER = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, limit_frame, limit_count):
        self.limit_frame = limit_frame
        self.limit_count = limit_count
        self.tracking_dict = {}

    def limit_call_rate(self, func):
        @functools.wraps(func)
        def wrapper_limit_call_rate(*args, **kwargs):
            if func.__name__ not in self.tracking_dict:
                self.tracking_dict[func.__name__] = []
            call_list = self.tracking_dict[func.__name__]
            current_time = datetime.datetime.now()
            if len(call_list) < self.limit_count:
                self.add_call_to_call_list(call_list, current_time)
                return func(*args, **kwargs)
            elif self.is_within_limit_frame(call_list, current_time) is True:
                LOGGER.error(f"Rate limiter reached for func {func.__name__}!")
                LOGGER.error(f"SKIPPING CALL. Args: {args, kwargs}")
                self.add_call_to_call_list(call_list, current_time)
        return wrapper_limit_call_rate
    
    def is_within_limit_frame(self, call_list, current_time):
        duration = current_time - call_list[0]
        duration_s = duration.total_seconds()
        if duration_s < self.limit_frame:
            return True
        else:
            return False
    
    def add_call_to_call_list(self, call_list, call_dt):
        if len(call_list) < self.limit_count:
            call_list.append(call_dt)
        elif len(call_list) > self.limit_count:
            call_list.append(call_dt)
            del call_list[0]


