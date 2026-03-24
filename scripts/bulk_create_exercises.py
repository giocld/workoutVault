#!/usr/bin/env python3
"""Bulk create exercises with full metadata."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from create_exercise import create_exercise, sanitize_filename
import re

# Define 30+ exercises per muscle group
EXERCISES = {
    "chest": [
        # Barbell
        (
            "Bench Press Barbell",
            "bench-press",
            ["barbell", "bench"],
            "core",
            ["bench-press-dumbbell", "incline-press-barbell"],
        ),
        (
            "Incline Bench Press Barbell",
            "incline-bench-press",
            ["barbell", "bench"],
            "core",
            ["incline-bench-press-dumbbell", "bench-press-barbell"],
        ),
        (
            "Decline Bench Press Barbell",
            "decline-bench-press",
            ["barbell", "bench"],
            "accessory",
            ["decline-bench-press-dumbbell"],
        ),
        (
            "Close Grip Bench Press",
            "close-grip-bench-press",
            ["barbell", "bench"],
            "accessory",
            ["bench-press-barbell"],
        ),
        (
            "Reverse Grip Bench Press",
            "reverse-grip-bench-press",
            ["barbell", "bench"],
            "accessory",
            [],
        ),
        (
            "Floor Press",
            "floor-press",
            ["barbell"],
            "accessory",
            ["bench-press-barbell"],
        ),
        # Dumbbell
        (
            "Bench Press Dumbbell",
            "bench-press",
            ["dumbbells", "bench"],
            "core",
            ["bench-press-barbell", "incline-press-dumbbell"],
        ),
        (
            "Incline Bench Press Dumbbell",
            "incline-bench-press",
            ["dumbbells", "bench"],
            "core",
            ["incline-bench-press-barbell", "bench-press-dumbbell"],
        ),
        (
            "Decline Bench Press Dumbbell",
            "decline-bench-press",
            ["dumbbells", "bench"],
            "accessory",
            ["decline-bench-press-barbell"],
        ),
        (
            "Dumbbell Pullover",
            "dumbbell-pullover",
            ["dumbbells", "bench"],
            "accessory",
            [],
        ),
        ("Svend Press", "svend-press", ["dumbbells"], "accessory", []),
        (
            "Dumbbell Squeeze Press",
            "dumbbell-squeeze-press",
            ["dumbbells", "bench"],
            "accessory",
            ["bench-press-dumbbell"],
        ),
        # Flyes
        (
            "Dumbbell Fly",
            "dumbbell-fly",
            ["dumbbells", "bench"],
            "accessory",
            ["cable-fly", "pec-deck-fly"],
        ),
        (
            "Incline Dumbbell Fly",
            "incline-dumbbell-fly",
            ["dumbbells", "bench"],
            "accessory",
            ["dumbbell-fly"],
        ),
        (
            "Cable Fly",
            "cable-fly",
            ["cable"],
            "accessory",
            ["dumbbell-fly", "pec-deck-fly"],
        ),
        ("Low Cable Fly", "low-cable-fly", ["cable"], "accessory", ["cable-fly"]),
        ("High Cable Fly", "high-cable-fly", ["cable"], "accessory", ["cable-fly"]),
        ("Pec Deck Fly", "pec-deck-fly", ["machine"], "accessory", ["cable-fly"]),
        (
            "Single Arm Cable Fly",
            "single-arm-cable-fly",
            ["cable"],
            "accessory",
            ["cable-fly"],
        ),
        # Bodyweight
        (
            "Push Up",
            "push-up",
            ["bodyweight"],
            "core",
            ["diamond-push-up", "incline-push-up"],
        ),
        (
            "Diamond Push Up",
            "diamond-push-up",
            ["bodyweight"],
            "accessory",
            ["push-up", "close-grip-bench-press"],
        ),
        (
            "Incline Push Up",
            "incline-push-up",
            ["bodyweight"],
            "accessory",
            ["push-up", "decline-push-up"],
        ),
        (
            "Decline Push Up",
            "decline-push-up",
            ["bodyweight"],
            "accessory",
            ["push-up", "incline-push-up"],
        ),
        (
            "Wide Grip Push Up",
            "wide-grip-push-up",
            ["bodyweight"],
            "accessory",
            ["push-up"],
        ),
        ("Archer Push Up", "archer-push-up", ["bodyweight"], "accessory", ["push-up"]),
        (
            "Plyometric Push Up",
            "plyometric-push-up",
            ["bodyweight"],
            "accessory",
            ["push-up"],
        ),
        (
            "Dips Chest Focus",
            "dips-chest",
            ["bodyweight", "dip-bars"],
            "core",
            ["bench-press-barbell"],
        ),
        # Machines
        (
            "Chest Press Machine",
            "chest-press-machine",
            ["machine"],
            "accessory",
            ["bench-press-barbell"],
        ),
        (
            "Incline Chest Press Machine",
            "incline-chest-press-machine",
            ["machine"],
            "accessory",
            ["incline-bench-press-barbell"],
        ),
        (
            "Hammer Strength Press",
            "hammer-strength-press",
            ["machine"],
            "accessory",
            ["bench-press-barbell"],
        ),
        # Specialty
        (
            "Landmine Press",
            "landmine-press",
            ["barbell"],
            "accessory",
            ["bench-press-barbell"],
        ),
        ("Plate Press", "plate-press", ["weight-plate"], "accessory", ["svend-press"]),
    ],
    "shoulders": [
        # Overhead Press
        (
            "Overhead Press Barbell",
            "overhead-press",
            ["barbell"],
            "core",
            ["overhead-press-dumbbell", "push-press"],
        ),
        (
            "Overhead Press Dumbbell",
            "overhead-press",
            ["dumbbells"],
            "core",
            ["overhead-press-barbell", "arnold-press"],
        ),
        (
            "Push Press",
            "push-press",
            ["barbell"],
            "accessory",
            ["overhead-press-barbell"],
        ),
        (
            "Arnold Press",
            "arnold-press",
            ["dumbbells"],
            "accessory",
            ["overhead-press-dumbbell"],
        ),
        (
            "Landmine Press",
            "landmine-press-shoulders",
            ["barbell"],
            "accessory",
            ["overhead-press-barbell"],
        ),
        ("Z Press", "z-press", ["barbell"], "accessory", ["overhead-press-barbell"]),
        (
            "Seated Overhead Press Barbell",
            "seated-overhead-press",
            ["barbell", "bench"],
            "accessory",
            ["overhead-press-barbell"],
        ),
        (
            "Seated Overhead Press Dumbbell",
            "seated-overhead-press-dumbbell",
            ["dumbbells", "bench"],
            "accessory",
            ["overhead-press-dumbbell"],
        ),
        # Lateral Raises
        (
            "Lateral Raise Dumbbell",
            "lateral-raise",
            ["dumbbells"],
            "core",
            ["lateral-raise-cable", "upright-row"],
        ),
        (
            "Lateral Raise Cable",
            "lateral-raise-cable",
            ["cable"],
            "accessory",
            ["lateral-raise-dumbbell"],
        ),
        (
            "Lateral Raise Machine",
            "lateral-raise-machine",
            ["machine"],
            "accessory",
            ["lateral-raise-dumbbell"],
        ),
        (
            "Leaning Lateral Raise",
            "leaning-lateral-raise",
            ["dumbbells"],
            "accessory",
            ["lateral-raise-dumbbell"],
        ),
        (
            "Single Arm Lateral Raise",
            "single-arm-lateral-raise",
            ["dumbbells"],
            "accessory",
            ["lateral-raise-dumbbell"],
        ),
        (
            "Around The World",
            "around-the-world",
            ["dumbbells"],
            "accessory",
            ["lateral-raise-dumbbell"],
        ),
        # Front Raises
        (
            "Front Raise Dumbbell",
            "front-raise",
            ["dumbbells"],
            "accessory",
            ["front-raise-cable", "overhead-press"],
        ),
        (
            "Front Raise Cable",
            "front-raise-cable",
            ["cable"],
            "accessory",
            ["front-raise-dumbbell"],
        ),
        (
            "Front Raise Plate",
            "front-raise-plate",
            ["weight-plate"],
            "accessory",
            ["front-raise-dumbbell"],
        ),
        (
            "Alternating Front Raise",
            "alternating-front-raise",
            ["dumbbells"],
            "accessory",
            ["front-raise-dumbbell"],
        ),
        # Rear Delts
        (
            "Face Pull",
            "face-pull",
            ["cable"],
            "core",
            ["reverse-pec-deck", "bent-over-fly"],
        ),
        (
            "Reverse Pec Deck",
            "reverse-pec-deck",
            ["machine"],
            "core",
            ["face-pull", "bent-over-fly"],
        ),
        (
            "Bent Over Fly Dumbbell",
            "bent-over-fly",
            ["dumbbells"],
            "accessory",
            ["face-pull", "reverse-pec-deck"],
        ),
        (
            "Bent Over Fly Cable",
            "bent-over-fly-cable",
            ["cable"],
            "accessory",
            ["bent-over-fly-dumbbell"],
        ),
        ("Rear Delt Row", "rear-delt-row", ["dumbbells"], "accessory", ["face-pull"]),
        ("High Row", "high-row", ["cable"], "accessory", ["face-pull"]),
        # Upright Row & Traps
        (
            "Upright Row Barbell",
            "upright-row",
            ["barbell"],
            "accessory",
            ["upright-row-dumbbell", "lateral-raise"],
        ),
        (
            "Upright Row Dumbbell",
            "upright-row-dumbbell",
            ["dumbbells"],
            "accessory",
            ["upright-row-barbell"],
        ),
        (
            "Upright Row Cable",
            "upright-row-cable",
            ["cable"],
            "accessory",
            ["upright-row-barbell"],
        ),
        (
            "Shrug Barbell",
            "shrug-barbell",
            ["barbell"],
            "accessory",
            ["shrug-dumbbell"],
        ),
        (
            "Shrug Dumbbell",
            "shrug-dumbbell",
            ["dumbbells"],
            "accessory",
            ["shrug-barbell"],
        ),
    ],
    "triceps": [
        # Pushdowns
        (
            "Tricep Pushdown Rope",
            "tricep-pushdown",
            ["cable"],
            "core",
            ["tricep-pushdown-bar", "tricep-pushdown-vbar"],
        ),
        (
            "Tricep Pushdown Bar",
            "tricep-pushdown-bar",
            ["cable"],
            "accessory",
            ["tricep-pushdown-rope"],
        ),
        (
            "Tricep Pushdown V Bar",
            "tricep-pushdown-vbar",
            ["cable"],
            "accessory",
            ["tricep-pushdown-rope"],
        ),
        (
            "Reverse Grip Pushdown",
            "reverse-grip-pushdown",
            ["cable"],
            "accessory",
            ["tricep-pushdown"],
        ),
        (
            "Single Arm Pushdown",
            "single-arm-pushdown",
            ["cable"],
            "accessory",
            ["tricep-pushdown"],
        ),
        # Overhead Extensions
        (
            "Overhead Tricep Extension Dumbbell",
            "overhead-tricep-extension",
            ["dumbbells"],
            "core",
            ["overhead-tricep-extension-cable", "skullcrusher"],
        ),
        (
            "Overhead Tricep Extension Cable",
            "overhead-tricep-extension-cable",
            ["cable"],
            "accessory",
            ["overhead-tricep-extension-dumbbell"],
        ),
        (
            "Overhead Tricep Extension Rope",
            "overhead-tricep-extension-rope",
            ["cable"],
            "accessory",
            ["overhead-tricep-extension"],
        ),
        (
            "Single Arm Overhead Extension",
            "single-arm-overhead-extension",
            ["dumbbells"],
            "accessory",
            ["overhead-tricep-extension"],
        ),
        (
            "French Press",
            "french-press",
            ["barbell", "bench"],
            "accessory",
            ["skullcrusher"],
        ),
        # Lying Extensions
        (
            "Skullcrusher Barbell",
            "skullcrusher",
            ["barbell", "bench"],
            "core",
            ["skullcrusher-dumbbell", "close-grip-bench-press"],
        ),
        (
            "Skullcrusher Dumbbell",
            "skullcrusher-dumbbell",
            ["dumbbells", "bench"],
            "accessory",
            ["skullcrusher-barbell"],
        ),
        (
            "Decline Skullcrusher",
            "decline-skullcrusher",
            ["barbell", "bench"],
            "accessory",
            ["skullcrusher"],
        ),
        # Compound
        (
            "Close Grip Bench Press",
            "close-grip-bench-press-triceps",
            ["barbell", "bench"],
            "core",
            ["bench-press-barbell", "dip"],
        ),
        (
            "Close Grip Push Up",
            "close-grip-push-up",
            ["bodyweight"],
            "accessory",
            ["push-up", "close-grip-bench-press"],
        ),
        (
            "Dip",
            "dip",
            ["bodyweight", "dip-bars"],
            "core",
            ["close-grip-bench-press", "tricep-pushdown"],
        ),
        ("Bench Dip", "bench-dip", ["bodyweight", "bench"], "accessory", ["dip"]),
        # Kickbacks
        (
            "Tricep Kickback Dumbbell",
            "tricep-kickback",
            ["dumbbells", "bench"],
            "accessory",
            ["tricep-pushdown"],
        ),
        (
            "Tricep Kickback Cable",
            "tricep-kickback-cable",
            ["cable"],
            "accessory",
            ["tricep-kickback-dumbbell"],
        ),
        (
            "Cross Body Tricep Extension",
            "cross-body-tricep-extension",
            ["cable"],
            "accessory",
            ["tricep-pushdown"],
        ),
        # Specialty
        (
            "JM Press",
            "jm-press",
            ["barbell", "bench"],
            "accessory",
            ["skullcrusher", "close-grip-bench-press"],
        ),
        (
            "Tate Press",
            "tate-press",
            ["dumbbells", "bench"],
            "accessory",
            ["skullcrusher-dumbbell"],
        ),
        (
            "Cable Lying Tricep Extension",
            "cable-lying-tricep-extension",
            ["cable"],
            "accessory",
            ["skullcrusher"],
        ),
        (
            "Tiger Bend Push Up",
            "tiger-bend-push-up",
            ["bodyweight"],
            "accessory",
            ["push-up"],
        ),
        ("Tricep Machine Dip", "tricep-machine-dip", ["machine"], "accessory", ["dip"]),
    ],
    "back": [
        # Vertical Pull
        (
            "Pull Up",
            "pull-up",
            ["bodyweight", "pull-up-bar"],
            "core",
            ["lat-pulldown", "chin-up"],
        ),
        (
            "Chin Up",
            "chin-up",
            ["bodyweight", "pull-up-bar"],
            "core",
            ["pull-up", "lat-pulldown"],
        ),
        (
            "Neutral Grip Pull Up",
            "neutral-grip-pull-up",
            ["bodyweight", "pull-up-bar"],
            "core",
            ["pull-up"],
        ),
        (
            "Wide Grip Pull Up",
            "wide-grip-pull-up",
            ["bodyweight", "pull-up-bar"],
            "accessory",
            ["pull-up"],
        ),
        (
            "Commando Pull Up",
            "commando-pull-up",
            ["bodyweight", "pull-up-bar"],
            "accessory",
            ["pull-up"],
        ),
        ("Lat Pulldown", "lat-pulldown", ["machine"], "core", ["pull-up", "chin-up"]),
        (
            "Close Grip Lat Pulldown",
            "close-grip-lat-pulldown",
            ["machine"],
            "accessory",
            ["lat-pulldown"],
        ),
        (
            "Single Arm Lat Pulldown",
            "single-arm-lat-pulldown",
            ["machine"],
            "accessory",
            ["lat-pulldown"],
        ),
        (
            "Straight Arm Pulldown",
            "straight-arm-pulldown",
            ["cable"],
            "accessory",
            ["lat-pulldown"],
        ),
        # Horizontal Pull
        (
            "Barbell Row",
            "barbell-row",
            ["barbell"],
            "core",
            ["dumbbell-row", "cable-row"],
        ),
        ("Pendlay Row", "pendlay-row", ["barbell"], "core", ["barbell-row"]),
        ("Yates Row", "yates-row", ["barbell"], "accessory", ["barbell-row"]),
        (
            "Dumbbell Row",
            "dumbbell-row",
            ["dumbbells", "bench"],
            "core",
            ["barbell-row", "cable-row"],
        ),
        (
            "Chest Supported Row",
            "chest-supported-row",
            ["dumbbells", "bench"],
            "accessory",
            ["dumbbell-row"],
        ),
        ("Seal Row", "seal-row", ["barbell", "bench"], "accessory", ["barbell-row"]),
        ("Cable Row", "cable-row", ["cable"], "core", ["barbell-row", "machine-row"]),
        ("Machine Row", "machine-row", ["machine"], "accessory", ["cable-row"]),
        ("T Bar Row", "t-bar-row", ["barbell", "landmine"], "core", ["barbell-row"]),
        (
            "Meadows Row",
            "meadows-row",
            ["barbell", "landmine"],
            "accessory",
            ["t-bar-row"],
        ),
        # Upper Back
        ("Face Pull", "face-pull-back", ["cable"], "core", ["reverse-pec-deck"]),
        (
            "Reverse Pec Deck",
            "reverse-pec-deck-back",
            ["machine"],
            "accessory",
            ["face-pull"],
        ),
        (
            "Rear Delt Row",
            "rear-delt-row-back",
            ["dumbbells"],
            "accessory",
            ["face-pull"],
        ),
        ("High Row", "high-row-back", ["cable"], "accessory", ["face-pull"]),
        (
            "Chest Supported Reverse Fly",
            "chest-supported-reverse-fly",
            ["dumbbells", "bench"],
            "accessory",
            ["reverse-pec-deck"],
        ),
        # Traps & Upper
        (
            "Shrug Barbell",
            "shrug-barbell-back",
            ["barbell"],
            "accessory",
            ["shrug-dumbbell"],
        ),
        (
            "Shrug Dumbbell",
            "shrug-dumbbell-back",
            ["dumbbells"],
            "accessory",
            ["shrug-barbell"],
        ),
        ("Farmer Walk", "farmer-walk", ["dumbbells"], "accessory", []),
        ("Rack Pull", "rack-pull", ["barbell"], "accessory", ["deadlift"]),
        ("Deadlift", "deadlift", ["barbell"], "accessory", ["rack-pull"]),
        # Lower Back
        (
            "Back Extension",
            "back-extension",
            ["bodyweight", "back-extension-bench"],
            "accessory",
            ["good-morning"],
        ),
        ("Good Morning", "good-morning", ["barbell"], "accessory", ["back-extension"]),
        (
            "Reverse Hyper",
            "reverse-hyper",
            ["machine"],
            "accessory",
            ["back-extension"],
        ),
    ],
    "biceps": [
        # Barbell Curls
        (
            "Barbell Curl",
            "barbell-curl",
            ["barbell"],
            "core",
            ["dumbbell-curl", "ez-bar-curl"],
        ),
        ("EZ Bar Curl", "ez-bar-curl", ["ez-bar"], "core", ["barbell-curl"]),
        ("Drag Curl", "drag-curl", ["barbell"], "accessory", ["barbell-curl"]),
        (
            "Wide Grip Barbell Curl",
            "wide-grip-barbell-curl",
            ["barbell"],
            "accessory",
            ["barbell-curl"],
        ),
        (
            "Close Grip Barbell Curl",
            "close-grip-barbell-curl",
            ["barbell"],
            "accessory",
            ["barbell-curl"],
        ),
        # Dumbbell Curls
        (
            "Dumbbell Curl",
            "dumbbell-curl",
            ["dumbbells"],
            "core",
            ["barbell-curl", "hammer-curl"],
        ),
        (
            "Incline Dumbbell Curl",
            "incline-dumbbell-curl",
            ["dumbbells", "bench"],
            "accessory",
            ["dumbbell-curl"],
        ),
        (
            "Preacher Curl Dumbbell",
            "preacher-curl-dumbbell",
            ["dumbbells", "preacher-bench"],
            "accessory",
            ["dumbbell-curl"],
        ),
        (
            "Concentration Curl",
            "concentration-curl",
            ["dumbbells", "bench"],
            "accessory",
            ["dumbbell-curl"],
        ),
        (
            "Spider Curl",
            "spider-curl",
            ["dumbbells", "bench"],
            "accessory",
            ["dumbbell-curl"],
        ),
        (
            "Seated Dumbbell Curl",
            "seated-dumbbell-curl",
            ["dumbbells", "bench"],
            "accessory",
            ["dumbbell-curl"],
        ),
        (
            "Cross Body Hammer Curl",
            "cross-body-hammer-curl",
            ["dumbbells"],
            "accessory",
            ["hammer-curl"],
        ),
        ("Waiter Curl", "waiter-curl", ["dumbbells"], "accessory", ["dumbbell-curl"]),
        # Hammer Curls
        (
            "Hammer Curl",
            "hammer-curl",
            ["dumbbells"],
            "core",
            ["dumbbell-curl", "cross-body-hammer-curl"],
        ),
        (
            "Rope Hammer Curl",
            "rope-hammer-curl",
            ["cable"],
            "accessory",
            ["hammer-curl"],
        ),
        (
            "Incline Hammer Curl",
            "incline-hammer-curl",
            ["dumbbells", "bench"],
            "accessory",
            ["hammer-curl"],
        ),
        # Cable Curls
        ("Cable Curl", "cable-curl", ["cable"], "accessory", ["barbell-curl"]),
        ("High Cable Curl", "high-cable-curl", ["cable"], "accessory", ["cable-curl"]),
        (
            "Single Arm Cable Curl",
            "single-arm-cable-curl",
            ["cable"],
            "accessory",
            ["cable-curl"],
        ),
        # Machine & Preacher
        (
            "Preacher Curl Machine",
            "preacher-curl-machine",
            ["machine"],
            "accessory",
            ["preacher-curl-dumbbell"],
        ),
        (
            "Preacher Curl EZ Bar",
            "preacher-curl-ez-bar",
            ["ez-bar", "preacher-bench"],
            "accessory",
            ["preacher-curl-dumbbell"],
        ),
        ("Machine Curl", "machine-curl", ["machine"], "accessory", ["barbell-curl"]),
        # Specialty
        ("Zottman Curl", "zottman-curl", ["dumbbells"], "accessory", ["dumbbell-curl"]),
        ("Bayesian Curl", "bayesian-curl", ["cable"], "accessory", ["cable-curl"]),
        ("Pinwheel Curl", "pinwheel-curl", ["dumbbells"], "accessory", ["hammer-curl"]),
        (
            "Scott Curl",
            "scott-curl",
            ["ez-bar", "scott-bench"],
            "accessory",
            ["preacher-curl"],
        ),
    ],
}


def enrich_exercise(
    exercise_path: Path,
    muscle_group: str,
    equipment: list,
    importance: str,
    related: list,
):
    """Add metadata to an exercise file."""
    content = exercise_path.read_text()

    exercise_name = exercise_path.stem

    # Replace placeholders
    content = re.sub(r"equipment: \[\]", f"equipment: {equipment}", content)
    content = re.sub(
        r"muscle_groups: \[\]", f"muscle_groups: [{muscle_group}]", content
    )
    content = re.sub(r"importance: accessory", f"importance: {importance}", content)

    tags = [muscle_group]
    if muscle_group in ["chest", "shoulders", "triceps"]:
        tags.append("push")
    else:
        tags.append("pull")

    content = re.sub(r"tags: \[\]", f"tags: {tags}", content)
    content = re.sub(r"related: \[\]", f"related: {related}", content)

    exercise_path.write_text(content)


def main():
    exercises_dir = Path(__file__).parent.parent / "exercises"
    templates_dir = Path(__file__).parent.parent / "templates"

    total_created = 0

    for muscle_group, exercises in EXERCISES.items():
        print(f"\n=== Creating {len(exercises)} {muscle_group} exercises ===")

        for name, movement, equipment, importance, related in exercises:
            filename = sanitize_filename(name)
            exercise_path = exercises_dir / f"{filename}.md"

            if exercise_path.exists():
                print(f"  Skipping (exists): {name}")
                continue

            try:
                create_exercise(name, movement, templates_dir, exercises_dir)
                enrich_exercise(
                    exercise_path, muscle_group, equipment, importance, related
                )
                print(f"  Created: {name}")
                total_created += 1
            except Exception as e:
                print(f"  Error creating {name}: {e}")

    print(f"\n=== Total exercises created: {total_created} ===")


if __name__ == "__main__":
    main()
