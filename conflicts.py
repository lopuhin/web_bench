import time
import transaction

from utils import is_prime


def test_conflicts_dict(N):
    for i in xrange(10000):
        def f(i):
            key = 'key'
            if key not in global_dict:
                global_dict[key] = 0
            global_dict[key] += i
        transaction.add(f, i)
    transaction.set_num_threads(N)
    transaction.run()


def test_conflicts_global(N):
    for i in xrange(10000):
        def f(i):
            global global_counter
            if global_counter is None:
                global_counter = 0
            global_counter += i
        transaction.add(f, i)
    transaction.set_num_threads(N)
    transaction.run()


global_dict = {}
global_counter = 0


def test_conflicts():
    global global_dict, global_counter
    while True:
        global_dict = {}
        global_counter = 0
        test_conflicts_dict(4)
        print global_dict
        assert global_dict == {'key': 49995000}
        #assert global_counter == 49995000


def test_scaling(N):
    transaction.set_num_threads(N)
    n = 100000
    for x in xrange(n, n + 2000):
        transaction.add(is_prime, x)
    transaction.run()


t0 = None
for n in (1, 2, 3, 4):
    t = time.time()
    test_scaling(n)
    duration = time.time() - t
    if t0 is None:
        t0 = duration
    print n, duration, duration / t0 * 100, '%'
