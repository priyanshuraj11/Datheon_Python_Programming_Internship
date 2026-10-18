#!/usr/bin/env python3

"""
Smart File Organizer
--------------------
Features:
- Automatically categorizes files by extension.
- Creates category folders dynamically.
- Handles duplicate filenames safely.
- Handles permission and filesystem errors.
- Supports dry-run mode.
- Displays an execution summary.
- Skips Windows system files such as desktop.ini.

Run:
    python organizer.py --dry-run
    python organizer.py

Organize another folder:
    python organizer.py "C:\\Users\\Lenovo\\Downloads"
"""

import argparse
import os
import shutil
import sys
from collections import Counter
from pathlib import Path


# File extension to category mapping
EXTENSION_CATEGORIES = {
    # Documents
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".rtf": "Documents",
    ".odt": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",
    ".csv": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".md": "Documents",

    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".bmp": "Images",
    ".tif": "Images",
    ".tiff": "Images",
    ".webp": "Images",
    ".svg": "Images",
    ".ico": "Images",
    ".heic": "Images",

    # Videos
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".mov": "Videos",
    ".avi": "Videos",
    ".wmv": "Videos",
    ".flv": "Videos",
    ".webm": "Videos",
    ".m4v": "Videos",
    ".mpeg": "Videos",
    ".mpg": "Videos",

    # Audio
    ".mp3": "Audio",
    ".wav": "Audio",
    ".aac": "Audio",
    ".flac": "Audio",
    ".ogg": "Audio",
    ".m4a": "Audio",
    ".wma": "Audio",

    # Archives
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",
    ".bz2": "Archives",
    ".xz": "Archives",
    ".tgz": "Archives",

    # Code and configuration
    ".py": "Code",
    ".js": "Code",
    ".ts": "Code",
    ".jsx": "Code",
    ".tsx": "Code",
    ".html": "Code",
    ".htm": "Code",
    ".css": "Code",
    ".scss": "Code",
    ".java": "Code",
    ".c": "Code",
    ".h": "Code",
    ".cpp": "Code",
    ".hpp": "Code",
    ".cs": "Code",
    ".php": "Code",
    ".rb": "Code",
    ".go": "Code",
    ".rs": "Code",
    ".swift": "Code",
    ".kt": "Code",
    ".sql": "Code",
    ".json": "Code",
    ".xml": "Code",
    ".yaml": "Code",
    ".yml": "Code",
    ".toml": "Code",
    ".sh": "Code",
    ".bat": "Code",
    ".ps1": "Code",
    ".ipynb": "Code",

    # Applications and installers
    ".exe": "Applications",
    ".msi": "Applications",
    ".dmg": "Applications",
    ".pkg": "Applications",
    ".deb": "Applications",
    ".rpm": "Applications",
    ".apk": "Applications",
}


# Windows and macOS metadata files to ignore
IGNORED_FILENAMES = {
    "desktop.ini",
    "thumbs.db",
    ".ds_store",
}


def get_category(file_path: Path) -> str:
    """Determine the category using the file extension."""

    extension = file_path.suffix.lower()

    return EXTENSION_CATEGORIES.get(extension, "Others")


def unique_destination(destination: Path) -> Path:
    """
    Return a destination path that does not overwrite an existing file.

    Example:
        report.pdf
        report (1).pdf
        report (2).pdf
    """

    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = (
            f"{destination.stem} ({counter})"
            f"{destination.suffix}"
        )

        candidate = destination.with_name(new_name)

        if not candidate.exists():
            return candidate

        counter += 1


