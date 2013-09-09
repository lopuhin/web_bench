import sys
import transaction

from utils import is_prime


def print_all_primes(N):
    primes = []
    def maybe_add_prime(n):
        if is_prime(n):
            primes.append(n)
    for x in xrange(N):
        transaction.add(maybe_add_prime, x)
    transaction.run()
    print sorted(primes[-10:])
    #import pdb; pdb.set_trace()


if __name__ == '__main__':
    n_threads, N = map(int, sys.argv[1:3])
    transaction.set_num_threads(n_threads)
    print N, 'running on', n_threads, 'threads'
    print_all_primes(N)
