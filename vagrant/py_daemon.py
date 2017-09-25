import daemon
import signal
import time
# import lockfile


class TestDaemon(object):

    def __init__(self):
        self.stopped = False

    def stop_tasks(self):
        self.stopped = True

    def run(self):
        i = 0
        logfile = open('/root/py_daemon.log', 'a')
        logfile.writelines("Starting run.\n")
        while self.stopped is False:  # or i < 3:
            logfile.writelines("run " + str(i) + "\n")
            i = i + 1
            time.sleep(1)
        logfile.writelines("exited cleanly at " + str(i) + "\n")
        logfile.close()


td = TestDaemon()


def program_cleanup(signum, frame):
    td.stop_tasks()


context = daemon.DaemonContext()
context.signal_map = {
    signal.SIGTERM: program_cleanup,
}

with context:
    td.run()
