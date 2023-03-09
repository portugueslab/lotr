"""This script can be used to export all relevant notebooks of the paper to pdfs.
By default the pdfs will be created in the specified figures location.
"""

import datetime
import os
from pathlib import Path

from lotr import FIGURES_LOCATION


def export_all_notebooks():
    # Create timestamped destination folder:
    date = datetime.datetime.now()
    subfolder_name = f"{date.year}{date.month}{date.day}_{date.hour}{date.minute}"

    dest = FIGURES_LOCATION / "exported notebooks" / subfolder_name
    dest.mkdir(exist_ok=True, parents=True)

    # Find all source notebooks:
    ipynb_files = (Path(__file__).parent.parent / "notebooks" / "testable").glob(
        "*.ipynb"
    )

    # Convert

    for nb in ipynb_files:
        os.system(f'jupyter nbconvert --output-dir "{dest}" --to PDF --execute "{nb}"')


if __name__ == "__main__":
    export_all_notebooks()
