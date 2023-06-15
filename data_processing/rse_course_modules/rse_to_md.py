import os
import shutil
import subprocess

# The top argument for walk
topdir = "/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules"  # Or specify your directory path

# The extension to search for
exten = ".ipynb"

# The destination directory
dest_dir = "/Users/lbokeria/Documents/hack_week_2023/reginald/data/rse_course/"  # Replace with your destination directory path

for dirpath, dirnames, files in os.walk(topdir):
    for name in files:
        if name.lower().endswith(exten):
            full_path = os.path.join(dirpath, name)
            output_path = (
                os.path.splitext(full_path)[0] + ".md"
            )  # Replace .ipynb with .md
            command = [
                "jupyter",
                "nbconvert",
                full_path,
                "--to",
                "markdown",
                "--output",
                output_path,
            ]
            subprocess.run(command)

            # Move the output file to the destination directory
            dest_file_path = os.path.join(dest_dir, os.path.basename(output_path))
            shutil.move(output_path, dest_file_path)
