import threading
import time
import queue


def f(name, timeout, queue):
    time.sleep(timeout)
    print('hello', name)
    queue.put(name + ' done!')


q = queue.Queue()  # thread-safe queue
bob = threading.Thread(target=f, args=('bob', 0.3, q))
bob.start()  # start the thread

alice = threading.Thread(target=f, args=('alice', 0.1, q))
alice.start()  # start the thread

# wait for threads to complete
bob.join()
alice.join()

# print results from intercommunication object
for result in iter(q.get, None):
    print(result)
