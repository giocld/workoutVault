#!/usr/bin/env python3
"""Create a new exercise note from template."""

import re
import argparse
from pathlib import Path
from string import Template


def sanitize_filename(name: str) -> str:
    """Convert exercise name to filename format."""
    filename = re.sub(r"[^\w\s-]", "", name.lower())
    filename = re.sub(r"[-\s]+", "-", filename)
    return filename.strip("-")


def create_exercise(
    name: str, movement: str, templates_dir: Path = None, exercises_dir: Path = None
) -> Path:
    """Create a new exercise note from template."""

    if templates_dir is None:
        templates_dir = Path(__file__).parent.parent / "templates"
    if exercises_dir is None:
        exercises_dir = Path(__file__).parent.parent / "exercises"

    filename = sanitize_filename(name)
    exercise_path = exercises_dir / f"{filename}.md"

    if exercise_path.exists():
        raise FileExistsError(f"Exercise already exists: {exercise_path}")

    template_path = templates_dir / "exercise.md"
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    template_content = template_path.read_text()

    content = template_content.replace("{{name}}", name)
    content = content.replace("{{filename}}", filename)
    content = content.replace("{{movement}}", movement)

    exercise_path.write_text(content)
    print(f"Created exercise: {exercise_path}")

    return exercise_path


def main():
    parser = argparse.ArgumentParser(description="Create a new exercise note")
    parser.add_argument("--name", required=True, help="Exercise name")
    parser.add_argument("--movement", required=True, help="Movement type")

    args = parser.parse_args()

    try:
        create_exercise(args.name, args.movement)
    except FileExistsError as e:
        print(f"Error: {e}")
        exit(1)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
