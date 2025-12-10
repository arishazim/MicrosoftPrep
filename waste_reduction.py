"""
Waste Reduction - Find the container set that minimizes waste

Problem: Given requirements and multiple container sets, find which set
minimizes total waste when using smallest container >= each requirement.
"""

import bisect

def chooseContainers(requirements, numContainerSets, containers):
    """
    Optimal solution using binary search for efficiency.
    Time: O(n*m + m*log(m) + n*r*log(m)) where n=numSets, m=containers per set, r=requirements
    Space: O(n*m)
    """
    # Group containers by set index
    sets = [[] for _ in range(numContainerSets)]
    for set_idx, size in containers:
        sets[set_idx].append(size)

    # Sort each set for binary search
    for s in sets:
        s.sort()

    min_waste = float('inf')
    best_set = -1

    # Evaluate each container set
    for set_idx, container_sizes in enumerate(sets):
        if not container_sizes:
            continue

        total_waste = 0
        valid = True

        # Check each requirement
        for req in requirements:
            # Binary search for smallest container >= req
            idx = bisect.bisect_left(container_sizes, req)

            if idx < len(container_sizes):
                total_waste += container_sizes[idx] - req
            else:
                # No container large enough
                valid = False
                break

        if valid and total_waste < min_waste:
            min_waste = total_waste
            best_set = set_idx

    return best_set


def chooseContainers_simple(requirements, numContainerSets, containers):
    """
    Simpler solution without binary search (easier to understand).
    Time: O(n*m + n*r*m) - slightly less efficient but more readable
    """
    # Group and sort containers by set
    sets = [[] for _ in range(numContainerSets)]
    for set_idx, size in containers:
        sets[set_idx].append(size)
    for s in sets:
        s.sort()

    min_waste = float('inf')
    best_set = -1

    for set_idx, sizes in enumerate(sets):
        if not sizes:
            continue

        total_waste = 0
        valid = True

        for req in requirements:
            # Find smallest container >= req
            container = next((s for s in sizes if s >= req), None)
            if container is None:
                valid = False
                break
            total_waste += container - req

        if valid and total_waste < min_waste:
            min_waste = total_waste
            best_set = set_idx

    return best_set


# Test with the example
if __name__ == "__main__":
    requirements = [4, 6, 6, 7]
    numContainerSets = 3
    containers = [
        [0, 3], [0, 5], [0, 7],
        [1, 6], [1, 8], [1, 9],
        [2, 3], [2, 5], [2, 6]
    ]

    result = chooseContainers(requirements, numContainerSets, containers)
    print(f"Best container set: {result}")

    # Verify the logic:
    # Set 0 [3,5,7]: req 4->5(w=1), 6->7(w=1), 6->7(w=1), 7->7(w=0) = 3 total
    # Set 1 [6,8,9]: req 4->6(w=2), 6->6(w=0), 6->6(w=0), 7->8(w=1) = 3 total
    # Set 2 [3,5,6]: req 4->5(w=1), 6->6(w=0), 6->6(w=0), 7->NONE = invalid
    # Result: 0 (both have waste=3, return lower index)

    print("\nTest Case 2:")
    requirements2 = [10, 20, 30]
    containers2 = [[0, 15], [0, 25], [1, 10], [1, 20], [1, 30]]
    result2 = chooseContainers(requirements2, 2, containers2)
    print(f"Best container set: {result2}")
    # Set 0 [15,25]: 10->15(w=5), 20->25(w=5), 30->NONE = invalid
    # Set 1 [10,20,30]: 10->10(w=0), 20->20(w=0), 30->30(w=0) = 0 total
    # Result: 1
