"""Read forces from .csv file and calculate work done.

To see command line options, run:
python example_work.py --help
"""

import matplotlib.pyplot as plt

import numpy as np

from forcelib import read_csv, plot_force_v_displacement, work, _parse_args

if __name__ == '__main__':
    # Read command line arguments
    args = _parse_args(__doc__)

    # Print the command line arguments
    print('Input file: {}'.format(str(args.file)))
    print('Skipped tests: {}'.format(args.exclude))

    # Read the CSV data into a list of pandas.Series
    forces = read_csv(str(args.file), args.exclude)

    # Select the 1 to 5 mm of displacement
    forces_1to5mm = forces[(forces['displacement'] >= 1) &
                           (forces['displacement'] < 5)]

    print(forces_1to5mm)
    # Calculate the work for each test
    works = work(forces_1to5mm)

    print(type(works))
    print(works)

    # works.plot(kind='bar')
    # index = np.arange(len(forces_1to5mm))

    # plt.bar(index, works)
    # plt.xticks(index + 0.5, [series.name for series in forces_1to5mm],
               # rotation=45)
    # plt.ylabel('Work done (J)')
    # plt.tight_layout()
    plt.show()
