import os
from lotr import FIGURES_LOCATION
from pathlib import Path
import datetime


# Create timestamped destination folder:
date = datetime.datetime.now()
subfolder_name = f"{date.year}{date.month}{date.day}_{date.hour}{date.minute}"

dest = FIGURES_LOCATION / "exported notebooks" / subfolder_name
dest.mkdir(exist_ok=True, parents=True)

# Find all source notebooks:
ipynb_files = (Path(__file__).parent.parent / "notebooks" / "testable").glob("*.ipynb")

# Convert
for nb in ipynb_files:
    os.system(f'jupyter nbconvert --output-dir "{dest}" --to PDF --execute "{nb}"')
