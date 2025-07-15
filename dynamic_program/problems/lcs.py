"""
Longest Common Subsequence (LCS) - Dynamic Programming Implementation
===================================================================

The LCS problem demonstrates:
- String/sequence dynamic programming
- 2D DP table construction
- Backtracking to find the actual subsequence
- Optimal substructure in string problems
"""

from typing import List, Tuple


def lcs_naive(X: str, Y: str, m: int, n: int) -> int:
    """
    Naive recursive solution - O(2^(m+n)) time complexity
    """
    # Base case
    if m == 0 or n == 0:
        return 0
    
    # If characters match
    if X[m - 1] == Y[n - 1]:
        return 1 + lcs_naive(X, Y, m - 1, n - 1)
    
    # If characters don't match
    return max(lcs_naive(X, Y, m, n - 1), lcs_naive(X, Y, m - 1, n))


def lcs_memoized(X: str, Y: str, m: int, n: int, memo: dict = None) -> int:
    """
    Memoized solution - O(m * n) time complexity
    """
    if memo is None:
        memo = {}
    
    key = (m, n)
    if key in memo:
        return memo[key]
    
    # Base case
    if m == 0 or n == 0:
        memo[key] = 0
        return 0
    
    # If characters match
    if X[m - 1] == Y[n - 1]:
        memo[key] = 1 + lcs_memoized(X, Y, m - 1, n - 1, memo)
    else:
        # If characters don't match
        memo[key] = max(lcs_memoized(X, Y, m, n - 1, memo), 
                       lcs_memoized(X, Y, m - 1, n, memo))
    
    return memo[key]


def lcs_tabulated(X: str, Y: str) -> Tuple[int, str]:
    """
    Tabulated solution - O(m * n) time complexity
    Returns both length and the actual LCS
    """
    m, n = len(X), len(Y)
    
    # Create 2D DP table
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    # Fill the table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Backtrack to find the actual LCS
    lcs_str = ""
    i, j = m, n
    
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            lcs_str = X[i - 1] + lcs_str
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    return dp[m][n], lcs_str


