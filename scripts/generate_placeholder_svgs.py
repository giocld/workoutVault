#!/usr/bin/env python3
"""Generate simple SVG placeholder images for exercises"""

import argparse
import re
from pathlib import Path


def sanitize_filename(name: str) -> str:
    """Convert exercise name to filename format."""
    filename = re.sub(r"[^\w\s-]", "", name.lower())
    filename = re.sub(r"[-\s]+", "-", filename)
    return filename.strip("-")


def get_muscle_group_color(exercise_name):
    """Return color based on muscle group keywords"""
    name_lower = exercise_name.lower()

    if any(word in name_lower for word in ["bench", "chest", "fly", "press"]):
        return "#FF6B6B"  # Red - chest
    elif any(word in name_lower for word in ["curl", "bicep", "hammer"]):
        return "#4ECDC4"  # Teal - biceps
    elif any(
        word in name_lower
        for word in ["tricep", "extension", "pushdown", "skullcrusher", "dip"]
    ):
        return "#95E1D3"  # Mint - triceps
    elif any(word in name_lower for word in ["row", "pull", "lat", "back"]):
        return "#A8E6CF"  # Green - back
    elif any(word in name_lower for word in ["shoulder", "raise", "press", "shrug"]):
        return "#FFD93D"  # Yellow - shoulders
    else:
        return "#6C5CE7"  # Purple - default


def generate_svg(exercise_name, muscle_group=None):
    """Generate an SVG placeholder image for an exercise"""

    color = get_muscle_group_color(exercise_name)

    # Shorten name if too long
    display_name = exercise_name
    if len(display_name) > 25:
        display_name = display_name[:22] + "..."

    # Split into lines if needed
    words = display_name.split()
    if len(words) > 3:
        mid = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])
        text_svg = f"""<text x="200" y="180" font-family="Arial, sans-serif" font-size="28" fill="white" text-anchor="middle" font-weight="bold">{line1}</text>
        <text x="200" y="220" font-family="Arial, sans-serif" font-size="28" fill="white" text-anchor="middle" font-weight="bold">{line2}</text>"""
    else:
        text_svg = f"""<text x="200" y="200" font-family="Arial, sans-serif" font-size="32" fill="white" text-anchor="middle" font-weight="bold">{display_name}</text>"""

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
            <stop offset="100%" style="stop-color:#2D3436;stop-opacity:1" />
        </linearGradient>
    </defs>
    
    <!-- Background -->
    <rect width="400" height="300" fill="url(#grad1)"/>
    
    <!-- Border -->
    <rect x="10" y="10" width="380" height="280" fill="none" stroke="white" stroke-width="3" rx="10"/>
    
    <!-- Dumbbell icon -->
    <g transform="translate(200, 80)" fill="white" opacity="0.3">
        <rect x="-60" y="-8" width="30" height="16" rx="3"/>
        <rect x="30" y="-8" width="30" height="16" rx="3"/>
        <rect x="-30" y="-3" width="60" height="6" rx="2"/>
    </g>
    
    <!-- Exercise name -->
    {text_svg}
    
    <!-- Subtle watermark -->
    <text x="200" y="280" font-family="Arial, sans-serif" font-size="12" fill="white" text-anchor="middle" opacity="0.5">Workout Tracker</text>
</svg>"""

    return svg


def generate_all_images(exercises_dir, images_dir, force=False):
    """Generate SVG images for all exercises"""

    images_dir.mkdir(parents=True, exist_ok=True)
    exercise_files = sorted(exercises_dir.glob("*.md"))

    print(f"Generating images for {len(exercise_files)} exercises...")
    print()

    success_count = 0

    for i, exercise_file in enumerate(exercise_files, 1):
        # Read exercise name
        try:
            content = exercise_file.read_text()
            match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
            if match:
                exercise_name = match.group(1).strip()
            else:
                exercise_name = exercise_file.stem.replace("-", " ").title()
        except:
            exercise_name = exercise_file.stem.replace("-", " ").title()

        filename = sanitize_filename(exercise_name)
        image_path = images_dir / f"{filename}.svg"

        if image_path.exists() and not force:
            print(f"[{i}/{len(exercise_files)}] {exercise_name} - ✓ exists")
            success_count += 1
            continue

        # Generate SVG
        svg_content = generate_svg(exercise_name)
        image_path.write_text(svg_content)

        print(f"[{i}/{len(exercise_files)}] {exercise_name} - ✓ generated")
        success_count += 1

    print()
    print(f"=== Results ===")
    print(f"Generated: {success_count}")
    print(f"Total: {len(exercise_files)}")
    print()
    print("Note: These are placeholder SVG images.")
    print("Replace them with real photos when available.")


def main():
    parser = argparse.ArgumentParser(description="Generate SVG placeholder images")
    parser.add_argument("--all", action="store_true", help="Generate all images")
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing images"
    )

    args = parser.parse_args()

    if args.all:
        vault_dir = Path(__file__).parent.parent
        exercises_dir = vault_dir / "exercises"
        images_dir = vault_dir / "images" / "exercises"

        generate_all_images(exercises_dir, images_dir, args.force)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
