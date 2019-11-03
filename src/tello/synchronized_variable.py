import threading


class SynchronizedVariable(object):
    """
    Object (variable) with a thread-safe getter and setter of its `value`.

    Args:
        value(obj): Initial value to which the internal variable is set
        lock(threading.Lock): Lock of the variable (optional)
    """

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
