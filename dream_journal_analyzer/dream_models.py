"""
Dream data models for the Dream Journal Analyzer
"""

import json
import csv
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Dream:
    """Represents a single dream entry"""
    title: str
    content: str
    emotions: List[str]
    characters: List[str]
    themes: List[str]
    lucid: bool = False
    nightmare: bool = False
    date: datetime = None
    id: str = None
    
    def __post_init__(self):
        if self.date is None:
            self.date = datetime.now()
        if self.id is None:
            self.id = str(uuid.uuid4())[:8]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert dream to dictionary format"""
        data = asdict(self)
        data['date'] = self.date.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Dream':
        """Create dream from dictionary"""
        data['date'] = datetime.fromisoformat(data['date'])
        return cls(**data)
    
    def matches_search(self, search_term: str) -> bool:
        """Check if dream matches search term"""
        search_term = search_term.lower()
        return (
            search_term in self.title.lower() or
            search_term in self.content.lower() or
            any(search_term in emotion.lower() for emotion in self.emotions) or
            any(search_term in character.lower() for character in self.characters) or
            any(search_term in theme.lower() for theme in self.themes)
        )


class DreamJournal:
    """Manages a collection of dreams with persistence"""
    
    def __init__(self, data_file: str = 'dreams.json'):
        self.data_file = data_file
        self.dreams: List[Dream] = []
        self.load_dreams()
    
    def load_dreams(self):
        """Load dreams from file"""
        if Path(self.data_file).exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.dreams = [Dream.from_dict(dream_data) for dream_data in data]
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Warning: Could not load dreams from {self.data_file}: {e}")
                self.dreams = []
    
    def save_dreams(self):
        """Save dreams to file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([dream.to_dict() for dream in self.dreams], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving dreams: {e}")
    
    def add_dream(self, dream: Dream):
        """Add a new dream to the journal"""
        self.dreams.append(dream)
        self.save_dreams()
    
    def get_dreams(self, limit: int = None, search: str = None) -> List[Dream]:
        """Get dreams with optional limit and search"""
        dreams = self.dreams
        
        if search:
            dreams = [dream for dream in dreams if dream.matches_search(search)]
        
        # Sort by date (newest first)
        dreams = sorted(dreams, key=lambda d: d.date, reverse=True)
        
        if limit:
            dreams = dreams[:limit]
        
        return dreams
    
    def get_dream_by_id(self, dream_id: int) -> Optional[Dream]:
        """Get a dream by its position in the list (1-indexed)"""
        try:
            sorted_dreams = sorted(self.dreams, key=lambda d: d.date, reverse=True)
            if 1 <= dream_id <= len(sorted_dreams):
                return sorted_dreams[dream_id - 1]
        except (IndexError, ValueError):
            pass
        return None
    
    def get_dreams_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dream]:
        """Get dreams within a date range"""
        return [
            dream for dream in self.dreams
            if start_date <= dream.date <= end_date
        ]
    
    def get_dreams_by_emotion(self, emotion: str) -> List[Dream]:
        """Get dreams containing a specific emotion"""
        return [
            dream for dream in self.dreams
            if emotion.lower() in [e.lower() for e in dream.emotions]
        ]
    
    def get_dreams_by_theme(self, theme: str) -> List[Dream]:
        """Get dreams containing a specific theme"""
        return [
            dream for dream in self.dreams
            if theme.lower() in [t.lower() for t in dream.themes]
        ]
    
    def get_lucid_dreams(self) -> List[Dream]:
        """Get all lucid dreams"""
        return [dream for dream in self.dreams if dream.lucid]
    
    def get_nightmares(self) -> List[Dream]:
        """Get all nightmares"""
        return [dream for dream in self.dreams if dream.nightmare]
    
    def delete_dream(self, dream_id: int) -> bool:
        """Delete a dream by ID"""
        dream = self.get_dream_by_id(dream_id)
        if dream:
            self.dreams.remove(dream)
            self.save_dreams()
            return True
        return False
    
    def update_dream(self, dream_id: int, updates: Dict[str, Any]) -> bool:
        """Update a dream with new data"""
        dream = self.get_dream_by_id(dream_id)
        if dream:
            for key, value in updates.items():
                if hasattr(dream, key):
                    setattr(dream, key, value)
            self.save_dreams()
            return True
        return False
    
    def export_to_json(self, filename: str):
        """Export dreams to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([dream.to_dict() for dream in self.dreams], f, indent=2, ensure_ascii=False)
    
    def export_to_csv(self, filename: str):
        """Export dreams to CSV file"""
        if not self.dreams:
            return
        
        fieldnames = ['id', 'title', 'content', 'date', 'emotions', 'characters', 'themes', 'lucid', 'nightmare']
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for dream in self.dreams:
                row = dream.to_dict()
                row['emotions'] = '; '.join(row['emotions'])
                row['characters'] = '; '.join(row['characters'])
                row['themes'] = '; '.join(row['themes'])
                writer.writerow(row)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get basic statistics about the dream journal"""
        if not self.dreams:
            return {'total_dreams': 0}
        
        total_dreams = len(self.dreams)
        lucid_dreams = len(self.get_lucid_dreams())
        nightmares = len(self.get_nightmares())
        
        # Get date range
        dates = [dream.date for dream in self.dreams]
        earliest_date = min(dates)
        latest_date = max(dates)
        
        # Count emotions and themes
        all_emotions = []
        all_themes = []
        all_characters = []
        
        for dream in self.dreams:
            all_emotions.extend(dream.emotions)
            all_themes.extend(dream.themes)
            all_characters.extend(dream.characters)
        
        emotion_counts = {}
        theme_counts = {}
        character_counts = {}
        
        for emotion in all_emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        for theme in all_themes:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        for character in all_characters:
            character_counts[character] = character_counts.get(character, 0) + 1
        
        return {
            'total_dreams': total_dreams,
            'lucid_dreams': lucid_dreams,
            'nightmares': nightmares,
            'lucid_percentage': (lucid_dreams / total_dreams) * 100 if total_dreams > 0 else 0,
            'nightmare_percentage': (nightmares / total_dreams) * 100 if total_dreams > 0 else 0,
            'earliest_date': earliest_date,
            'latest_date': latest_date,
            'emotion_counts': emotion_counts,
            'theme_counts': theme_counts,
            'character_counts': character_counts,
            'total_emotions': len(emotion_counts),
            'total_themes': len(theme_counts),
            'total_characters': len(character_counts)
        }