def organize_directory(
    source: Path,
    dry_run: bool = False
) -> dict:
    """Organize regular files directly inside the source directory."""

    if not source.exists():
        raise FileNotFoundError(
            f"Directory does not exist: {source}"
        )

    if not source.is_dir():
        raise NotADirectoryError(
            f"Path is not a directory: {source}"
        )

    source = source.resolve()

    stats = Counter()
    category_counts = Counter()
    errors = []

    print("\n" + "=" * 66)
    print("                 SMART FILE ORGANIZER")
    print("=" * 66)

    print(f"Source directory : {source}")

    mode = (
        "DRY RUN - Preview only"
        if dry_run
        else "LIVE - Files will be moved"
    )

    print(f"Mode             : {mode}")
    print("-" * 66)

    # Scan the source directory.
    try:
        with os.scandir(source) as scanner:
            entries = list(scanner)

    except PermissionError as exc:
        raise PermissionError(
            f"Cannot access directory: {source}"
        ) from exc

    except OSError as exc:
        raise OSError(
            f"Could not scan directory: {exc}"
        ) from exc

    # Process each entry.
    for entry in entries:

        item = Path(entry.path)

        try:
            # Skip Windows/macOS metadata files.
            if entry.name.lower() in IGNORED_FILENAMES:
                stats["system_files_skipped"] += 1

                print(
                    f"[SKIP] System file: {entry.name}"
                )

                continue

            # Skip symbolic links.
            if entry.is_symlink():
                stats["symlinks_skipped"] += 1

                print(
                    f"[SKIP] Symbolic link: {entry.name}"
                )

                continue

            # Skip directories.
            if entry.is_dir(follow_symlinks=False):
                stats["directories_skipped"] += 1
                continue

            # Skip non-regular files.
            if not entry.is_file(follow_symlinks=False):
                stats["other_entries_skipped"] += 1

                print(
                    f"[SKIP] Not a regular file: {entry.name}"
                )

                continue

            stats["files_inspected"] += 1

            # Determine the category.
            category = get_category(item)

            category_dir = source / category

            destination = unique_destination(
                category_dir / item.name
            )

            # Preview mode: do not change any files.
            if dry_run:
                print(
                    f"[PREVIEW] {item.name} -> "
                    f"{category}/{destination.name}"
                )

                stats["would_move"] += 1
                category_counts[category] += 1

                continue

            # Create category folder if required.
            category_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            # Check the destination again before moving.
            destination = unique_destination(
                category_dir / item.name
            )

            # Move the file.
            shutil.move(
                str(item),
                str(destination)
            )

            stats["moved"] += 1
            category_counts[category] += 1

            print(
                f"[MOVED] {item.name} -> "
                f"{category}/{destination.name}"
            )

        except PermissionError as exc:
            stats["permission_errors"] += 1

            errors.append(
                f"{entry.name}: Permission denied ({exc})"
            )

            print(
                f"[PERMISSION ERROR] {entry.name}: {exc}"
            )

        except FileExistsError as exc:
            stats["collision_errors"] += 1

            errors.append(
                f"{entry.name}: Destination already exists ({exc})"
            )

            print(
                f"[COLLISION ERROR] {entry.name}: {exc}"
            )

        except (OSError, shutil.Error) as exc:
            stats["other_errors"] += 1

            errors.append(
                f"{entry.name}: {exc}"
            )

            print(
                f"[ERROR] {entry.name}: {exc}"
            )

    # Display execution summary.
    print("\n" + "=" * 66)
    print("                  EXECUTION SUMMARY")
    print("=" * 66)

    print(
        f"Files inspected          : "
        f"{stats['files_inspected']}"
    )

    if dry_run:
        print(
            f"Files that would move    : "
            f"{stats['would_move']}"
        )

        print(
            "Files actually moved     : 0 (dry-run mode)"
        )

    else:
        print(
            f"Files moved successfully : "
            f"{stats['moved']}"
        )

    print(
        f"Directories skipped      : "
        f"{stats['directories_skipped']}"
    )

    print(
        f"System files skipped     : "
        f"{stats['system_files_skipped']}"
    )

    print(
        f"Symbolic links skipped   : "
        f"{stats['symlinks_skipped']}"
    )

    print(
        f"Other entries skipped    : "
        f"{stats['other_entries_skipped']}"
    )

    print(
        f"Permission errors        : "
        f"{stats['permission_errors']}"
    )

    print(
        f"Collision errors         : "
        f"{stats['collision_errors']}"
    )

    print(
        f"Other errors             : "
        f"{stats['other_errors']}"
    )

    # Category-wise totals.
    if category_counts:

        print("\nCategory breakdown:")

        for category, count in sorted(
            category_counts.items()
        ):
            print(f"  {category:<15} {count}")

    # Display errors, if any.
    if errors:

        print("\nErrors requiring attention:")

        for error in errors:
            print(f"  - {error}")

    print("=" * 66)

    return {
        "stats": dict(stats),
        "categories": dict(category_counts),
        "errors": errors,
    }


def main() -> int:
    """Parse arguments and execute the organizer."""

    # Default directory: test_files beside this script.
    script_directory = Path(__file__).resolve().parent

    default_directory = script_directory / "test_files"

    parser = argparse.ArgumentParser(
        description=(
            "Automatically organize files into "
            "folders based on their extensions."
        )
    )

    parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=default_directory,
        help=(
            "Directory to organize. "
            "Defaults to the local test_files folder."
        ),
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview planned moves without changing files.",
    )

    args = parser.parse_args()

    try:
        organize_directory(
            args.directory,
            dry_run=args.dry_run
        )

        return 0

    except (
        FileNotFoundError,
        NotADirectoryError,
        PermissionError,
        OSError,
    ) as exc:

        print(
            f"\n[FATAL ERROR] {exc}",
            file=sys.stderr
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(main())