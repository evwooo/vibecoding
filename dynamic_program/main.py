#!/usr/bin/env python3
"""
Dynamic Programming Learning Application
========================================

An interactive application to learn and understand Dynamic Programming concepts
through various classic problems and examples.
"""

import sys
import os
from typing import Dict, Callable

# Add the current directory to the path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from problems import fibonacci, knapsack, lcs, coin_change, edit_distance, climbing_stairs


class DynamicProgrammingApp:
    """Main application class for Dynamic Programming learning"""
    
    def __init__(self):
        self.problems: Dict[str, Callable] = {
            '1': fibonacci.run_fibonacci_demo,
            '2': knapsack.run_knapsack_demo,
            '3': lcs.run_lcs_demo,
            '4': coin_change.run_coin_change_demo,
            '5': edit_distance.run_edit_distance_demo,
            '6': climbing_stairs.run_climbing_stairs_demo,
        }
        
        self.menu_items = {
            '1': 'Fibonacci Numbers',
            '2': 'Knapsack Problem',
            '3': 'Longest Common Subsequence',
            '4': 'Coin Change Problem',
            '5': 'Edit Distance',
            '6': 'Climbing Stairs',
            '0': 'Exit'
        }
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*60)
        print("🧠 DYNAMIC PROGRAMMING LEARNING CENTER 🧠")
        print("="*60)
        print("\nChoose a problem to explore:")
        print("-" * 40)
        
        for key, value in self.menu_items.items():
            if key == '0':
                print(f"\n{key}. {value}")
            else:
                print(f"{key}. {value}")
        
        print("-" * 40)
        
    def display_intro(self):
        """Display introduction to Dynamic Programming"""
        print("\n🎯 INTRODUCTION TO DYNAMIC PROGRAMMING")
        print("="*50)
        print("""
Dynamic Programming (DP) is a method for solving complex problems by breaking 
them down into simpler subproblems. It is applicable to problems exhibiting 
the properties of overlapping subproblems and optimal substructure.

Key Concepts:
1. OVERLAPPING SUBPROBLEMS: The problem can be broken down into subproblems 
   which are reused several times.

2. OPTIMAL SUBSTRUCTURE: The optimal solution to the problem contains optimal 
   solutions to the subproblems.

3. MEMOIZATION: Store the results of expensive function calls and return the 
   cached result when the same inputs occur again.

4. TABULATION: Build up a table of solutions to subproblems in a bottom-up manner.

Let's explore these concepts through classic problems!
        """)
        
    def run(self):
        """Main application loop"""
        self.display_intro()
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (0-6): ").strip()
            
            if choice == '0':
                print("\n👋 Thank you for learning Dynamic Programming!")
                print("Keep practicing to master these concepts! 🚀")
                break
            
            if choice in self.problems:
                try:
                    print("\n" + "="*60)
                    self.problems[choice]()
                    input("\nPress Enter to continue...")
                except KeyboardInterrupt:
                    print("\n\nReturning to main menu...")
                except Exception as e:
                    print(f"\nError: {e}")
                    input("\nPress Enter to continue...")
            else:
                print("\n❌ Invalid choice. Please select a number between 0-6.")
                input("Press Enter to continue...")


if __name__ == "__main__":
    app = DynamicProgrammingApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        sys.exit(0)