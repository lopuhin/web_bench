import sys
import time
import threading

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


def test_inevitable_info(N):
    def outputs(i):
        time.sleep(1)
        print i
    transaction.set_num_threads(N)
    for x in xrange(N):
        transaction.add(outputs, x)
    transaction.run()

#test_inevitable_info(4)
#exit()


start_prime = 50000000
end_prime = start_prime + 20
tested_primes = range(start_prime, end_prime)


def test_scaling_transaction(N):
    transaction.set_num_threads(N)
    for x in tested_primes:
        transaction.add(is_prime, x)
    transaction.run()

def test_scaling_threads(N):
    def target(n_thread):
        for x in tested_primes:
            if x % N == n_thread:
                is_prime(x)
    threads = []
    for n in xrange(N):
        t = threading.Thread(target=target, args=(n,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

def test_scaling_fake(_):
    for x in tested_primes:
        is_prime(x)

def test_scaling_runner():
    t0 = None
    print
    print '#\tt\trel to 1 thread'
    for n in [1, 2, 3, 4]:
        t = time.time()
       #test_scaling_transaction(n)
        test_scaling_threads(n)
       #test_scaling_fake(n)
        duration = time.time() - t
        if t0 is None:
            t0 = duration
        print '%d\t%.2f\t%.2f %%' % (n, duration, duration / t0 * 100)


for _ in xrange(5):
   #test_scaling_runner()
    t = time.time()
    test_scaling_threads(int(sys.argv[1]))
    print time.time() - t
