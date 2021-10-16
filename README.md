# LOTR project analysis
[![tests](https://github.com/portugueslab/lotr/actions/workflows/main.yml/badge.svg)](https://github.com/portugueslab/lotr/actions/workflows/main.yml)

Analysis of the anterior hindbrain motion integration ring attractor.

### Installation with notebook clean hook

To commit notebooks without content, install `nb-clean`:
``` 
python3 -m pip install nb-clean
```

And in the repo local path:
```
nb-clean add-filter
```

Once analysis notebooks are completed, they should be moved to the `notebooks/testable` folder. All notebooks there will be executed by pytest (no controls on the results though).

To regenerate all figures in the figures folder, run:
```
pytest --cov --nbmake "./notebooks/testable/"  -n=auto
```

To export all testable notebooks to PDFs, you can run the following script:
```
python ...lotr/scripts/export_all_notebooks.py
```
