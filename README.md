# Workout Tracker

An Obsidian-based workout tracking system for mobile usage with automatic exercise image fetching and git sync.

## Features

- **Exercise Library**: 150+ exercises across all muscle groups
- **Muscle Group Organization**: Hierarchical structure with core/accessory classification
- **Smart Rotation**: Automatically suggests exercises you haven't done recently
- **Mobile First**: Works seamlessly on phone with git sync
- **Local Images**: Exercise demonstration images stored locally for offline access
- **Flexible Logging**: Log during workout, sync after

## Quick Start

1. **Setup**: See [SETUP.md](SETUP.md) for installation and configuration
2. **Create Exercise**: `python scripts/create_exercise.py --name "New Exercise" --movement "movement-name"`
3. **Start Workout**: Create new workout note from template
4. **Log Sets**: Create exercise log notes during workout
5. **Sync**: Run `./scripts/sync.sh` or use auto-sync

## Structure

- `muscle-groups/`: Index files for each muscle group (Chest, Shoulders, Triceps, Back, Biceps)
- `exercises/`: 150+ exercise files (30+ per muscle group)
- `logs/`: Individual exercise logs by date
- `workouts/`: Daily workout summaries
- `images/exercises/`: Exercise demonstration images
- `scripts/`: Automation scripts
- `templates/`: Note templates

## Exercise Library

### Push Day Muscles
- **Chest**: 30+ exercises (barbell, dumbbell, cable, machine, bodyweight)
- **Shoulders**: 30+ exercises (front, side, rear delts)
- **Triceps**: 30+ exercises (all heads and angles)

### Pull Day Muscles
- **Back**: 30+ exercises (lats, rhomboids, traps, lower back)
- **Biceps**: 30+ exercises (short head, long head, brachialis)

## Dependencies

- Obsidian (mobile and desktop)
- Dataview plugin
- Python 3.8+
- Git
