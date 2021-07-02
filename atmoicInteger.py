"""An atomic, thread-safe incrementing counter."""
"""
inspired by:https://gist.github.com/benhoyt/8c8a8d62debe8e5aa5340373f9c509c7
"""
import threading
from multiprocessing import Process
import multiprocessing


class AtomicInteger:
    def __init__(self, start_value=0):
        #make sure it is an integer
        self.value = int(start_value)
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1
            return self.value

    def get_value(self):
        return self.value


def increment_atomicInteger(ai):
    for i in range(100):
        print(ai.increment())

if __name__ == '__main__':
    ai_main = AtomicInteger()
    threads = multiprocessing.cpu_count()
    processes = [threading.Thread(target=increment_atomicInteger, args=(ai_main,)) for _ in range(threads)]
    print(ai_main.get_value())
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    print(ai_main.get_value())
