# memorable

A lightweight and fast python program for detecting and reporting memory leaks in functions and classes.

## description

Memorable is a Python decorator that helps you identify memory leaks within specific functions or classes. It utilizes Python's built-in `tracemalloc` module to capture memory snapshots before and after the execution of the decorated code. It then compares these snapshots to detect memory allocations that have not been released.

## usage

- just import Memorable from the core as:

```python
from memorable.core import Memorable
```

- use  `Memorable()` as a decorator for any function or class you'd want to detect memory leaks for

```python
@Memorable()
def my_function():
    # Code that may potentially cause memory leaks
```

- Run your Python script. When the decorated function or class is executed, Memorable will capture memory allocation data and report any memory leaks detected.

- The detected memory leaks will be printed to the console with information about the file, line number, and the increase in memory size. For example:

```bash
Memory Leaks Detected:
File: example.py
Line: 42
Memory Increase: 0.45 KiB

File: example.py
Line: 58
Memory Increase: 0.09 KiB
```

## todo

[ ]  Implement more advanced memory leak detection algorithms.
