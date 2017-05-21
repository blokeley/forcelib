"""Plot forces and displacements versus time.

To see command line options, run:
python plot.py --help
"""

import matplotlib.pyplot as plt

import forcelib as flib

if __name__ == '__main__':
    # Read command line arguments
    args = flib._parse_args(__doc__)

    # Read the CSV data into a pandas.DataFrame
    forces = flib.read_csv(str(args.file), args.exclude)

    # Plot force versus displacement (the default)
    flib.plot(forces, title=str(args.file))
    plt.show()

    # Plot force and displacement versus time
    flib.plot(forces, x='time', y=['force', 'displacement'])
    plt.show()
