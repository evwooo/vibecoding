#!/usr/bin/env python3
"""
Dream Journal Analyzer - A comprehensive tool for logging and analyzing dreams
Author: Assistant
Description: Log dreams, analyze patterns, and gain insights into your subconscious mind
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional
import os

from dream_models import Dream, DreamJournal
from analyzer import DreamAnalyzer
from visualizer import DreamVisualizer
from config import Config


class DreamJournalApp:
    def __init__(self):
        self.config = Config()
        self.journal = DreamJournal(self.config.data_file)
        self.analyzer = DreamAnalyzer(self.journal)
        self.visualizer = DreamVisualizer(self.journal)
    
    def add_dream(self, title: str, content: str, emotions: List[str], 
                  characters: List[str], themes: List[str], 
                  lucid: bool = False, nightmare: bool = False):
        """Add a new dream entry"""
        dream = Dream(
            title=title,
            content=content,
            emotions=emotions,
            characters=characters,
            themes=themes,
            lucid=lucid,
            nightmare=nightmare
        )
        
        self.journal.add_dream(dream)
        print(f"✨ Dream '{title}' added successfully!")
        return dream
    
    def list_dreams(self, limit: int = 10, search: str = None):
        """List recent dreams"""
        dreams = self.journal.get_dreams(limit=limit, search=search)
        
        if not dreams:
            print("📖 No dreams found in your journal.")
            return
        
        print(f"\n📚 {'Recent Dreams' if not search else f'Dreams matching \"{search}\"'}:")
        print("=" * 50)
        
        for i, dream in enumerate(dreams, 1):
            print(f"{i}. {dream.title}")
            print(f"   Date: {dream.date.strftime('%Y-%m-%d %H:%M')}")
            print(f"   Emotions: {', '.join(dream.emotions)}")
            print(f"   Themes: {', '.join(dream.themes)}")
            if dream.lucid:
                print("   🌟 Lucid Dream")
            if dream.nightmare:
                print("   😰 Nightmare")
            print()
    
    def view_dream(self, dream_id: int):
        """View a specific dream in detail"""
        dream = self.journal.get_dream_by_id(dream_id)
        if not dream:
            print(f"❌ Dream with ID {dream_id} not found.")
            return
        
        print(f"\n🌙 {dream.title}")
        print("=" * 50)
        print(f"Date: {dream.date.strftime('%Y-%m-%d %H:%M')}")
        print(f"ID: {dream.id}")
        print()
        print("Content:")
        print(dream.content)
        print()
        print(f"Emotions: {', '.join(dream.emotions)}")
        print(f"Characters: {', '.join(dream.characters)}")
        print(f"Themes: {', '.join(dream.themes)}")
        
        if dream.lucid:
            print("🌟 This was a lucid dream!")
        if dream.nightmare:
            print("😰 This was a nightmare!")
    
    def analyze_patterns(self):
        """Analyze dream patterns and show insights"""
        print("\n🔍 Analyzing your dream patterns...")
        
        insights = self.analyzer.analyze_patterns()
        
        print("\n📊 Dream Analysis Results:")
        print("=" * 50)
        
        print(f"Total dreams logged: {insights['total_dreams']}")
        print(f"Average dreams per month: {insights['avg_dreams_per_month']:.1f}")
        print(f"Most active dreaming period: {insights['most_active_period']}")
        
        print(f"\nTop emotions: {', '.join(insights['top_emotions'])}")
        print(f"Top themes: {', '.join(insights['top_themes'])}")
        print(f"Most common characters: {', '.join(insights['common_characters'])}")
        
        print(f"\nLucid dreams: {insights['lucid_percentage']:.1f}%")
        print(f"Nightmares: {insights['nightmare_percentage']:.1f}%")
        
        if insights['recurring_themes']:
            print(f"\nRecurring themes: {', '.join(insights['recurring_themes'])}")
        
        if insights['emotional_trends']:
            print(f"\nEmotional trends: {insights['emotional_trends']}")
    
    def generate_report(self):
        """Generate a comprehensive dream report"""
        print("\n📋 Generating comprehensive dream report...")
        
        report = self.analyzer.generate_report()
        
        report_file = f"dream_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"✅ Report saved to: {report_file}")
        
        # Also display a summary
        print("\n📋 Report Summary:")
        print("=" * 50)
        print(report[:500] + "...")
    
    def export_data(self, format: str = 'json'):
        """Export dream data"""
        if format == 'json':
            filename = f"dreams_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            self.journal.export_to_json(filename)
            print(f"✅ Dreams exported to: {filename}")
        elif format == 'csv':
            filename = f"dreams_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            self.journal.export_to_csv(filename)
            print(f"✅ Dreams exported to: {filename}")
        else:
            print("❌ Unsupported export format. Use 'json' or 'csv'.")


def main():
    parser = argparse.ArgumentParser(description='Dream Journal Analyzer')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add dream command
    add_parser = subparsers.add_parser('add', help='Add a new dream')
    add_parser.add_argument('title', help='Dream title')
    add_parser.add_argument('content', help='Dream content/description')
    add_parser.add_argument('--emotions', nargs='+', default=[], help='Emotions felt in the dream')
    add_parser.add_argument('--characters', nargs='+', default=[], help='Characters in the dream')
    add_parser.add_argument('--themes', nargs='+', default=[], help='Themes of the dream')
    add_parser.add_argument('--lucid', action='store_true', help='Mark as lucid dream')
    add_parser.add_argument('--nightmare', action='store_true', help='Mark as nightmare')
    
    # List dreams command
    list_parser = subparsers.add_parser('list', help='List recent dreams')
    list_parser.add_argument('--limit', type=int, default=10, help='Number of dreams to show')
    list_parser.add_argument('--search', help='Search for specific content')
    
    # View dream command
    view_parser = subparsers.add_parser('view', help='View a specific dream')
    view_parser.add_argument('id', type=int, help='Dream ID to view')
    
    # Analyze command
    subparsers.add_parser('analyze', help='Analyze dream patterns')
    
    # Report command
    subparsers.add_parser('report', help='Generate comprehensive report')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export dream data')
    export_parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Export format')
    
    # Interactive mode
    subparsers.add_parser('interactive', help='Start interactive mode')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    app = DreamJournalApp()
    
    try:
        if args.command == 'add':
            app.add_dream(
                title=args.title,
                content=args.content,
                emotions=args.emotions,
                characters=args.characters,
                themes=args.themes,
                lucid=args.lucid,
                nightmare=args.nightmare
            )
        
        elif args.command == 'list':
            app.list_dreams(limit=args.limit, search=args.search)
        
        elif args.command == 'view':
            app.view_dream(args.id)
        
        elif args.command == 'analyze':
            app.analyze_patterns()
        
        elif args.command == 'report':
            app.generate_report()
        
        elif args.command == 'export':
            app.export_data(format=args.format)
        
        elif args.command == 'interactive':
            interactive_mode(app)
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Sweet dreams!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def interactive_mode(app):
    """Interactive mode for easier dream entry"""
    print("🌙 Welcome to Interactive Dream Journal Mode!")
    print("Type 'help' for commands or 'quit' to exit.")
    
    while True:
        try:
            command = input("\n🌟 > ").strip().lower()
            
            if command == 'quit' or command == 'exit':
                break
            
            elif command == 'help':
                print("\nAvailable commands:")
                print("  add     - Add a new dream")
                print("  list    - List recent dreams")
                print("  analyze - Analyze patterns")
                print("  help    - Show this help")
                print("  quit    - Exit interactive mode")
            
            elif command == 'add':
                print("\n✨ Adding a new dream...")
                title = input("Dream title: ").strip()
                content = input("Dream content: ").strip()
                
                emotions = input("Emotions (comma-separated): ").strip()
                emotions = [e.strip() for e in emotions.split(',') if e.strip()]
                
                characters = input("Characters (comma-separated): ").strip()
                characters = [c.strip() for c in characters.split(',') if c.strip()]
                
                themes = input("Themes (comma-separated): ").strip()
                themes = [t.strip() for t in themes.split(',') if t.strip()]
                
                lucid = input("Was this a lucid dream? (y/n): ").strip().lower() == 'y'
                nightmare = input("Was this a nightmare? (y/n): ").strip().lower() == 'y'
                
                app.add_dream(title, content, emotions, characters, themes, lucid, nightmare)
            
            elif command == 'list':
                app.list_dreams()
            
            elif command == 'analyze':
                app.analyze_patterns()
            
            else:
                print("❌ Unknown command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            break
        except EOFError:
            break
    
    print("\n👋 Exiting interactive mode. Sweet dreams!")


if __name__ == '__main__':
    main()