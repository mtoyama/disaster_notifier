import logging
import datetime
import functools

LOGGER = logging.getLogger(__name__)

def log_run_duration(func):
    @functools.wraps(func)
    def wrapper_log_timing(*args, **kwargs):
        timing_start = datetime.datetime.now()
        result = func(*args, **kwargs)
        timing_duration = datetime.datetime.now() - timing_start
        timing_duration_s = timing_duration.total_seconds()
        LOGGER.info(f"Total duration for func {func.__name__}: {timing_duration_s}s")
        return result
    return wrapper_log_timing