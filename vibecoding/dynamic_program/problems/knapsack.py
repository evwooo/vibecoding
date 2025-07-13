"""
0/1 Knapsack Problem - Dynamic Programming Implementation
========================================================

The 0/1 Knapsack problem is a classic optimization problem that demonstrates:
- Optimal substructure
- Overlapping subproblems
- 2D dynamic programming
- Space optimization techniques
"""

from typing import List, Tuple


def knapsack_naive(weights: List[int], values: List[int], capacity: int, n: int) -> int:
    """
    Naive recursive solution - O(2^n) time complexity
    For each item, we have two choices: include it or exclude it
    """
    # Base case
    if n == 0 or capacity == 0:
        return 0
    
    # If weight of nth item is more than capacity, cannot include it
    if weights[n - 1] > capacity:
        return knapsack_naive(weights, values, capacity, n - 1)
    
    # Return maximum of two cases:
    # 1. nth item included
    # 2. nth item not included
    include = values[n - 1] + knapsack_naive(weights, values, capacity - weights[n - 1], n - 1)
    exclude = knapsack_naive(weights, values, capacity, n - 1)
    
    return max(include, exclude)


def knapsack_memoized(weights: List[int], values: List[int], capacity: int, n: int, memo: dict = None) -> int:
    """
    Memoized solution - O(n * capacity) time complexity
    Top-down approach using recursion with memoization
    """
    if memo is None:
        memo = {}
    
    # Create a key for memoization
    key = (n, capacity)
    if key in memo:
        return memo[key]
    
    # Base case
    if n == 0 or capacity == 0:
        memo[key] = 0
        return 0
    
    # If weight of nth item is more than capacity, cannot include it
    if weights[n - 1] > capacity:
        memo[key] = knapsack_memoized(weights, values, capacity, n - 1, memo)
        return memo[key]
    
    # Return maximum of two cases
    include = values[n - 1] + knapsack_memoized(weights, values, capacity - weights[n - 1], n - 1, memo)
    exclude = knapsack_memoized(weights, values, capacity, n - 1, memo)
    
    memo[key] = max(include, exclude)
    return memo[key]


def knapsack_tabulated(weights: List[int], values: List[int], capacity: int) -> Tuple[int, List[int]]:
    """
    Tabulated solution - O(n * capacity) time complexity
    Bottom-up approach using 2D table
    Returns both maximum value and the items selected
    """
    n = len(weights)
    
    # Create 2D DP table
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Fill the table
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                # Maximum of including or excluding current item
                include = values[i - 1] + dp[i - 1][w - weights[i - 1]]
                exclude = dp[i - 1][w]
                dp[i][w] = max(include, exclude)
            else:
                # Cannot include current item
                dp[i][w] = dp[i - 1][w]
    
    # Backtrack to find selected items
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)
            w -= weights[i - 1]
    
    return dp[n][capacity], selected_items[::-1]


def knapsack_optimized(weights: List[int], values: List[int], capacity: int) -> int:
    """
    Space-optimized solution - O(capacity) space complexity
    Since we only need the previous row, we can use 1D array
    """
    n = len(weights)
    dp = [0] * (capacity + 1)
    
    for i in range(n):
        # Traverse from right to left to avoid overwriting
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]


def print_knapsack_table(weights: List[int], values: List[int], capacity: int):
    """Visualize the DP table construction"""
    n = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Fill the table
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                include = values[i - 1] + dp[i - 1][w - weights[i - 1]]
                exclude = dp[i - 1][w]
                dp[i][w] = max(include, exclude)
            else:
                dp[i][w] = dp[i - 1][w]
    
    # Print the table
    print("\n📊 DP Table Visualization:")
    print("Rows: Items (0 to n), Columns: Capacity (0 to W)")
    print("-" * (capacity * 4 + 10))
    
    # Header
    print("Item\\Cap ", end="")
    for w in range(capacity + 1):
        print(f"{w:>3}", end=" ")
    print()
    
    # Table rows
    for i in range(n + 1):
        if i == 0:
            print(f"   {i:>2}   ", end="")
        else:
            print(f"   {i:>2}   ", end="")
        for w in range(capacity + 1):
            print(f"{dp[i][w]:>3}", end=" ")
        print()


