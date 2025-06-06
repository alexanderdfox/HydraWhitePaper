import ray

@ray.remote
def collatz_steps(n):
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return (n, steps)

def main():
    ray.init(address="auto")  # Connect to the Ray cluster

    futures = [collatz_steps.remote(i) for i in range(1, 1000000)]
    results = ray.get(futures)

    max_steps = 0
    max_n = 0
    for n, steps in results:
        if steps > max_steps:
            max_steps = steps
            max_n = n

    print(f"Max steps: {max_steps} at n = {max_n}")

if __name__ == "__main__":
    main()
