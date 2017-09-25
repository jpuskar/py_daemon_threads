import threading
from queue import Queue
import time
import random


class HandlerJob(object):

    def __init__(self, message):
        self.message = message

    def __eq__(self, other):
        if self.message == other.message:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.message)


class SetQueue(Queue):

    def _init(self, maxsize):
        Queue._init(self, maxsize)
        self.all_items = set()

    def _put(self, item):
        if item not in self.all_items:
            Queue._put(self, item)
            self.all_items.add(item)

    def _get(self):
        item = Queue._get(self)
        if item in self.all_items:
            self.all_items.remove(item)
        return item


class QueueManager(object):

    def __init__(self):
        self._job_queue = SetQueue()
        self._jobs_in_progress = ()
        self._stop_all_workers = False
        self._threads = []

    def start(self):
        num_worker_threads = 4
        for i in range(num_worker_threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            self._threads.append(t)
        while not self._stop_all_workers:
            self._job_scan()
            time.sleep(1)

    def stop(self):
        self._stop_all_workers = True
        timeout = 10
        for thread in self._threads:
            i = 0
            while thread.isAlive() and i < timeout:
                time.sleep(0.5)
                i += 1

    def worker(self):
        while not self._stop_all_workers:
            # Wait for an item to work on
            job = self._job_queue.get(block=True)
            final_msg = str(threading.current_thread().getName()) + ": " + str(job.message)
            print(final_msg)
            time.sleep(random.randint(0, 7))

    def _safe_add_job(self, job):
        if job not in self._jobs_in_progress:
            self._job_queue.put(job)

    def _job_scan(self):
        for x in range(1, 10):
            message = 'message ' + str(x)
            job = HandlerJob(
                message=message,
            )
            self._safe_add_job(job)


qm = QueueManager()
qm.start()
time.sleep(10)
qm.stop()
