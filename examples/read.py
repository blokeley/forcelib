"""Read forces from .csv file.

To see command line options, run:
python read.py --help
"""

import matplotlib.pyplot as plt

import forcelib

if __name__ == '__main__':
    # Read command line arguments
    args = forcelib._parse_args(__doc__)

    # Read the CSV data into a pandas.DataFrame
    forces = forcelib.read_csv(str(args.file), args.exclude)

    # Plot the forces
    forcelib.plot(forces)
    plt.show()
