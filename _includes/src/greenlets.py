import gevent
from gevent import monkey
monkey.patch_all()
import time


def f(name, timeout):
    time.sleep(timeout)
    print('hello', name)
    return name + ' done!'


bob = gevent.spawn(f, 'bob', 0.3)
bob.start()  # start the greenlet

alice = gevent.spawn(f, 'alice', 0.1)
alice.start()  # start the greenlet

# wait for greenlets to complete
bob.join()
alice.join()

# print results
print(bob.value)
print(alice.value)
