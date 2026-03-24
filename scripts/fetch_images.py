#!/usr/bin/env python3
"""Fetch exercise demonstration images from musclewiki.wiki"""

import argparse
import re
import time
from pathlib import Path


def sanitize_filename(name: str) -> str:
    """Convert exercise name to filename format."""
    filename = re.sub(r"[^\w\s-]", "", name.lower())
    filename = re.sub(r"[-\s]+", "-", filename)
    return filename.strip("-")


def fetch_image(exercise_name: str, images_dir: Path, force: bool = False) -> Path:
    """Fetch exercise image (placeholder implementation)."""
    filename = sanitize_filename(exercise_name)
    image_path = images_dir / f"{filename}.png"

    if image_path.exists() and not force:
        print(f"Image already exists: {image_path}")
        return image_path

    # Placeholder: create empty file
    image_path.touch()
    print(f"Created placeholder: {image_path}")

    return image_path


def fetch_all_images(exercises_dir: Path, images_dir: Path, force: bool = False):
    """Fetch images for all exercises."""
    if not exercises_dir.exists():
        print(f"Exercises directory not found: {exercises_dir}")
        return

    images_dir.mkdir(parents=True, exist_ok=True)

    exercise_files = list(exercises_dir.glob("*.md"))
    print(f"Found {len(exercise_files)} exercises")

    for exercise_file in exercise_files:
        exercise_name = exercise_file.stem
        try:
            fetch_image(exercise_name, images_dir, force)
            time.sleep(0.1)
        except Exception as e:
            print(f"Error fetching {exercise_name}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Fetch exercise images")
    parser.add_argument("--exercise", help="Specific exercise to fetch")
    parser.add_argument("--all", action="store_true", help="Fetch all images")
    parser.add_argument("--force", action="store_true", help="Overwrite existing")

    args = parser.parse_args()

    vault_dir = Path(__file__).parent.parent
    exercises_dir = vault_dir / "exercises"
    images_dir = vault_dir / "images" / "exercises"

    if args.exercise:
        images_dir.mkdir(parents=True, exist_ok=True)
        fetch_image(args.exercise, images_dir, args.force)
    elif args.all:
        fetch_all_images(exercises_dir, images_dir, args.force)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
