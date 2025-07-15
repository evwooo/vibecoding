"""
Configuration management for Dream Journal Analyzer
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """Manages application configuration"""
    
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = config_file
        self.default_config = {
            'data_file': 'dreams.json',
            'backup_enabled': True,
            'backup_frequency': 'daily',
            'max_backups': 7,
            'export_format': 'json',
            'date_format': '%Y-%m-%d %H:%M:%S',
            'visualization': {
                'default_chart_size': [12, 8],
                'color_scheme': 'default',
                'save_charts': True,
                'chart_directory': 'charts'
            },
            'analysis': {
                'min_dreams_for_analysis': 5,
                'pattern_threshold': 0.3,
                'emotion_categories': {
                    'positive': ['happy', 'joy', 'excited', 'peaceful', 'love', 'content'],
                    'negative': ['sad', 'fear', 'angry', 'anxious', 'confused', 'frustrated'],
                    'neutral': ['curious', 'calm', 'indifferent', 'focused']
                }
            },
            'ui': {
                'show_colors': True,
                'show_emojis': True,
                'page_size': 10,
                'auto_save': True
            }
        }
        
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return self._merge_config(self.default_config, config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file {self.config_file}: {e}")
                print("Using default configuration.")
        
        # Create default config file
        self.save_config(self.default_config)
        return self.default_config.copy()
    
    def _merge_config(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge user config with default config"""
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def save_config(self, config: Dict[str, Any] = None):
        """Save configuration to file"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except IOError as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default=None):
        """Get configuration value with dot notation support"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value with dot notation support"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config()
    
    @property
    def data_file(self) -> str:
        """Get the data file path"""
        return self.get('data_file', 'dreams.json')
    
    @property
    def backup_enabled(self) -> bool:
        """Check if backup is enabled"""
        return self.get('backup_enabled', True)
    
    @property
    def visualization_settings(self) -> Dict[str, Any]:
        """Get visualization settings"""
        return self.get('visualization', {})
    
    @property
    def analysis_settings(self) -> Dict[str, Any]:
        """Get analysis settings"""
        return self.get('analysis', {})
    
    @property
    def ui_settings(self) -> Dict[str, Any]:
        """Get UI settings"""
        return self.get('ui', {})
    
    def create_backup(self):
        """Create a backup of the current data file"""
        if not self.backup_enabled:
            return
        
        data_file = self.data_file
        if not os.path.exists(data_file):
            return
        
        # Create backup directory
        backup_dir = Path('backups')
        backup_dir.mkdir(exist_ok=True)
        
        # Create backup filename with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = backup_dir / f'dreams_backup_{timestamp}.json'
        
        try:
            # Copy the data file
            import shutil
            shutil.copy2(data_file, backup_file)
            
            # Clean up old backups
            self._cleanup_old_backups(backup_dir)
            
            print(f"Backup created: {backup_file}")
        except Exception as e:
            print(f"Error creating backup: {e}")
    
    def _cleanup_old_backups(self, backup_dir: Path):
        """Remove old backup files"""
        max_backups = self.get('max_backups', 7)
        
        # Get all backup files
        backup_files = sorted(backup_dir.glob('dreams_backup_*.json'))
        
        # Remove excess files
        while len(backup_files) > max_backups:
            oldest_backup = backup_files.pop(0)
            try:
                oldest_backup.unlink()
                print(f"Removed old backup: {oldest_backup}")
            except Exception as e:
                print(f"Error removing old backup: {e}")
    
    def reset_to_defaults(self):
        """Reset configuration to default values"""
        self.config = self.default_config.copy()
        self.save_config()
        print("Configuration reset to defaults.")
    
    def export_config(self, filename: str):
        """Export current configuration to a file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"Configuration exported to {filename}")
        except Exception as e:
            print(f"Error exporting configuration: {e}")
    
    def import_config(self, filename: str):
        """Import configuration from a file"""
        try:
            with open(filename, 'r') as f:
                imported_config = json.load(f)
            
            self.config = self._merge_config(self.default_config, imported_config)
            self.save_config()
            print(f"Configuration imported from {filename}")
        except Exception as e:
            print(f"Error importing configuration: {e}")
    
    def show_config(self):
        """Display current configuration"""
        print("\n🔧 Current Configuration:")
        print("=" * 30)
        self._print_config(self.config)
    
    def _print_config(self, config: Dict[str, Any], indent: int = 0):
        """Recursively print configuration"""
        for key, value in config.items():
            if isinstance(value, dict):
                print("  " * indent + f"{key}:")
                self._print_config(value, indent + 1)
            else:
                print("  " * indent + f"{key}: {value}")
    
    def validate_config(self) -> bool:
        """Validate configuration settings"""
        errors = []
        
        # Check data file
        data_file = self.data_file
        if not data_file.endswith('.json'):
            errors.append("Data file must be a .json file")
        
        # Check backup settings
        if self.backup_enabled:
            max_backups = self.get('max_backups', 7)
            if not isinstance(max_backups, int) or max_backups < 1:
                errors.append("max_backups must be a positive integer")
        
        # Check visualization settings
        chart_size = self.get('visualization.default_chart_size', [12, 8])
        if not isinstance(chart_size, list) or len(chart_size) != 2:
            errors.append("visualization.default_chart_size must be a list of 2 numbers")
        
        # Check analysis settings
        min_dreams = self.get('analysis.min_dreams_for_analysis', 5)
        if not isinstance(min_dreams, int) or min_dreams < 1:
            errors.append("analysis.min_dreams_for_analysis must be a positive integer")
        
        if errors:
            print("❌ Configuration validation errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        print("✅ Configuration is valid")
        return True