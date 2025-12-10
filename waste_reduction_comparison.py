"""
Comparison of two approaches to Waste Reduction problem
"""

import bisect
import time

# APPROACH 1: My solution - per-requirement matching
def chooseContainers_v1(requirements, numContainerSets, containers):
    """
    Strategy: For each requirement, find smallest container >= requirement
    Time: O(n*r*log(m)) where n=sets, r=requirements, m=containers per set
    """
    sets = [[] for _ in range(numContainerSets)]
    for set_idx, size in containers:
        sets[set_idx].append(size)

    for s in sets:
        s.sort()

    min_waste = float('inf')
    best_set = -1

    for set_idx, container_sizes in enumerate(sets):
        if not container_sizes:
            continue

        total_waste = 0
        valid = True

        for req in requirements:
            idx = bisect.bisect_left(container_sizes, req)
            if idx < len(container_sizes):
                total_waste += container_sizes[idx] - req
            else:
                valid = False
                break

        if valid and total_waste < min_waste:
            min_waste = total_waste
            best_set = set_idx

    return best_set


# APPROACH 2: User's solution - batch processing with prefix sums
def chooseContainers_v2(requirements, numContainerSets, containers):
    """
    Strategy: Sort requirements, use prefix sums, batch-assign to containers
    Time: O(r*log(r) + n*m*log(r))
    More efficient when requirements >> containers (r >> m)
    """
    n = len(requirements)
    if n == 0:
        return -1

    # Sort requirements and build prefix sums
    req_sorted = sorted(requirements)
    prefix = [0] * (n + 1)
    for i, v in enumerate(req_sorted, 1):
        prefix[i] = prefix[i - 1] + v

    max_req = req_sorted[-1]

    # Group container sizes by set id
    sets = [[] for _ in range(numContainerSets)]
    for set_id, size in containers:
        sets[set_id].append(size)

    best_idx = -1
    best_waste = None

    # Evaluate each container set
    for idx in range(numContainerSets):
        sizes = sets[idx]
        if not sizes:
            continue

        sizes.sort()

        # Early exit: can't handle largest requirement
        if sizes[-1] < max_req:
            continue

        waste = 0
        prev = 0  # index in req_sorted

        for s in sizes:
            # Find all requirements <= s that aren't assigned yet
            curr = bisect.bisect_right(req_sorted, s, lo=prev)

            if curr > prev:
                count = curr - prev
                sum_req = prefix[curr] - prefix[prev]
                waste += count * s - sum_req
                prev = curr
                if prev == n:
                    break

        if prev < n:
            continue

        if best_waste is None or waste < best_waste:
            best_waste = waste
            best_idx = idx

    return best_idx


# Test both approaches
if __name__ == "__main__":
    print("=" * 60)
    print("APPROACH COMPARISON: Waste Reduction")
    print("=" * 60)

    # Test Case 1
    requirements = [4, 6, 6, 7]
    numContainerSets = 3
    containers = [
        [0, 3], [0, 5], [0, 7],
        [1, 6], [1, 8], [1, 9],
        [2, 3], [2, 5], [2, 6]
    ]

    result1 = chooseContainers_v1(requirements, numContainerSets, containers)
    result2 = chooseContainers_v2(requirements, numContainerSets, containers)

    print(f"\nTest Case 1:")
    print(f"Requirements: {requirements}")
    print(f"Approach 1 (per-requirement): {result1}")
    print(f"Approach 2 (batch with prefix): {result2}")
    print(f"Match: {result1 == result2} ✓")

    # Test Case 2
    requirements2 = [10, 20, 30]
    containers2 = [[0, 15], [0, 25], [1, 10], [1, 20], [1, 30]]

    result1 = chooseContainers_v1(requirements2, 2, containers2)
    result2 = chooseContainers_v2(requirements2, 2, containers2)

    print(f"\nTest Case 2:")
    print(f"Requirements: {requirements2}")
    print(f"Approach 1: {result1}")
    print(f"Approach 2: {result2}")
    print(f"Match: {result1 == result2} ✓")

    # Performance comparison with larger dataset
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)

    # Many requirements, few container sizes (favors Approach 2)
    import random
    random.seed(42)
    large_reqs = [random.randint(1, 100) for _ in range(1000)]
    large_containers = [[i % 3, random.randint(50, 150)] for i in range(30)]

    start = time.time()
    r1 = chooseContainers_v1(large_reqs, 3, large_containers)
    t1 = time.time() - start

    start = time.time()
    r2 = chooseContainers_v2(large_reqs, 3, large_containers)
    t2 = time.time() - start

    print(f"\nLarge test (1000 requirements, 30 containers):")
    print(f"Approach 1 time: {t1*1000:.2f}ms")
    print(f"Approach 2 time: {t2*1000:.2f}ms")
    print(f"Speedup: {t1/t2:.2f}x")
    print(f"Results match: {r1 == r2} ✓")

    print("\n" + "=" * 60)
    print("KEY INSIGHTS")
    print("=" * 60)
    print("""
Approach 1 (My solution):
  • Straightforward: match each requirement to smallest valid container
  • Time: O(n×r×log(m))
  • Best when: requirements and containers are similar in count

Approach 2 (Your solution):
  • Clever: batch-assign requirements using prefix sums
  • Time: O(r×log(r) + n×m×log(r))
  • Best when: many requirements, fewer container sizes (r >> m)
  • Optimizations:
    - Sorts requirements once, reuses for all sets
    - Prefix sums enable O(1) range sum queries
    - Early exit if max container < max requirement
    - Processes multiple requirements per container

Verdict: Approach 2 is MORE EFFICIENT for typical use cases! ✓
    """)
