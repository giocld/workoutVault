#!/usr/bin/env python3
"""Fetch exercise images from wger.de API using translations endpoint"""

import argparse
import asyncio
import aiohttp
import re
from pathlib import Path


def sanitize_filename(name: str) -> str:
    """Convert exercise name to filename format."""
    filename = re.sub(r"[^\w\s-]", "", name.lower())
    filename = re.sub(r"[-\s]+", "-", filename)
    return filename.strip("-")


async def fetch_all_pages(session, base_url):
    """Fetch all pages from a paginated API endpoint"""
    all_results = []
    url = base_url

    while url:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                all_results.extend(data.get("results", []))
                url = data.get("next")
            else:
                print(f"Error fetching {url}: {response.status}")
                break

    return all_results


async def download_image(session, image_url, image_path):
    """Download image from URL"""
    try:
        async with session.get(
            image_url, timeout=aiohttp.ClientTimeout(total=30)
        ) as response:
            if response.status == 200:
                data = await response.read()
                if len(data) > 1000:
                    image_path.write_bytes(data)
                    return True
        return False
    except Exception as e:
        return False


async def fetch_images_for_exercises(exercises_dir, images_dir, force=False):
    """Match local exercises with wger.de images and download"""

    print("Fetching data from wger.de...")

    async with aiohttp.ClientSession() as session:
        # Get all translations (English = language 2)
        translations = await fetch_all_pages(
            session, "https://wger.de/api/v2/exercise-translation/?language=2&limit=100"
        )

        # Get all images
        images = await fetch_all_pages(
            session, "https://wger.de/api/v2/exerciseimage/?limit=100"
        )

        # Create lookup: exercise_id -> image_url
        exercise_to_image = {}
        for img in images:
            if img.get("is_main"):
                exercise_id = img.get("exercise")
                if exercise_id:
                    exercise_to_image[exercise_id] = img["image"]

        # Create lookup: exercise_name -> exercise_id
        # Also store original names for display
        name_to_exercise_id = {}
        name_variations = {}

        for trans in translations:
            name = trans.get("name", "").strip()
            exercise_id = trans.get("exercise")

            if name and exercise_id:
                # Store original
                name_lower = name.lower()
                name_to_exercise_id[name_lower] = exercise_id
                name_variations[name_lower] = name

                # Create variations (without equipment specs)
                variations = [
                    re.sub(
                        r"\s*(?:barbell|dumbbell|cable|machine|bodyweight|ez[-\s]?bar)\s*",
                        " ",
                        name_lower,
                    ).strip(),
                    re.sub(
                        r"\s*\([^)]*\)\s*", "", name_lower
                    ).strip(),  # Remove parentheses
                ]
                for var in variations:
                    if var and var != name_lower:
                        if var not in name_to_exercise_id:
                            name_to_exercise_id[var] = exercise_id
                            name_variations[var] = name

        print(f"Found {len(translations)} translations and {len(images)} images")
        print(f"Mapped {len(name_to_exercise_id)} exercise names")
        print()

        # Process local exercises
        images_dir.mkdir(parents=True, exist_ok=True)
        exercise_files = sorted(exercises_dir.glob("*.md"))

        success_count = 0
        fail_count = 0

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
            image_path = images_dir / f"{filename}.png"

            if image_path.exists() and not force:
                print(f"[{i}/{len(exercise_files)}] {exercise_name} - ✓ exists")
                success_count += 1
                continue

            # Try to find matching exercise
            lookup_name = exercise_name.lower()
            image_url = None
            matched_name = None

            # Direct match
            if lookup_name in name_to_exercise_id:
                exercise_id = name_to_exercise_id[lookup_name]
                if exercise_id in exercise_to_image:
                    image_url = exercise_to_image[exercise_id]
                    matched_name = name_variations.get(lookup_name, lookup_name)

            # Try with common substitutions
            if not image_url:
                variations = [
                    lookup_name.replace("press", "bench press"),
                    lookup_name.replace("dumbbell", ""),
                    lookup_name.replace("barbell", ""),
                    lookup_name.replace("cable", ""),
                    lookup_name.replace("machine", ""),
                ]
                for var in variations:
                    var = var.strip()
                    if var in name_to_exercise_id:
                        exercise_id = name_to_exercise_id[var]
                        if exercise_id in exercise_to_image:
                            image_url = exercise_to_image[exercise_id]
                            matched_name = name_variations.get(var, var)
                            break

            if image_url:
                print(f"[{i}/{len(exercise_files)}] {exercise_name} - downloading...")
                if await download_image(session, image_url, image_path):
                    size = image_path.stat().st_size
                    print(f"  ✓ Downloaded ({size} bytes)")
                    success_count += 1
                else:
                    print(f"  ✗ Failed to download")
                    fail_count += 1
            else:
                print(f"[{i}/{len(exercise_files)}] {exercise_name} - ✗ no match")
                fail_count += 1

    print()
    print(f"=== Results ===")
    print(f"Success: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"Total: {len(exercise_files)}")


async def main():
    parser = argparse.ArgumentParser(description="Fetch exercise images from wger.de")
    parser.add_argument("--all", action="store_true", help="Fetch all exercise images")
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing images"
    )

    args = parser.parse_args()

    if args.all:
        vault_dir = Path(__file__).parent.parent
        exercises_dir = vault_dir / "exercises"
        images_dir = vault_dir / "images" / "exercises"

        await fetch_images_for_exercises(exercises_dir, images_dir, args.force)
    else:
        parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())
