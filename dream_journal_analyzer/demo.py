#!/usr/bin/env python3
"""
Demo script for Dream Journal Analyzer
This script demonstrates the key features of the application.
"""

import os
import sys
from main import DreamJournalApp

def run_demo():
    """Run a demonstration of the Dream Journal Analyzer"""
    print("🌙 Dream Journal Analyzer Demo")
    print("=" * 40)
    
    # Initialize the app
    app = DreamJournalApp()
    
    # Add some sample dreams
    print("\n✨ Adding sample dreams...")
    
    # Dream 1: Lucid flying dream
    app.add_dream(
        title="Soaring Through Clouds",
        content="I realized I was dreaming and decided to fly. I soared above the clouds, feeling the wind beneath me. The landscape below was breathtaking - rolling hills covered in emerald grass.",
        emotions=["free", "joyful", "peaceful", "amazed"],
        characters=["myself"],
        themes=["flight", "nature", "lucid", "landscape"],
        lucid=True
    )
    
    # Dream 2: Underwater exploration
    app.add_dream(
        title="Deep Sea Adventure",
        content="I was diving in crystal clear water and discovered a sunken ship. Colorful fish swam around me, and I found a treasure chest filled with ancient coins.",
        emotions=["curious", "excited", "wonder", "peaceful"],
        characters=["myself", "fish"],
        themes=["water", "exploration", "treasure", "discovery"]
    )
    
    # Dream 3: Nightmare
    app.add_dream(
        title="Dark Forest Chase",
        content="I was running through a dark forest, something was chasing me. I couldn't see what it was, but I could hear footsteps behind me. Finally, I found a cabin where I felt safe.",
        emotions=["fear", "anxiety", "panic", "relief"],
        characters=["myself", "unknown pursuer"],
        themes=["chase", "forest", "darkness", "safety"],
        nightmare=True
    )
    
    # Dream 4: School setting
    app.add_dream(
        title="Exam Day Confusion",
        content="I was back in school and had to take an exam I hadn't studied for. The classroom kept changing, and I couldn't find my pencil.",
        emotions=["confused", "anxious", "frustrated"],
        characters=["myself", "classmates", "teacher"],
        themes=["school", "exam", "confusion", "unprepared"]
    )
    
    # Dream 5: Family gathering
    app.add_dream(
        title="Family Reunion",
        content="I was at a family gathering in my childhood home. Everyone was laughing and sharing stories. The house felt warm and filled with love.",
        emotions=["happy", "nostalgic", "loved", "content"],
        characters=["myself", "family", "relatives"],
        themes=["family", "home", "nostalgia", "gathering"]
    )
    
    print("\n📚 Recent Dreams:")
    app.list_dreams(limit=3)
    
    print("\n🔍 Dream Analysis:")
    app.analyze_patterns()
    
    print("\n📊 Dream Statistics:")
    stats = app.journal.get_statistics()
    print(f"Total dreams: {stats['total_dreams']}")
    print(f"Lucid dreams: {stats['lucid_dreams']}")
    print(f"Nightmares: {stats['nightmares']}")
    print(f"Different emotions tracked: {stats['total_emotions']}")
    print(f"Different themes tracked: {stats['total_themes']}")
    print(f"Different characters tracked: {stats['total_characters']}")
    
    print("\n🎯 Demo completed successfully!")
    print("To explore more features, run: python main.py --help")
    print("For interactive mode, run: python main.py interactive")

if __name__ == "__main__":
    run_demo()