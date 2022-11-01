#!/usr/bin/python3
import sys
import os


if len(sys.argv) < 2:
    print("Must enter directory to check")
    quit()

dir = sys.argv[1]

print(f"Geting average file size of {dir}")
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
