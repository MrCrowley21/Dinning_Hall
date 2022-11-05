from Components_logic.Dinning_hall import *
from threading import Lock


class RatingSystem:
    def __init__(self):
        self.lock = Lock()
        self.marks = []

    def get_mark(self, preparing_time, max_wait):
        if preparing_time < max_wait:
            mark = 5
        elif preparing_time < 1.1 * max_wait:
            mark = 4
        elif preparing_time < 1.2 * max_wait:
            mark = 3
        elif preparing_time < 1.3 * max_wait:
            mark = 2
        elif preparing_time < 1.4 * max_wait:
            mark = 1
        else:
            mark = 0
        self.lock.acquire()
        self.marks.append(mark)
        self.lock.release()
        return mark

    def add_mark(self, mark):
        self.lock.acquire()
        self.marks.append(mark)
        self.lock.release()

    def compute_average_mark(self):
        if len(self.marks) > 0:
            return sum(self.marks) / len(self.marks)
        else:
            return 0
