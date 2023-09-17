import tracemalloc
import atexit
import pytest
from memorable.core import Memorable

class TestMemorable:
    @classmethod
    def setup_class(cls):
        # Initialize Memorable instance for testing
        cls.memorable = Memorable()

    @classmethod
    def teardown_class(cls):
        cls.memorable.stop_tracking()

    def test_start_tracking(self):
        self.memorable.start_tracking()
        assert self.memorable.tracking == True
        self.memorable.stop_tracking()

    def test_stop_tracking(self):
        self.memorable.start_tracking()
        self.memorable.stop_tracking()
        assert self.memorable.tracking == False

    def test_find_memory_leaks(self, capsys):
        self.memorable.start_tracking()

        # Simulate memory leaks (you can customize this)
        big_list = [0] * 1000000

        # Capture stdout to check for printed output
        self.memorable.find_memory_leaks()

        # Ensure that the output contains expected information about memory leaks
        captured = capsys.readouterr()
        assert "Memory Leaks Detected:" in captured.out
        assert "File:" in captured.out
        assert "Line:" in captured.out
        assert "Memory Increase:" in captured.out

        self.memorable.stop_tracking()

    def test_decorator(self, capsys):
        @self.memorable
        def sample_func():
            # Simulate memory leaks (you can customize this)
            big_list = [0] * 1000000

        sample_func()

        # Ensure that the output contains expected information about memory leaks
        captured = capsys.readouterr()
        assert "Memory Leaks Detected:" in captured.out
        assert "File:" in captured.out
        assert "Line:" in captured.out
        assert "Memory Increase:" in captured.out

if __name__ == "__main__":
    pytest.main()
