"""Read forces from .csv file.

To see command line options, run:
python read.py --help
"""

import matplotlib.pyplot as plt

import forcelib as flib

if __name__ == '__main__':
    # Read command line arguments
    args = flib._parse_args(__doc__)

    # Read the CSV data into a pandas.DataFrame
    forces = flib.read_csv(str(args.file), args.exclude)

    # Plot the forces
    flib.plot(forces)
    plt.show()
