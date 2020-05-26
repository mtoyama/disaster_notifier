from context import monitors
import pytest
import time

@pytest.mark.parametrize("call_interval,call_range,expected_count", [
    (0.05, 10, 5), (0.05, 5, 5), (0.05, 4, 4), (0.2, 5, 5), (0.005, 100, 5),
    (0.05, 1, 1)
])
def test_rate_limiter(call_interval, call_range, expected_count):
    rate_limiter = monitors.RateLimiter(limit_frame=1, limit_count=5)

    @rate_limiter.limit_call_rate
    def dummy_func(test_arg, test_kwarg="test_kwarg"):
        return 1
    
    call_count = 0
    for i in range(call_range):
        addition = dummy_func("test_arg", test_kwarg="test_kwarg")
        if addition:
            call_count += addition
        time.sleep(call_interval)
    
    assert call_count == expected_count
    assert len(rate_limiter.tracking_dict["dummy_func"]) == expected_count
    time.sleep(1)
    addition = dummy_func("test_arg")
    if addition:
        call_count += addition
    if expected_count < 5:
        expected_count += 1
    assert call_count == expected_count
    assert len(rate_limiter.tracking_dict["dummy_func"]) == expected_count
