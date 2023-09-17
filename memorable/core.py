import tracemalloc
import atexit

class Memorable:
    def __init__(self):
        self.tracking = False
        self.snapshot_before = None

    def start_tracking(self):
        if not self.tracking:
            tracemalloc.start()
            atexit.register(tracemalloc.stop)
            self.snapshot_before = tracemalloc.take_snapshot()
            self.tracking = True

    def stop_tracking(self):
        if self.tracking:
            tracemalloc.stop()
            self.tracking = False

    def find_memory_leaks(self):
        if self.snapshot_before:
            snapshot_after = tracemalloc.take_snapshot()
            stats = snapshot_after.compare_to(self.snapshot_before, "lineno")
            if stats:
                print("\nMemory Leaks Detected:")
                for stat in stats:
                    if stat.size_diff > 0:
                        traceback = stat.traceback
                        print(f"File: {traceback[0].filename}")
                        print(f"Line: {traceback[0].lineno}")
                        print(f"Memory Increase: {stat.size_diff / 1024:.2f} KiB\n")

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            self.start_tracking()
            result = func(*args, **kwargs)
            self.find_memory_leaks()
            self.stop_tracking()
            return result

        return wrapper
