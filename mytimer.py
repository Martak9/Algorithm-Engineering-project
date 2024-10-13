from time import perf_counter


class MyTimer:
    _start: float
    _wpause: float
    _pause_sum: float


    def __new__(cls, time_func=perf_counter):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MyTimer, cls).__new__(cls)
            cls.instance._time_func = time_func
            cls.instance._start = time_func()
            cls.instance._pause_sum = 0
        return cls.instance

    def restart(self):
        self._start = self._time_func()
        self._pause_sum = 0

    def pause(self):
        self._wpause = self._time_func()

    def resume(self):
        self._pause_sum += self._time_func() - self._wpause

    def get_elapsed_time(self):
        return self._time_func() - self._start - self._pause_sum
