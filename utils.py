# -*- encoding: utf-8 -*-

import logging; logger = logging.getLogger(name=__name__)
from functools import wraps
import time
import traceback


def debug_exec(*deco_args, **deco_kwargs):
    ''' Output execution time to logger.debug, additionally:
    profile = True  - profile with cProfile,
    stat_profile = True - profile with statprof,
    traceback = True - print traceback before each call
    '''
    def deco(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            log_fn = logger.debug
            if deco_kwargs.get('traceback'):
                traceback.print_stack()
            if deco_kwargs.get('traceback'):
                traceback.print_stack()
            log_fn('starting %s', fn.__name__)
            start = time.time()
            stat_profile = deco_kwargs.get('stat_profile')
            if stat_profile:
                import statprof
                statprof.reset(frequency=10000)
                statprof.start()
            try:
                return fn(*args, **kwargs)
            finally:
                log_fn('finished %s in %s s', fn.__name__, time.time() - start)
                if stat_profile:
                    statprof.stop()
                    statprof.display()
        if deco_kwargs.get('profile'):
            import profilehooks
            inner = profilehooks.profile(immediate=True)(inner)
        return inner
    if deco_args:
        return deco(deco_args[0])
    else:
        return deco


def is_prime(n):
    result = True
    for i in xrange(2, n):
        if n % i == 0:
            result = False
    return result


assert is_prime(7)
assert is_prime(31)
assert not is_prime(7 * 31)
