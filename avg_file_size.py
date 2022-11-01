#!/usr/bin/python3
import os
import argparse


def main():
    """
    Gets the averge size of non-zero files in a directory.
    """
    parser = argparse.ArgumentParser(
        "Find the average size of non-zero files in a directory"
    )
    parser.add_argument("directory", help="Directory to check")
    args = parser.parse_args()
    dir = args.directory

    print(f"Getting average file size of: {dir}")
    num_bytes = 0
    num_files = 0
    num_empty_files = 0
    for f in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, f)):
            b = os.path.getsize(os.path.join(dir, f))
            if b == 0:
                num_empty_files += 1
            else:
                num_bytes += b
                num_files += 1

    print(
        f"Empty files: {num_empty_files}, Non-Empty files: {num_files}, Avg file size: {num_bytes/num_files}"
    )


main()
