"""
Dream data visualization and charting
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import Counter
from datetime import datetime, timedelta
from typing import Dict, List, Any
import numpy as np
from dream_models import DreamJournal


class DreamVisualizer:
    """Creates visualizations for dream data"""
    
    def __init__(self, journal: DreamJournal):
        self.journal = journal
    
    def create_emotion_chart(self, save_path: str = None) -> str:
        """Create a bar chart of emotions"""
        stats = self.journal.get_statistics()
        emotion_counts = stats['emotion_counts']
        
        if not emotion_counts:
            return "No emotion data available for visualization"
        
        # Get top 10 emotions
        top_emotions = Counter(emotion_counts).most_common(10)
        emotions, counts = zip(*top_emotions)
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(emotions, counts, color='skyblue', alpha=0.8)
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(count), ha='center', va='bottom')
        
        plt.title('Most Common Emotions in Dreams', fontsize=16, fontweight='bold')
        plt.xlabel('Emotions', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            return f"Emotion chart saved to {save_path}"
        else:
            plt.show()
            return "Emotion chart displayed"
    
    def create_theme_pie_chart(self, save_path: str = None) -> str:
        """Create a pie chart of dream themes"""
        stats = self.journal.get_statistics()
        theme_counts = stats['theme_counts']
        
        if not theme_counts:
            return "No theme data available for visualization"
        
        # Get top 8 themes
        top_themes = Counter(theme_counts).most_common(8)
        themes, counts = zip(*top_themes)
        
        plt.figure(figsize=(10, 8))
        colors = plt.cm.Set3(np.linspace(0, 1, len(themes)))
        
        wedges, texts, autotexts = plt.pie(counts, labels=themes, autopct='%1.1f%%',
                                          colors=colors, startangle=90)
        
        # Beautify the text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.title('Distribution of Dream Themes', fontsize=16, fontweight='bold')
        plt.axis('equal')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            return f"Theme pie chart saved to {save_path}"
        else:
            plt.show()
            return "Theme pie chart displayed"
    
    def create_timeline_chart(self, save_path: str = None) -> str:
        """Create a timeline chart of dream frequency"""
        if not self.journal.dreams:
            return "No dream data available for timeline visualization"
        
        # Group dreams by date
        dream_dates = [dream.date.date() for dream in self.journal.dreams]
        date_counts = Counter(dream_dates)
        
        # Create a complete date range
        min_date = min(dream_dates)
        max_date = max(dream_dates)
        
        date_range = []
        current_date = min_date
        while current_date <= max_date:
            date_range.append(current_date)
            current_date += timedelta(days=1)
        
        # Create counts for all dates
        counts = [date_counts.get(date, 0) for date in date_range]
        
        plt.figure(figsize=(15, 6))
        plt.plot(date_range, counts, marker='o', linewidth=2, markersize=4)
        plt.fill_between(date_range, counts, alpha=0.3)
        
        plt.title('Dream Frequency Over Time', fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Number of Dreams', fontsize=12)
        
        # Format x-axis
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.xticks(rotation=45)
        
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            return f"Timeline chart saved to {save_path}"
        else:
            plt.show()
            return "Timeline chart displayed"
    
    def create_lucid_nightmare_chart(self, save_path: str = None) -> str:
        """Create a chart showing lucid dreams vs nightmares"""
        lucid_count = len(self.journal.get_lucid_dreams())
        nightmare_count = len(self.journal.get_nightmares())
        normal_count = len(self.journal.dreams) - lucid_count - nightmare_count
        
        if lucid_count + nightmare_count + normal_count == 0:
            return "No dream data available for lucid/nightmare visualization"
        
        categories = ['Normal Dreams', 'Lucid Dreams', 'Nightmares']
        counts = [normal_count, lucid_count, nightmare_count]
        colors = ['lightblue', 'gold', 'lightcoral']
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(categories, counts, color=colors, alpha=0.8)
        
        # Add value labels
        for bar, count in zip(bars, counts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(count), ha='center', va='bottom', fontweight='bold')
        
        plt.title('Dream Types Distribution', fontsize=16, fontweight='bold')
        plt.ylabel('Number of Dreams', fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            return f"Dream types chart saved to {save_path}"
        else:
            plt.show()
            return "Dream types chart displayed"
    
    def create_monthly_trends(self, save_path: str = None) -> str:
        """Create a chart showing monthly dream trends"""
        if not self.journal.dreams:
            return "No dream data available for monthly trends"
        
        # Group by month
        monthly_counts = {}
        for dream in self.journal.dreams:
            month_key = dream.date.strftime('%Y-%m')
            monthly_counts[month_key] = monthly_counts.get(month_key, 0) + 1
        
        # Sort by month
        sorted_months = sorted(monthly_counts.keys())
        counts = [monthly_counts[month] for month in sorted_months]
        
        plt.figure(figsize=(12, 6))
        plt.plot(range(len(sorted_months)), counts, marker='o', linewidth=2, markersize=6)
        plt.fill_between(range(len(sorted_months)), counts, alpha=0.3)
        
        plt.title('Monthly Dream Frequency Trends', fontsize=16, fontweight='bold')
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Number of Dreams', fontsize=12)
        plt.xticks(range(len(sorted_months)), sorted_months, rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            return f"Monthly trends chart saved to {save_path}"
        else:
            plt.show()
            return "Monthly trends chart displayed"
    
    def create_character_network(self, save_path: str = None) -> str:
        """Create a simple character frequency chart"""
        stats = self.journal.get_statistics()
        character_counts = stats['character_counts']
        
        if not character_counts:
            return "No character data available for visualization"
        
        # Get top 10 characters
        top_characters = Counter(character_counts).most_common(10)
        characters, counts = zip(*top_characters)
        
        plt.figure(figsize=(12, 6))
        bars = plt.barh(characters, counts, color='lightgreen', alpha=0.8)
        
        # Add value labels
        for bar, count in zip(bars, counts):
            plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                    str(count), ha='left', va='center', fontweight='bold')
        
        plt.title('Most Frequent Dream Characters', fontsize=16, fontweight='bold')
        plt.xlabel('Frequency', fontsize=12)
        plt.ylabel('Characters', fontsize=12)
        plt.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            return f"Character chart saved to {save_path}"
        else:
            plt.show()
            return "Character chart displayed"
    
    def create_comprehensive_dashboard(self, save_path: str = None) -> str:
        """Create a comprehensive dashboard with multiple charts"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Dream Journal Dashboard', fontsize=20, fontweight='bold')
        
        # 1. Emotion bar chart
        stats = self.journal.get_statistics()
        emotion_counts = stats['emotion_counts']
        if emotion_counts:
            top_emotions = Counter(emotion_counts).most_common(5)
            emotions, counts = zip(*top_emotions)
            axes[0, 0].bar(emotions, counts, color='skyblue', alpha=0.8)
            axes[0, 0].set_title('Top Emotions')
            axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. Dream types pie chart
        lucid_count = len(self.journal.get_lucid_dreams())
        nightmare_count = len(self.journal.get_nightmares())
        normal_count = len(self.journal.dreams) - lucid_count - nightmare_count
        
        if lucid_count + nightmare_count + normal_count > 0:
            labels = ['Normal', 'Lucid', 'Nightmares']
            sizes = [normal_count, lucid_count, nightmare_count]
            colors = ['lightblue', 'gold', 'lightcoral']
            axes[0, 1].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
            axes[0, 1].set_title('Dream Types')
        
        # 3. Monthly trends
        monthly_counts = {}
        for dream in self.journal.dreams:
            month_key = dream.date.strftime('%Y-%m')
            monthly_counts[month_key] = monthly_counts.get(month_key, 0) + 1
        
        if monthly_counts:
            sorted_months = sorted(monthly_counts.keys())
            counts = [monthly_counts[month] for month in sorted_months]
            axes[1, 0].plot(range(len(sorted_months)), counts, marker='o')
            axes[1, 0].set_title('Monthly Trends')
            axes[1, 0].set_xticks(range(len(sorted_months)))
            axes[1, 0].set_xticklabels(sorted_months, rotation=45)
        
        # 4. Top themes
        theme_counts = stats['theme_counts']
        if theme_counts:
            top_themes = Counter(theme_counts).most_common(5)
            themes, counts = zip(*top_themes)
            axes[1, 1].barh(themes, counts, color='lightgreen', alpha=0.8)
            axes[1, 1].set_title('Top Themes')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            return f"Dashboard saved to {save_path}"
        else:
            plt.show()
            return "Dashboard displayed"
    
    def generate_all_charts(self, output_dir: str = "charts") -> List[str]:
        """Generate all available charts"""
        import os
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        results = []
        
        # Generate each chart
        charts = [
            ('emotion_chart.png', self.create_emotion_chart),
            ('theme_pie.png', self.create_theme_pie_chart),
            ('timeline.png', self.create_timeline_chart),
            ('dream_types.png', self.create_lucid_nightmare_chart),
            ('monthly_trends.png', self.create_monthly_trends),
            ('characters.png', self.create_character_network),
            ('dashboard.png', self.create_comprehensive_dashboard)
        ]
        
        for filename, chart_func in charts:
            filepath = os.path.join(output_dir, filename)
            try:
                result = chart_func(filepath)
                results.append(result)
                plt.close('all')  # Close all figures to prevent memory issues
            except Exception as e:
                results.append(f"Error generating {filename}: {e}")
        
        return results