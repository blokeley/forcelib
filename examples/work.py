"""Read forces from .csv file and calculate work done.

To see command line options, run:
python work.py --help
"""

import matplotlib.pyplot as plt

import forcelib as flib

if __name__ == '__main__':
    # Read command line arguments
    args = flib._parse_args(__doc__)

    # Print the command line arguments
    print('Input file: {}'.format(str(args.file)))
    print('Skipped tests: {}'.format(args.exclude))

    # Read the CSV data into a pandas.DataFrame
    forces = flib.read_csv(str(args.file), args.exclude)

    # Select the 1 to 5 mm of displacement
    forces_1to5mm = forces[(forces['displacement'] >= 1) &
                           (forces['displacement'] < 5)]

    # Calculate the work for each test
    works = flib.work(forces_1to5mm)

    works.plot(kind='bar', title='Work done (J)')
    plt.show()
