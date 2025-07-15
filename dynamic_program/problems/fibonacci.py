"""
Fibonacci Numbers - Dynamic Programming Implementation
=====================================================

The Fibonacci sequence is a classic example to understand the concepts of:
- Overlapping subproblems
- Memoization (top-down approach)
- Tabulation (bottom-up approach)
"""

import time
from typing import Dict


def fibonacci_naive(n: int) -> int:
    """
    Naive recursive implementation - O(2^n) time complexity
    This shows why we need dynamic programming!
    """
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


def fibonacci_memoized(n: int, memo: Dict[int, int] = None) -> int:
    """
    Memoized implementation - O(n) time complexity
    Top-down approach using recursion with memoization
    """
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        memo[n] = n
        return n
    
    memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    return memo[n]


def fibonacci_tabulated(n: int) -> int:
    """
    Tabulated implementation - O(n) time complexity
    Bottom-up approach using iteration
    """
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[0] = 0
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]


def fibonacci_optimized(n: int) -> int:
    """
    Space-optimized implementation - O(1) space complexity
    Since we only need the last two values
    """
    if n <= 1:
        return n
    
    prev2 = 0
    prev1 = 1
    
    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    
    return prev1


def demonstrate_fibonacci(n: int):
    """Demonstrate different approaches with timing"""
    print(f"🔢 Computing Fibonacci({n}):")
    print("-" * 40)
    
    # Memoized approach
    start = time.time()
    result_memo = fibonacci_memoized(n)
    time_memo = time.time() - start
    print(f"Memoized:     {result_memo} (Time: {time_memo:.6f}s)")
    
    # Tabulated approach
    start = time.time()
    result_tab = fibonacci_tabulated(n)
    time_tab = time.time() - start
    print(f"Tabulated:    {result_tab} (Time: {time_tab:.6f}s)")
    
    # Optimized approach
    start = time.time()
    result_opt = fibonacci_optimized(n)
    time_opt = time.time() - start
    print(f"Optimized:    {result_opt} (Time: {time_opt:.6f}s)")
    
    # Naive approach (only for small n)
    if n <= 35:
        start = time.time()
        result_naive = fibonacci_naive(n)
        time_naive = time.time() - start
        print(f"Naive:        {result_naive} (Time: {time_naive:.6f}s)")
    else:
        print(f"Naive:        Skipped (too slow for n={n})")


def show_fibonacci_sequence(n: int):
    """Show the first n Fibonacci numbers"""
    print(f"\n📈 First {n} Fibonacci numbers:")
    print("-" * 40)
    
    if n <= 0:
        print("Please enter a positive number.")
        return
    
    sequence = []
    for i in range(n):
        sequence.append(fibonacci_optimized(i))
    
    # Print in rows of 10
    for i in range(0, len(sequence), 10):
        row = sequence[i:i+10]
        print(" ".join(f"{num:>6}" for num in row))


def run_fibonacci_demo():
    """Run the interactive Fibonacci demonstration"""
    print("🔢 FIBONACCI NUMBERS - DYNAMIC PROGRAMMING")
    print("="*50)
    
    print("""
📚 CONCEPT EXPLANATION:
The Fibonacci sequence is defined as:
F(0) = 0, F(1) = 1
F(n) = F(n-1) + F(n-2) for n > 1

This problem demonstrates:
1. OVERLAPPING SUBPROBLEMS: F(n) depends on F(n-1) and F(n-2)
2. OPTIMAL SUBSTRUCTURE: The optimal solution contains optimal solutions to subproblems
3. EXPONENTIAL TIME in naive recursion due to repeated calculations

APPROACHES:
1. Naive Recursion: O(2^n) time - Very slow!
2. Memoization: O(n) time, O(n) space - Top-down
3. Tabulation: O(n) time, O(n) space - Bottom-up
4. Optimized: O(n) time, O(1) space - Space optimized
    """)
    
    while True:
        print("\nChoose an option:")
        print("1. Calculate Fibonacci(n) with timing comparison")
        print("2. Show first n Fibonacci numbers")
        print("3. Back to main menu")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            try:
                n = int(input("Enter n (recommended: 10-40): "))
                if n < 0:
                    print("Please enter a non-negative number.")
                    continue
                demonstrate_fibonacci(n)
            except ValueError:
                print("Please enter a valid integer.")
        
        elif choice == '2':
            try:
                n = int(input("Enter how many numbers to show (max 50): "))
                if n <= 0:
                    print("Please enter a positive number.")
                    continue
                if n > 50:
                    print("Limiting to 50 numbers for display purposes.")
                    n = 50
                show_fibonacci_sequence(n)
            except ValueError:
                print("Please enter a valid integer.")
        
        elif choice == '3':
            break
        
        else:
            print("Invalid choice. Please select 1, 2, or 3.")