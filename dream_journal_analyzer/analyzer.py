"""
Dream pattern analysis and insights generation
"""

import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import statistics
from dream_models import DreamJournal, Dream


class DreamAnalyzer:
    """Analyzes dream patterns and generates insights"""
    
    def __init__(self, journal: DreamJournal):
        self.journal = journal
    
    def analyze_patterns(self) -> Dict[str, Any]:
        """Analyze dream patterns and return insights"""
        stats = self.journal.get_statistics()
        
        if stats['total_dreams'] == 0:
            return {
                'total_dreams': 0,
                'message': 'No dreams to analyze yet. Start logging your dreams!'
            }
        
        # Time-based analysis
        dreams_by_month = self._analyze_dreams_by_month()
        most_active_period = self._find_most_active_period()
        
        # Content analysis
        top_emotions = self._get_top_items(stats['emotion_counts'], 5)
        top_themes = self._get_top_items(stats['theme_counts'], 5)
        common_characters = self._get_top_items(stats['character_counts'], 5)
        
        # Pattern analysis
        recurring_themes = self._find_recurring_themes()
        emotional_trends = self._analyze_emotional_trends()
        
        # Calculate averages
        avg_dreams_per_month = self._calculate_avg_dreams_per_month()
        
        return {
            'total_dreams': stats['total_dreams'],
            'avg_dreams_per_month': avg_dreams_per_month,
            'most_active_period': most_active_period,
            'top_emotions': top_emotions,
            'top_themes': top_themes,
            'common_characters': common_characters,
            'lucid_percentage': stats['lucid_percentage'],
            'nightmare_percentage': stats['nightmare_percentage'],
            'recurring_themes': recurring_themes,
            'emotional_trends': emotional_trends,
            'dreams_by_month': dreams_by_month
        }
    
    def _analyze_dreams_by_month(self) -> Dict[str, int]:
        """Analyze dream frequency by month"""
        dreams_by_month = defaultdict(int)
        
        for dream in self.journal.dreams:
            month_key = dream.date.strftime('%Y-%m')
            dreams_by_month[month_key] += 1
        
        return dict(dreams_by_month)
    
    def _find_most_active_period(self) -> str:
        """Find the most active dreaming period"""
        dreams_by_month = self._analyze_dreams_by_month()
        
        if not dreams_by_month:
            return "No data available"
        
        most_active_month = max(dreams_by_month, key=dreams_by_month.get)
        return f"{most_active_month} ({dreams_by_month[most_active_month]} dreams)"
    
    def _get_top_items(self, counts: Dict[str, int], limit: int) -> List[str]:
        """Get top items from a count dictionary"""
        return [item for item, count in Counter(counts).most_common(limit)]
    
    def _find_recurring_themes(self) -> List[str]:
        """Find themes that appear in multiple dreams"""
        stats = self.journal.get_statistics()
        theme_counts = stats['theme_counts']
        
        # Themes that appear in at least 2 dreams
        recurring = [theme for theme, count in theme_counts.items() if count >= 2]
        return sorted(recurring, key=lambda x: theme_counts[x], reverse=True)
    
    def _analyze_emotional_trends(self) -> str:
        """Analyze emotional trends over time"""
        if len(self.journal.dreams) < 2:
            return "Not enough data for trend analysis"
        
        # Sort dreams by date
        sorted_dreams = sorted(self.journal.dreams, key=lambda d: d.date)
        
        # Split into two halves
        mid_point = len(sorted_dreams) // 2
        early_dreams = sorted_dreams[:mid_point]
        recent_dreams = sorted_dreams[mid_point:]
        
        # Count emotions in each half
        early_emotions = Counter()
        recent_emotions = Counter()
        
        for dream in early_dreams:
            early_emotions.update(dream.emotions)
        
        for dream in recent_dreams:
            recent_emotions.update(dream.emotions)
        
        # Find changes
        increasing_emotions = []
        decreasing_emotions = []
        
        all_emotions = set(early_emotions.keys()) | set(recent_emotions.keys())
        
        for emotion in all_emotions:
            early_count = early_emotions.get(emotion, 0)
            recent_count = recent_emotions.get(emotion, 0)
            
            if recent_count > early_count:
                increasing_emotions.append(emotion)
            elif early_count > recent_count:
                decreasing_emotions.append(emotion)
        
        trends = []
        if increasing_emotions:
            trends.append(f"Increasing: {', '.join(increasing_emotions[:3])}")
        if decreasing_emotions:
            trends.append(f"Decreasing: {', '.join(decreasing_emotions[:3])}")
        
        return "; ".join(trends) if trends else "No significant trends detected"
    
    def _calculate_avg_dreams_per_month(self) -> float:
        """Calculate average dreams per month"""
        if not self.journal.dreams:
            return 0.0
        
        dates = [dream.date for dream in self.journal.dreams]
        earliest = min(dates)
        latest = max(dates)
        
        # Calculate number of months
        months = (latest.year - earliest.year) * 12 + (latest.month - earliest.month) + 1
        
        return len(self.journal.dreams) / months if months > 0 else 0.0
    
    def analyze_content_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in dream content"""
        if not self.journal.dreams:
            return {}
        
        # Word frequency analysis
        word_freq = self._analyze_word_frequency()
        
        # Dream length analysis
        lengths = [len(dream.content.split()) for dream in self.journal.dreams]
        avg_length = statistics.mean(lengths) if lengths else 0
        
        # Common settings/locations
        settings = self._extract_settings()
        
        # Time-related patterns
        time_patterns = self._analyze_time_patterns()
        
        return {
            'common_words': word_freq,
            'avg_dream_length': avg_length,
            'common_settings': settings,
            'time_patterns': time_patterns
        }
    
    def _analyze_word_frequency(self) -> List[Tuple[str, int]]:
        """Analyze word frequency in dream content"""
        # Common words to exclude
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'was', 'were', 'are', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'i', 'me', 'my', 'mine', 'you', 'your', 'yours', 'he', 'him', 'his', 'she', 'her', 'hers',
            'it', 'its', 'we', 'us', 'our', 'ours', 'they', 'them', 'their', 'theirs'
        }
        
        word_count = Counter()
        
        for dream in self.journal.dreams:
            # Extract words and clean them
            words = re.findall(r'\b\w+\b', dream.content.lower())
            filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
            word_count.update(filtered_words)
        
        return word_count.most_common(20)
    
    def _extract_settings(self) -> List[str]:
        """Extract common settings/locations from dreams"""
        settings = []
        location_keywords = ['house', 'school', 'work', 'forest', 'beach', 'city', 'room', 'car', 'street']
        
        for dream in self.journal.dreams:
            content_lower = dream.content.lower()
            for keyword in location_keywords:
                if keyword in content_lower:
                    settings.append(keyword)
        
        return [setting for setting, count in Counter(settings).most_common(10)]
    
    def _analyze_time_patterns(self) -> Dict[str, Any]:
        """Analyze time-related patterns in dreams"""
        # Group dreams by day of week
        day_counts = defaultdict(int)
        
        for dream in self.journal.dreams:
            day_of_week = dream.date.strftime('%A')
            day_counts[day_of_week] += 1
        
        most_common_day = max(day_counts, key=day_counts.get) if day_counts else "Unknown"
        
        return {
            'dreams_by_day': dict(day_counts),
            'most_common_day': most_common_day
        }
    
    def generate_report(self) -> str:
        """Generate a comprehensive dream analysis report"""
        insights = self.analyze_patterns()
        content_patterns = self.analyze_content_patterns()
        
        report = []
        report.append("🌙 DREAM JOURNAL ANALYSIS REPORT 🌙")
        report.append("=" * 50)
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Basic statistics
        report.append("📊 BASIC STATISTICS")
        report.append("-" * 20)
        report.append(f"Total dreams logged: {insights['total_dreams']}")
        report.append(f"Average dreams per month: {insights['avg_dreams_per_month']:.1f}")
        report.append(f"Most active period: {insights['most_active_period']}")
        report.append(f"Lucid dreams: {insights['lucid_percentage']:.1f}%")
        report.append(f"Nightmares: {insights['nightmare_percentage']:.1f}%")
        report.append("")
        
        # Emotional analysis
        report.append("😊 EMOTIONAL ANALYSIS")
        report.append("-" * 20)
        report.append(f"Top emotions: {', '.join(insights['top_emotions'])}")
        report.append(f"Emotional trends: {insights['emotional_trends']}")
        report.append("")
        
        # Thematic analysis
        report.append("🎭 THEMATIC ANALYSIS")
        report.append("-" * 20)
        report.append(f"Top themes: {', '.join(insights['top_themes'])}")
        report.append(f"Recurring themes: {', '.join(insights['recurring_themes'])}")
        report.append("")
        
        # Characters
        report.append("👥 CHARACTER ANALYSIS")
        report.append("-" * 20)
        report.append(f"Most common characters: {', '.join(insights['common_characters'])}")
        report.append("")
        
        # Content patterns
        if content_patterns:
            report.append("📝 CONTENT PATTERNS")
            report.append("-" * 20)
            report.append(f"Average dream length: {content_patterns.get('avg_dream_length', 0):.1f} words")
            
            if 'common_words' in content_patterns:
                top_words = [word for word, count in content_patterns['common_words'][:10]]
                report.append(f"Common words: {', '.join(top_words)}")
            
            if 'common_settings' in content_patterns:
                report.append(f"Common settings: {', '.join(content_patterns['common_settings'])}")
            
            if 'time_patterns' in content_patterns:
                time_data = content_patterns['time_patterns']
                report.append(f"Most common dream day: {time_data.get('most_common_day', 'Unknown')}")
            report.append("")
        
        # Recommendations
        report.append("💡 RECOMMENDATIONS")
        report.append("-" * 20)
        
        if insights['lucid_percentage'] < 10:
            report.append("• Consider practicing lucid dreaming techniques")
        
        if insights['nightmare_percentage'] > 20:
            report.append("• High nightmare frequency - consider stress management")
        
        if insights['total_dreams'] < 10:
            report.append("• Keep logging dreams for better pattern analysis")
        
        if len(insights['top_emotions']) < 3:
            report.append("• Try to identify more emotions in your dreams")
        
        report.append("")
        report.append("🌟 End of Report 🌟")
        
        return "\n".join(report)