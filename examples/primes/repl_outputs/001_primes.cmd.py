def sieve_of_eratosthenes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i, prime in enumerate(is_prime) if prime]

primes = sieve_of_eratosthenes(10000)
print(f"Found {len(primes)} primes up to 10,000:\n")
for i in range(0, len(primes), 20):
    print(", ".join(str(p) for p in primes[i:i+20]))