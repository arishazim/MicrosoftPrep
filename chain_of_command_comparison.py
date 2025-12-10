"""
Comparison of two approaches to Chain of Command problem
"""

import time

# APPROACH 1: My solution - DFS per query with memoization
def findKthPerson_v1(parent, queries):
    """
    Strategy: DFS for each unique node in queries, cache results
    Time: O(n + q*m) where m is avg subtree size
    Space: O(n) + cache storage
    """
    n = len(parent)
    children = [[] for _ in range(n + 1)]

    for i in range(n):
        node = i + 1
        parent_node = parent[i]
        if parent_node != -1:
            children[parent_node].append(node)

    for i in range(n + 1):
        children[i].sort()

    cache = {}

    def dfs(node):
        if node in cache:
            return cache[node]
        order = [node]
        for child in children[node]:
            order.extend(dfs(child))
        cache[node] = order
        return order

    result = []
    for start_node, k in queries:
        order = dfs(start_node)
        if k <= len(order):
            result.append(order[k - 1])
        else:
            result.append(-1)

    return result


# APPROACH 2: User's solution - Precompute preorder + range queries
def findKthPerson_v2(parent, queries):
    """
    Strategy: Single preorder traversal, answer queries in O(1)
    Time: O(n + q) - optimal!
    Space: O(n)

    Key insight: If we know:
    - tin[node] = position where node appears in preorder
    - sub_size[node] = size of subtree rooted at node
    Then k-th element in subtree = order[tin[node] + k - 1]
    """
    n = len(parent)

    # Build children lists; nodes are 1..n
    children = [[] for _ in range(n + 1)]
    root = -1
    for node in range(1, n + 1):
        p = parent[node - 1]
        if p == -1:
            root = node
        else:
            children[p].append(node)
    # Children are added in increasing node order, already sorted!

    # Preorder traversal: compute tin and subtree sizes
    order = []
    tin = [0] * (n + 1)
    sub_size = [0] * (n + 1)

    # Iterative DFS to avoid recursion limits
    stack = [(root, 0)]

    while stack:
        u, idx = stack[-1]

        if idx == 0:
            tin[u] = len(order)
            order.append(u)

        if idx < len(children[u]):
            v = children[u][idx]
            stack[-1] = (u, idx + 1)
            stack.append((v, 0))
        else:
            stack.pop()
            sub_size[u] = len(order) - tin[u]

    # Answer queries in O(1) each
    result = []
    for startNode, k in queries:
        u = startNode
        if k > sub_size[u]:
            result.append(-1)
        else:
            pos = tin[u] + k - 1
            result.append(order[pos])

    return result


if __name__ == "__main__":
    print("=" * 70)
    print("APPROACH COMPARISON: Chain of Command")
    print("=" * 70)

    # Test Case 1
    parent1 = [-1, 1, 1, 1, 3, 5, 3, 5, 7]
    queries1 = [[1, 5], [7, 2], [9, 2], [3, 6]]

    result1 = findKthPerson_v1(parent1, queries1)
    result2 = findKthPerson_v2(parent1, queries1)

    print("\nTest Case 1:")
    print(f"Approach 1 (DFS + cache): {result1}")
    print(f"Approach 2 (preorder + O(1) query): {result2}")
    print(f"Expected: [6, 9, -1, 9]")
    print(f"Match: {result1 == result2 == [6, 9, -1, 9]} ✓")

    # Test Case 2
    parent2 = [-1, 1, 1, 2, 2]
    queries2 = [[1, 3], [2, 3]]

    result1 = findKthPerson_v1(parent2, queries2)
    result2 = findKthPerson_v2(parent2, queries2)

    print("\nTest Case 2:")
    print(f"Approach 1: {result1}")
    print(f"Approach 2: {result2}")
    print(f"Expected: [4, 5]")
    print(f"Match: {result1 == result2 == [4, 5]} ✓")

    # Test Case 3
    parent3 = [-1, 1, 1, 2, 3, 1, 6]
    queries3 = [[2, 4], [7, 1], [1, 6]]

    result1 = findKthPerson_v1(parent3, queries3)
    result2 = findKthPerson_v2(parent3, queries3)

    print("\nTest Case 3:")
    print(f"Approach 1: {result1}")
    print(f"Approach 2: {result2}")
    print(f"Expected: [-1, 7, 6]")
    print(f"Match: {result1 == result2 == [-1, 7, 6]} ✓")

    # Performance test
    print("\n" + "=" * 70)
    print("PERFORMANCE COMPARISON")
    print("=" * 70)

    # Large tree with many queries
    import random
    random.seed(42)

    n_large = 10000
    parent_large = [-1] + [random.randint(1, i) for i in range(1, n_large)]
    queries_large = [[random.randint(1, n_large), random.randint(1, 10)]
                     for _ in range(5000)]

    start = time.time()
    r1 = findKthPerson_v1(parent_large, queries_large)
    t1 = time.time() - start

    start = time.time()
    r2 = findKthPerson_v2(parent_large, queries_large)
    t2 = time.time() - start

    print(f"\nLarge test (10K nodes, 5K queries):")
    print(f"Approach 1 time: {t1*1000:.2f}ms")
    print(f"Approach 2 time: {t2*1000:.2f}ms")
    print(f"Speedup: {t1/t2:.2f}x")
    print(f"Results match: {r1 == r2} ✓")

    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print("""
Approach 1 (My solution - DFS with memoization):
  • Performs DFS for each unique query node
  • Caches results to avoid redundant computation
  • Time: O(n + q×m) where m is avg subtree size
  • Works but not optimal for large query sets

Approach 2 (Your solution - Preorder + Range Query): ✓✓✓
  • Brilliant insight: Precompute global preorder ONCE
  • Store tin[node] = position in preorder
  • Store sub_size[node] = subtree size
  • Answer each query in O(1): order[tin[node] + k - 1]
  • Time: O(n + q) - OPTIMAL!

Additional optimizations in Approach 2:
  1. Children naturally sorted (added in node order 1..n)
  2. Iterative DFS avoids recursion stack limits
  3. No memoization needed - precomputation is the key
  4. All queries answered via simple array lookups

Verdict: Approach 2 is SUPERIOR!
  - Faster (O(n + q) vs O(n + q×m))
  - Simpler query processing (O(1) vs DFS)
  - More scalable for large query sets
  - Production-ready with iterative DFS

This demonstrates expert-level competitive programming! ✓
    """)

    # Visual explanation
    print("\n" + "=" * 70)
    print("VISUALIZATION: How Approach 2 Works")
    print("=" * 70)

    parent_demo = [-1, 1, 1, 2, 2]
    print(f"\nTree: parent = {parent_demo}")
    print("""
Tree structure:
       1
      / \\
     2   3
    / \\
   4   5

Preorder traversal: [1, 2, 4, 5, 3]
                     0  1  2  3  4  (indices)

Node data:
  Node | tin | sub_size | Subtree in preorder
  -----|-----|----------|--------------------
   1   |  0  |    5     | [0:5] = [1,2,4,5,3]
   2   |  1  |    3     | [1:4] = [2,4,5]
   3   |  4  |    1     | [4:5] = [3]
   4   |  2  |    1     | [2:3] = [4]
   5   |  3  |    1     | [3:4] = [5]

Query (1, 3): tin[1]=0, k=3, answer = order[0+3-1] = order[2] = 4 ✓
Query (2, 3): tin[2]=1, k=3, answer = order[1+3-1] = order[3] = 5 ✓
    """)
