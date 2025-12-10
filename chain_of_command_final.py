"""
Chain of Command - Optimal Solution
Find k-th person to receive directive in organizational tree

Time Complexity: O(n + q) - optimal!
Space Complexity: O(n)

Strategy:
1. Build tree from parent array
2. Compute preorder traversal once
3. For each node, store:
   - tin[node]: position where node appears in preorder
   - sub_size[node]: size of subtree rooted at node
4. Answer each query in O(1): order[tin[node] + k - 1]
"""

def findKthPerson(parent, queries):
    n = len(parent)

    children = [[] for _ in range(n + 1)]
    root = 1
    for i, p in enumerate(parent):
        node = i + 1
        if p == -1:
            root = node
        else:
            children[p].append(node)

    order = []
    tin = [0] * (n + 1)
    sub_size = [0] * (n + 1)

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

    res = []
    for u, k in queries:
        if k > sub_size[u]:
            res.append(-1)
        else:
            res.append(order[tin[u] + k - 1])

    return res


# Test cases
if __name__ == "__main__":
    # Example from problem
    parent1 = [-1, 1, 1, 1, 3, 5, 3, 5, 7]
    queries1 = [[1, 5], [7, 2], [9, 2], [3, 6]]
    result1 = findKthPerson(parent1, queries1)
    assert result1 == [6, 9, -1, 9], f"Expected [6, 9, -1, 9], got {result1}"
    print(f"Test 1 passed: {result1}")

    # Sample Case 0
    parent2 = [-1, 1, 1, 2, 2]
    queries2 = [[1, 3], [2, 3]]
    result2 = findKthPerson(parent2, queries2)
    assert result2 == [4, 5], f"Expected [4, 5], got {result2}"
    print(f"Test 2 passed: {result2}")

    # Sample Case 1
    parent3 = [-1, 1, 1, 2, 3, 1, 6]
    queries3 = [[2, 4], [7, 1], [1, 6]]
    result3 = findKthPerson(parent3, queries3)
    assert result3 == [-1, 7, 6], f"Expected [-1, 7, 6], got {result3}"
    print(f"Test 3 passed: {result3}")

    print("\nAll tests passed! ✓")
