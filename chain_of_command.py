"""
Chain of Command - Find k-th person to receive directive in organizational tree

Problem: Given a tree structure and queries, find the k-th person to receive
a directive using DFS traversal with children processed in ascending order.
"""

def findKthPerson(parent, queries):
    """
    Optimal solution with memoization to cache DFS results.

    Time: O(n + q*m) where n=nodes, q=queries, m=avg subtree size
    Space: O(n) for tree structure and cache

    Key insight: DFS with children sorted gives propagation order
    """
    n = len(parent)

    # Build adjacency list (children for each node)
    # Note: parent[i] represents node i+1 (1-indexed)
    children = [[] for _ in range(n + 1)]
    for i in range(n):
        node = i + 1
        parent_node = parent[i]
        if parent_node != -1:
            children[parent_node].append(node)

    # Sort children lists to ensure ascending order traversal
    for i in range(n + 1):
        children[i].sort()

    # Cache DFS results to avoid recomputation
    cache = {}

    def dfs(node):
        """Get propagation order starting from node using DFS"""
        if node in cache:
            return cache[node]

        # Start with current node, then add all descendants
        order = [node]
        for child in children[node]:
            order.extend(dfs(child))

        cache[node] = order
        return order

    # Process each query
    result = []
    for start_node, k in queries:
        order = dfs(start_node)
        if k <= len(order):
            result.append(order[k - 1])  # k is 1-indexed
        else:
            result.append(-1)

    return result


# Test with examples
if __name__ == "__main__":
    print("=" * 70)
    print("CHAIN OF COMMAND - Test Cases")
    print("=" * 70)

    # Example from problem description
    print("\nExample from description:")
    parent1 = [-1, 1, 1, 1, 3, 5, 3, 5, 7]
    queries1 = [[1, 5], [7, 2], [9, 2], [3, 6]]
    result1 = findKthPerson(parent1, queries1)
    print(f"parent = {parent1}")
    print(f"queries = {queries1}")
    print(f"result = {result1}")
    print(f"expected = [6, 9, -1, 9]")
    print(f"Match: {result1 == [6, 9, -1, 9]} ✓")

    # Sample Case 0
    print("\n" + "-" * 70)
    print("Sample Case 0:")
    parent2 = [-1, 1, 1, 2, 2]
    queries2 = [[1, 3], [2, 3]]
    result2 = findKthPerson(parent2, queries2)
    print(f"parent = {parent2}")
    print(f"queries = {queries2}")
    print(f"result = {result2}")
    print(f"expected = [4, 5]")
    print(f"Match: {result2 == [4, 5]} ✓")

    # Sample Case 1
    print("\n" + "-" * 70)
    print("Sample Case 1:")
    parent3 = [-1, 1, 1, 2, 3, 1, 6]
    queries3 = [[2, 4], [7, 1], [1, 6]]
    result3 = findKthPerson(parent3, queries3)
    print(f"parent = {parent3}")
    print(f"queries = {queries3}")
    print(f"result = {result3}")
    print(f"expected = [-1, 7, 6]")
    print(f"Match: {result3 == [-1, 7, 6]} ✓")

    # Detailed trace for understanding
    print("\n" + "=" * 70)
    print("DETAILED TRACE - Example 1")
    print("=" * 70)

    def visualize_tree(parent):
        n = len(parent)
        children = [[] for _ in range(n + 1)]
        root = -1
        for i in range(n):
            node = i + 1
            if parent[i] == -1:
                root = node
            else:
                children[parent[i]].append(node)

        for i in range(n + 1):
            children[i].sort()

        def dfs_trace(node, indent=0):
            order = [node]
            print(f"{'  ' * indent}Node {node}")
            for child in children[node]:
                child_order = dfs_trace(child, indent + 1)
                order.extend(child_order)
            return order

        print(f"\nTree structure (DFS traversal from root {root}):")
        full_order = dfs_trace(root)
        print(f"\nPropagation order from node {root}: {full_order}")
        return full_order

    visualize_tree(parent1)

    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print("""
Algorithm:
1. Build adjacency list from parent array (1-indexed nodes)
2. Sort children for each node (ascending order requirement)
3. Use DFS to build propagation order for each query
4. Cache results to optimize repeated queries on same node

Complexity:
- Time: O(n) tree building + O(n log n) sorting + O(q×m) queries
  where m is average subtree size
- Space: O(n) for tree and cache

Optimization:
- Memoization prevents recomputing same subtrees
- Sorted children list ensures correct propagation order
""")
