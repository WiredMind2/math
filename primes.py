import time
import timeit

from matplotlib import pyplot as plt

# Testing some prime functions

fac_cache = {0: 1, 1: 1}

def fac(i):
    try:
        return fac_cache[i]
    except KeyError:
        v = fac(i-1) * i
        fac_cache[i] = v
        return v

def is_prime(i):
    if i == 1:
        return False
    return fac(i - 1) % (i) == (i - 1)

def is_prime_opti(num):
    # From blackbox.ai

    if num <= 1:

        return False

    elif num <= 3:

        return True

    elif num % 2 == 0 or num % 3 == 0:

        return False

    i = 5

    while i * i <= num:

        if num % i == 0 or num % (i + 2) == 0:

            return False

        i += 6

    return True

def SieveOfEratosthenes(num):
    prime = [True for i in range(num + 1)]
    # boolean array
    p = 2
    while p * p <= num:
        # If prime[p] is not
        # changed, then it is a prime
        if prime[p] == True:
            # Updating all multiples of p
            for i in range(p * p, num + 1, p):
                prime[i] = False
        p += 1

    # # Print all prime numbers
    # for p in range(2, num + 1):
    #     if prime[p]:
    #         print(p)

def mass_compute():

    max_value = 1000

    iters = 500

    delays1 = []
    delays2 = []
    delays3 = []
    for i in range(iters):
        #1
        start = time.time()
        for j in range(1, max_value):
            is_prime(j)
        stop = time.time()
        delays1.append(stop-start)

        #2
        start = time.time()
        SieveOfEratosthenes(max_value)
        stop = time.time()
        delays2.append(stop-start)

        #3
        start = time.time()
        for j in range(1, max_value):
            is_prime_opti(j)
        stop = time.time()
        delays3.append(stop-start)
        
    print('Batch primes computation')
    print(f'1 - Avg: {sum(delays1)/len(delays1)}')
    print(f'2 - Avg: {sum(delays2)/len(delays2)}')
    print(f'3 - Avg: {sum(delays3)/len(delays3)}')

def single_compute():
    
    max_value = 500

    iters = 500

    delays1 = []
    delays2 = []
    delays3 = []
    for i in range(iters):
        for v in range(1, max_value):
            #1
            start = time.time()
            is_prime(v)
            stop = time.time()
            delays1.append(stop-start)

            #2
            start = time.time()
            SieveOfEratosthenes(v)
            stop = time.time()
            delays2.append(stop-start)
            
            #3
            start = time.time()
            is_prime_opti(v)
            stop = time.time()
            delays3.append(stop-start)

    print('Single prime computation:')
    print(f'1 - Avg: {sum(delays1)/len(delays1)}')
    print(f'2 - Avg: {sum(delays2)/len(delays2)}')
    print(f'3 - Avg: {sum(delays3)/len(delays3)}')

def plot_complexity():
    max_value = 1000
    steps = 100
    inputs = list(range(steps, max_value, steps))
    
    funcs = (is_prime, is_prime_opti, SieveOfEratosthenes)
    delays = [[] for _ in range(len(funcs))]
    for v in inputs:
        for i, func in enumerate(funcs):
            start_time = timeit.default_timer()

            func(v)

            end_time = timeit.default_timer()

            delays[i].append(end_time - start_time)

    for i, delay in enumerate(delays):
        plt.plot(inputs, delay, label=f'Algorithm n{i}')

    plt.xlabel('Input Size')

    plt.ylabel('Time Taken')

    plt.title('Time Taken for each function')

    plt.legend()
    plt.show()

# mass_compute()
# single_compute()
plot_complexity()



"""
So checking if a number is a prime is faster than computing all previous prime numbers (duh)
BUT 2 is faster than 1 for computing the first n prime, (but not any n prime)
"""