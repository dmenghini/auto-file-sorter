import os
import shutil
from pathlib import Path


def get_extension(filename: str) -> str:
    """Returns the lowercase file extension without the dot, or 'no_extension' if none."""
    ext = Path(filename).suffix.lower().lstrip(".")
    return ext if ext else "no_extension"


def create_target_dir(base_dir: Path, extension: str) -> Path:
    """Creates and returns the path to the target directory for the given extension."""
    target_dir = base_dir / extension
    target_dir.mkdir(exist_ok=True)
    return target_dir


def move_file_to_target(file_path: Path, target_dir: Path):
    """Moves the file to the target directory, handling name collisions."""
    target_file_path = target_dir / file_path.name

    # Handle name collisions by appending a number suffix
    if target_file_path.exists():
        counter = 1
        while True:
            new_name = f"{file_path.stem}_{counter}{file_path.suffix}"
            new_target = target_dir / new_name
            if not new_target.exists():
                target_file_path = new_target
                break
            counter += 1

    shutil.move(str(file_path), str(target_file_path))


def remove_empty_dirs(base_dir: Path):
    for root, dirs, _ in os.walk(base_dir, topdown=False):
        for d in dirs:
            dir_path = Path(root) / d
            try:
                dir_path.rmdir()
                print(f"Removed empty directory: {dir_path}")
            except OSError:
                pass  # Directory not empty, skip


def organize_files_by_extension(source_dir: str, recursive: bool = False):
    """
    Organizes files in the source_dir into subdirectories based on their file extensions.
    If recursive is True, also sorts files from all subdirectories.
    """
    base_path = Path(source_dir)

    if not base_path.exists() or not base_path.is_dir():
        raise ValueError(f"Provided path '{source_dir}' is not a valid directory.")

    if recursive:
        # Walk through all subdirectories
        walker = os.walk(source_dir)
    else:
        # Only list files in the top-level directory
        walker = [(source_dir, [], os.listdir(source_dir))]

    for root, _, files in walker:
        for file in files:
            file_path = Path(root) / file

            if not file_path.is_file():
                continue

            # Skip already sorted files
            if file_path.parent.name == get_extension(file):
                continue

            ext = get_extension(file)
            target_dir = create_target_dir(base_path, ext)

            try:
                move_file_to_target(file_path, target_dir)
            except Exception as e:
                print(f"Error moving {file_path}: {e}")
