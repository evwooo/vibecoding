# 🌙 Dream Journal Analyzer

A comprehensive Python application for logging, analyzing, and visualizing your dreams to gain insights into your subconscious mind.

## ✨ Features

- **Dream Logging**: Record dreams with detailed metadata including emotions, characters, themes, and special flags
- **Pattern Analysis**: Discover trends in your dreams over time
- **Visualization**: Generate beautiful charts and graphs of your dream data
- **Search & Filter**: Find specific dreams by content, emotions, themes, or characters
- **Export Data**: Export your dreams to JSON or CSV formats
- **Comprehensive Reports**: Generate detailed analysis reports with insights and recommendations
- **Interactive CLI**: Both command-line and interactive modes for easy usage
- **Backup System**: Automatic backups of your dream data
- **Configuration**: Customizable settings for personalization

## 🚀 Installation

1. Clone or download the project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📖 Usage

### Command Line Interface

#### Adding Dreams
```bash
python main.py add "Flying Dream" "I was flying over the city" --emotions happy excited free --themes flight adventure --characters myself --lucid
```

#### Listing Dreams
```bash
python main.py list --limit 5
python main.py list --search "flying"
```

#### Viewing Specific Dream
```bash
python main.py view 1
```

#### Analyzing Patterns
```bash
python main.py analyze
```

#### Generating Reports
```bash
python main.py report
```

#### Exporting Data
```bash
python main.py export --format json
python main.py export --format csv
```

### Interactive Mode

For a more user-friendly experience:
```bash
python main.py interactive
```

This opens an interactive session where you can:
- Add dreams with guided prompts
- List recent dreams
- Analyze patterns
- Get help with commands

## 📊 Analysis Features

### Pattern Detection
- **Emotional Trends**: Track how your emotions change over time
- **Recurring Themes**: Identify themes that appear frequently
- **Character Analysis**: See which people appear most often in your dreams
- **Temporal Patterns**: Discover when you dream most frequently

### Insights Generated
- Total dreams logged and frequency statistics
- Percentage of lucid dreams and nightmares
- Most common emotions, themes, and characters
- Emotional trend analysis over time
- Monthly dreaming patterns
- Content analysis and word frequency

### Visualizations
- Emotion frequency bar charts
- Theme distribution pie charts
- Dream frequency timelines
- Dream type comparisons (normal, lucid, nightmare)
- Monthly trend analysis
- Character frequency charts
- Comprehensive dashboard

## 🗂️ Data Structure

Each dream entry contains:
- **Title**: Brief description of the dream
- **Content**: Detailed dream narrative
- **Date**: Automatic timestamp
- **Emotions**: List of emotions experienced
- **Characters**: People/entities in the dream
- **Themes**: Main topics or concepts
- **Lucid**: Flag for lucid dreams
- **Nightmare**: Flag for nightmares
- **ID**: Unique identifier

## 🔧 Configuration

The application uses a `config.json` file for customization:

```json
{
  "data_file": "dreams.json",
  "backup_enabled": true,
  "max_backups": 7,
  "visualization": {
    "default_chart_size": [12, 8],
    "save_charts": true,
    "chart_directory": "charts"
  },
  "analysis": {
    "min_dreams_for_analysis": 5,
    "pattern_threshold": 0.3
  }
}
```

## 📁 Project Structure

```
dream_journal_analyzer/
├── main.py              # Main application entry point
├── dream_models.py      # Data models (Dream, DreamJournal)
├── analyzer.py          # Pattern analysis and insights
├── visualizer.py        # Chart generation and visualization
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── dreams.json         # Your dream data (created automatically)
└── config.json         # Configuration file (created automatically)
```

## 🔍 Example Usage Session

```bash
# Start interactive mode
python main.py interactive

# Add a dream
> add
Dream title: Underwater Adventure
Dream content: I was swimming in crystal clear water with colorful fish...
Emotions: peaceful, wonder, calm
Characters: myself, dolphins
Themes: water, nature, exploration
Was this a lucid dream? n
Was this a nightmare? n
✨ Dream 'Underwater Adventure' added successfully!

# List recent dreams
> list
📚 Recent Dreams:
==================================================
1. Underwater Adventure
   Date: 2024-01-15 10:30
   Emotions: peaceful, wonder, calm
   Themes: water, nature, exploration

# Analyze patterns
> analyze
🔍 Analyzing your dream patterns...
📊 Dream Analysis Results:
==================================================
Total dreams logged: 5
Average dreams per month: 2.5
Top emotions: peaceful, wonder, happy
Top themes: water, nature, adventure
Lucid dreams: 20.0%
Nightmares: 0.0%
```

## 📈 Sample Analysis Output

```
🌙 DREAM JOURNAL ANALYSIS REPORT 🌙
==================================================
Generated on: 2024-01-15 10:30:45

📊 BASIC STATISTICS
--------------------
Total dreams logged: 25
Average dreams per month: 4.2
Most active period: 2024-01 (12 dreams)
Lucid dreams: 16.0%
Nightmares: 8.0%

😊 EMOTIONAL ANALYSIS
--------------------
Top emotions: peaceful, happy, excited, curious, wonder
Emotional trends: Increasing: peaceful, calm; Decreasing: anxious

🎭 THEMATIC ANALYSIS
--------------------
Top themes: nature, adventure, water, flying, family
Recurring themes: nature, water, flying

👥 CHARACTER ANALYSIS
--------------------
Most common characters: myself, family, friends, strangers

📝 CONTENT PATTERNS
--------------------
Average dream length: 45.3 words
Common words: water, flying, house, running, beautiful
Common settings: house, forest, beach, school

💡 RECOMMENDATIONS
--------------------
• Keep logging dreams for better pattern analysis
• Consider practicing lucid dreaming techniques
```

## 🎯 Benefits

- **Self-Discovery**: Understand your subconscious patterns and themes
- **Memory Enhancement**: Regular dream logging improves dream recall
- **Stress Monitoring**: Track emotional patterns to identify stress indicators
- **Lucid Dream Training**: Monitor progress in lucid dreaming practice
- **Creative Inspiration**: Use dream themes for creative projects
- **Personal Growth**: Gain insights into your fears, desires, and aspirations

## 🛠️ Technical Details

- **Language**: Python 3.7+
- **Dependencies**: matplotlib, numpy, python-dateutil
- **Data Storage**: JSON format for easy portability
- **Visualization**: matplotlib for charts and graphs
- **CLI**: argparse for command-line interface
- **Configuration**: JSON-based configuration system

## 🔒 Privacy & Security

- All data is stored locally on your machine
- No internet connection required
- Automatic backup system to prevent data loss
- Export functionality for data portability

## 🤝 Contributing

This is an original project created as a unique Python application. Feel free to extend it with additional features like:
- Web interface
- Mobile app companion
- Advanced NLP analysis
- Dream sharing capabilities
- Integration with sleep tracking devices

## 📜 License

This project is open source and available under the MIT License.

## 🌟 Getting Started

1. Install the dependencies: `pip install -r requirements.txt`
2. Run the application: `python main.py interactive`
3. Start logging your dreams!
4. After logging several dreams, run `python main.py analyze` to see patterns

Happy dreaming! 🌙✨