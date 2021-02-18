import time
from collections import deque

inf = float("inf")


class _meter:

    __begin__ = 0
    __end__ = 0
    __size__ = 60
    __store__ = deque([0.0] * __size__, maxlen=__size__)
    name = ""

    @classmethod
    def _begin(cls):
        cls.__begin__ = time.perf_counter()#/1000000#time_ns()

    @classmethod
    def _end(cls):
        cls.__end__ = time.perf_counter()#/1000000#time_ns()
        cls.__store__.append(cls.speed())

    @classmethod
    def _noop(cls):
        pass

    @classmethod
    def enable(cls):
        cls.begin = cls._begin
        cls.end = cls._end

    @classmethod
    def disable(cls):
        cls.begin = cls._noop
        cls.end = cls._noop

    @classmethod
    def diff(cls):
        return cls.__end__ - cls.__begin__

    @classmethod
    def speed(cls):
        d = cls.diff()
        if d <= 0.0:
            return 0.0
        if d == inf:
            return inf
        return 1 / d

    @classmethod
    def smooth_speed(cls):
        return sum(cls.__store__) / cls.__size__

    begin = _begin
    end = _end


# Public counters
__tracked_meters = {}

# Public functions
def enable_perf():
    ...


def disable_perf():
    ...


def get_meter(meter_name):
    meter = __tracked_meters.get(meter_name, None)
    if meter is not None:
        return meter

    tmp = type(
        meter_name,
        (_meter,),
        {
            "name": meter_name,
            "__begin__": 0,
            "__end__": 0,
            "__size__": 60,
            "__store__": deque([0.0] * 60, maxlen=60),
        },
    )
    __tracked_meters[meter_name] = tmp
    return tmp


__tracked_meters = {}


__all__ = [
    "enable_perf",
    "disable_perf",
    "get_meter",
]
