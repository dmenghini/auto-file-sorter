import argparse
from sorter.file_organizer import organize_files_by_extension

def main():
    parser = argparse.ArgumentParser(
        description="Organize files in a directory by their file extension."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="Path to the directory to organize"
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively sort files in all subdirectories (default: False)"
    )

    args = parser.parse_args()
    organize_files_by_extension(args.directory, recursive=args.recursive)
