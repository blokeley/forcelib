"""Plot forces and displacements versus time.

To see command line options, run:
python plot.py --help
"""

import matplotlib.pyplot as plt

import forcelib

if __name__ == '__main__':
    # Read command line arguments
    args = forcelib._parse_args(__doc__)

    # Read the CSV data into a pandas.DataFrame
    forces = forcelib.read_csv(str(args.file), args.exclude)

    # Plot force versus displacement (the default)
    forcelib.plot(forces, title=str(args.file))
    plt.show()

    # Plot force and displacement versus time
    forcelib.plot(forces, x='time', y=['force', 'displacement'])
    plt.show()
