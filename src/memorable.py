import functools
import tracemalloc
import threading
import time

class Memorable:
    def __init__(self, max_snapshots=10, snapshot_interval=10):
        self.max_snapshots = max_snapshots
        self.snapshot_interval = snapshot_interval
        self.snapshots = []

        self.lock = threading.Lock()
        self.bg_thread = threading.Thread(target=self.background_run, daemon=True)
        self.bg_thread.start()

    def process_leaks(self, leaks):
        for leak in leaks:
            traceback = tracemalloc.Traceback(leak.traceback)
            frame = traceback[0]
            filename = frame.filename
            lineno = frame.lineno
            funcname = frame.name

            print(f"Leak of {leak.size / (1024 * 1024):.2f} MiB")
            print(f"File: {filename}")
            print(f"Func: {funcname}")
            print(f"Line: {lineno}")

    def background_run(self):
        tracemalloc.start()

        while True:
            if len(self.snapshots) >= self.max_snapshots:
                self.snapshots.pop(0)  # Remove oldest snapshot

            with self.lock:
                snapshot = tracemalloc.take_snapshot()
                self.snapshots.append(snapshot)

            if len(self.snapshots) > 1:
                leaks = snapshot.compare_to(self.snapshots[-2])
                if leaks:
                    self.process_leaks(leaks)

            time.sleep(self.snapshot_interval)

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retval = func(*args, **kwargs)

            with self.lock:
                if wrapper.call_count % self.snapshot_interval == 0:
                    snapshot = tracemalloc.take_snapshot()
                    self.snapshots.append(snapshot)

            wrapper.call_count += 1
            return retval

        wrapper.call_count = 0
        return wrapper

