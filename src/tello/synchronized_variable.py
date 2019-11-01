import threading


class SynchronizedVariable(object):

    def __init__(self, value, lock=None):
        super(SynchronizedVariable, self).__init__()
        self._value = value
        self._lock = lock if lock is not None else threading.Lock()

    @property
    def value(self):
        self._lock.acquire(blocking=True)
        try:
            value = self._value
        finally:
            self._lock.release()
        return value

    @value.setter
    def value(self, value):
        self._lock.acquire(blocking=True)
        try:
            self._value = value
        finally:
            self._lock.release()
