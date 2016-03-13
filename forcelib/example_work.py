"""Read forces from .csv file and calculate work done.

To see command line options, run:
python example_work.py --help
"""

import matplotlib.pyplot as plt

import numpy as np

from forcelib import read_forces, plot, work, _parse_args

if __name__ == '__main__':
    # Read command line arguments
    args = _parse_args(__doc__)

    # Print the command line arguments
    print('Input file: {}'.format(str(args.file)))
    print('Skipped tests: {}'.format(args.exclude))

    # Read the CSV data into a list of pandas.Series
    forces = read_forces(str(args.file), args.exclude)

    # Select the 1 to 5 mm of displacement
    # s.index is the array of displacement.  We select only the rows where
    # displacement < 5 by using s[s.index < 5]
    forces_1to5mm = [s[(s.index >= 1) & (s.index < 5)] for s in forces]
    plot(forces_1to5mm)
    plt.show()

    # Calculate the work for each series (test)
    # Note that the first element in a Python list has index 0
    works = [work(series) for series in forces_1to5mm]

    index = np.arange(len(forces_1to5mm))

    plt.bar(index, works)
    plt.xticks(index + 0.5, [series.name for series in forces_1to5mm],
               rotation=45)
    plt.ylabel('Work done (J)')
    plt.tight_layout()
    plt.show()