def demonstrate_knapsack(weights: List[int], values: List[int], capacity: int):
    """Demonstrate different approaches with timing"""
    n = len(weights)
    
    print(f"🎒 Knapsack Problem:")
    print(f"Capacity: {capacity}")
    print(f"Items: {n}")
    print("-" * 40)
    
    # Display items
    print("Items (Weight, Value):")
    for i in range(n):
        print(f"Item {i + 1}: ({weights[i]}, {values[i]})")
    
    print("-" * 40)
    
    # Tabulated approach (with item tracking)
    max_value, selected_items = knapsack_tabulated(weights, values, capacity)
    print(f"Maximum Value: {max_value}")
    
    print(f"Selected Items: ", end="")
    total_weight = 0
    total_value = 0
    if selected_items:
        for item_idx in selected_items:
            print(f"Item {item_idx + 1}", end=" ")
            total_weight += weights[item_idx]
            total_value += values[item_idx]
    else:
        print("None")
    
    print(f"\nTotal Weight: {total_weight}/{capacity}")
    print(f"Total Value: {total_value}")
    
    # Show table if small enough
    if capacity <= 10 and n <= 6:
        print_knapsack_table(weights, values, capacity)


def run_knapsack_demo():
    """Run the interactive knapsack demonstration"""
    print("🎒 0/1 KNAPSACK PROBLEM - DYNAMIC PROGRAMMING")
    print("="*50)
    
    print("""
📚 CONCEPT EXPLANATION:
Given a knapsack with capacity W and n items with weights and values,
find the maximum value that can be obtained without exceeding the capacity.

Each item can be either included (1) or excluded (0) - hence "0/1" knapsack.

This problem demonstrates:
1. OPTIMAL SUBSTRUCTURE: Solution contains optimal solutions to subproblems
2. OVERLAPPING SUBPROBLEMS: Same subproblems are solved multiple times
3. 2D DYNAMIC PROGRAMMING: State depends on two parameters (items, capacity)

APPROACHES:
1. Naive Recursion: O(2^n) time - Very slow!
2. Memoization: O(n * W) time, O(n * W) space - Top-down
3. Tabulation: O(n * W) time, O(n * W) space - Bottom-up
4. Optimized: O(n * W) time, O(W) space - Space optimized
    """)
    
    # Predefined examples
    examples = [
        {
            "name": "Classic Example",
            "weights": [10, 20, 30],
            "values": [60, 100, 120],
            "capacity": 50
        },
        {
            "name": "Jewelry Store",
            "weights": [1, 3, 4, 5],
            "values": [1, 4, 5, 7],
            "capacity": 7
        },
        {
            "name": "Treasure Hunt",
            "weights": [2, 3, 4, 5, 6],
            "values": [3, 4, 5, 6, 7],
            "capacity": 8
        }
    ]
    
    while True:
        print("\nChoose an option:")
        print("1. Try predefined examples")
        print("2. Enter custom problem")
        print("3. Back to main menu")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            print("\nPredefined Examples:")
            for i, example in enumerate(examples, 1):
                print(f"{i}. {example['name']}")
            
            try:
                ex_choice = int(input("Select example (1-3): ")) - 1
                if 0 <= ex_choice < len(examples):
                    example = examples[ex_choice]
                    print(f"\n--- {example['name']} ---")
                    demonstrate_knapsack(example['weights'], example['values'], example['capacity'])
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a valid number.")
        
        elif choice == '2':
            try:
                print("\nEnter custom problem:")
                n = int(input("Number of items: "))
                if n <= 0:
                    print("Number of items must be positive.")
                    continue
                
                weights = []
                values = []
                
                for i in range(n):
                    weight = int(input(f"Weight of item {i + 1}: "))
                    value = int(input(f"Value of item {i + 1}: "))
                    weights.append(weight)
                    values.append(value)
                
                capacity = int(input("Knapsack capacity: "))
                
                if capacity <= 0:
                    print("Capacity must be positive.")
                    continue
                
                demonstrate_knapsack(weights, values, capacity)
                
            except ValueError:
                print("Please enter valid integers.")
        
        elif choice == '3':
            break
        
        else:
            print("Invalid choice. Please select 1, 2, or 3.")