def lcs_optimized(X: str, Y: str) -> int:
    """
    Space-optimized solution - O(min(m, n)) space complexity
    Only returns the length, not the actual LCS
    """
    m, n = len(X), len(Y)
    
    # Make sure X is the shorter string
    if m > n:
        X, Y = Y, X
        m, n = n, m
    
    # Use only two rows
    prev = [0] * (m + 1)
    curr = [0] * (m + 1)
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if Y[i - 1] == X[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        
        prev, curr = curr, prev
    
    return prev[m]


def print_lcs_table(X: str, Y: str):
    """Visualize the LCS DP table construction"""
    m, n = len(X), len(Y)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    # Fill the table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Print the table
    print("\n📊 LCS DP Table:")
    print("Rows: String X, Columns: String Y")
    print("-" * (n * 4 + 10))
    
    # Header
    print("     ", end="")
    print("  ε ", end="")  # Empty string
    for char in Y:
        print(f"  {char} ", end="")
    print()
    
    # Table rows
    for i in range(m + 1):
        if i == 0:
            print("  ε ", end="")
        else:
            print(f"  {X[i-1]} ", end="")
        
        for j in range(n + 1):
            print(f"{dp[i][j]:>3}", end=" ")
        print()


def find_all_lcs(X: str, Y: str) -> List[str]:
    """
    Find all possible LCS (there might be multiple)
    """
    m, n = len(X), len(Y)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    # Fill the table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Find all LCS using backtracking
    def backtrack(i: int, j: int, current_lcs: str) -> List[str]:
        if i == 0 or j == 0:
            return [current_lcs[::-1]]
        
        result = []
        if X[i - 1] == Y[j - 1]:
            result.extend(backtrack(i - 1, j - 1, current_lcs + X[i - 1]))
        else:
            if dp[i - 1][j] == dp[i][j]:
                result.extend(backtrack(i - 1, j, current_lcs))
            if dp[i][j - 1] == dp[i][j]:
                result.extend(backtrack(i, j - 1, current_lcs))
        
        return result
    
    all_lcs = backtrack(m, n, "")
    return list(set(all_lcs))  # Remove duplicates


def demonstrate_lcs(X: str, Y: str):
    """Demonstrate LCS with different approaches"""
    print(f"🔤 Longest Common Subsequence:")
    print(f"String X: '{X}'")
    print(f"String Y: '{Y}'")
    print("-" * 40)
    
    # Tabulated approach
    lcs_length, lcs_str = lcs_tabulated(X, Y)
    print(f"LCS Length: {lcs_length}")
    print(f"LCS String: '{lcs_str}'")
    
    # Show all possible LCS if there are multiple
    if lcs_length > 0:
        all_lcs = find_all_lcs(X, Y)
        if len(all_lcs) > 1:
            print(f"\nAll possible LCS ({len(all_lcs)}):")
            for i, lcs in enumerate(all_lcs[:10], 1):  # Show max 10
                print(f"  {i}. '{lcs}'")
            if len(all_lcs) > 10:
                print(f"  ... and {len(all_lcs) - 10} more")
    
    # Show table if strings are small enough
    if len(X) <= 8 and len(Y) <= 8:
        print_lcs_table(X, Y)
    
    # Highlight the matching characters
    print(f"\n🎯 Character Matching:")
    print(f"X: {X}")
    print(f"Y: {Y}")
    if lcs_str:
        print(f"LCS: {lcs_str}")
        print("Matching positions:")
        
        # Show positions in X
        x_positions = []
        lcs_index = 0
        for i, char in enumerate(X):
            if lcs_index < len(lcs_str) and char == lcs_str[lcs_index]:
                x_positions.append(i)
                lcs_index += 1
        
        # Show positions in Y
        y_positions = []
        lcs_index = 0
        for i, char in enumerate(Y):
            if lcs_index < len(lcs_str) and char == lcs_str[lcs_index]:
                y_positions.append(i)
                lcs_index += 1
        
        print(f"In X: positions {x_positions}")
        print(f"In Y: positions {y_positions}")


def run_lcs_demo():
    """Run the interactive LCS demonstration"""
    print("🔤 LONGEST COMMON SUBSEQUENCE - DYNAMIC PROGRAMMING")
    print("="*50)
    
    print("""
📚 CONCEPT EXPLANATION:
The Longest Common Subsequence (LCS) problem is to find the longest subsequence 
common to two sequences. A subsequence is a sequence that can be derived from 
another sequence by deleting some or no elements without changing the order.

Example: 
X = "ABCDGH", Y = "AEDFHR"
LCS = "ADH" (length 3)

This problem demonstrates:
1. OPTIMAL SUBSTRUCTURE: LCS(X[0..m], Y[0..n]) contains LCS of subproblems
2. OVERLAPPING SUBPROBLEMS: Same subproblems are solved multiple times
3. STRING DP: Working with character-by-character comparison

APPROACHES:
1. Naive Recursion: O(2^(m+n)) time - Very slow!
2. Memoization: O(m * n) time, O(m * n) space - Top-down
3. Tabulation: O(m * n) time, O(m * n) space - Bottom-up
4. Optimized: O(m * n) time, O(min(m, n)) space - Space optimized
    """)
    
    # Predefined examples
    examples = [
        ("ABCDGH", "AEDFHR"),
        ("AGGTAB", "GXTXAYB"),
        ("ABCBDAB", "BDCABA"),
        ("PROGRAMMING", "DYNAMIC"),
        ("LONGEST", "STONE")
    ]
    
    while True:
        print("\nChoose an option:")
        print("1. Try predefined examples")
        print("2. Enter custom strings")
        print("3. DNA sequence example")
        print("4. Back to main menu")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            print("\nPredefined Examples:")
            for i, (x, y) in enumerate(examples, 1):
                print(f"{i}. X='{x}', Y='{y}'")
            
            try:
                ex_choice = int(input("Select example (1-5): ")) - 1
                if 0 <= ex_choice < len(examples):
                    x, y = examples[ex_choice]
                    print(f"\n--- Example {ex_choice + 1} ---")
                    demonstrate_lcs(x, y)
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a valid number.")
        
        elif choice == '2':
            try:
                print("\nEnter custom strings:")
                x = input("Enter first string: ").strip().upper()
                y = input("Enter second string: ").strip().upper()
                
                if not x or not y:
                    print("Both strings must be non-empty.")
                    continue
                
                demonstrate_lcs(x, y)
                
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '3':
            # DNA sequence example
            print("\n🧬 DNA Sequence Example:")
            dna_examples = [
                ("ATCGCATAAGCGCTAAGCAAATGC", "ATCGCATAAGCGCTAAGCAAATGC"),
                ("GCATCGCAGAGAGTATACAGTACG", "GCATCGCAGAGAGTATACAGTACG"),
                ("ATCGATCG", "TACGATCG")
            ]
            
            for i, (seq1, seq2) in enumerate(dna_examples, 1):
                print(f"\n{i}. Sequence 1: {seq1}")
                print(f"   Sequence 2: {seq2}")
            
            try:
                choice = int(input("Select DNA example (1-3): ")) - 1
                if 0 <= choice < len(dna_examples):
                    seq1, seq2 = dna_examples[choice]
                    demonstrate_lcs(seq1, seq2)
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a valid number.")
        
        elif choice == '4':
            break
        
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")