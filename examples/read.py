"""Read forces from .csv file.

To see command line options, run:
python read.py --help
"""

import matplotlib.pyplot as plt

from forcelib import read_csv, plot_fd, _parse_args

if __name__ == '__main__':
    # Read command line arguments
    args = _parse_args(__doc__)

    # Print the command line arguments
    print('Input file: {}'.format(str(args.file)))
    print('Skipped tests: {}'.format(args.exclude))

    # Read the CSV data into a pandas.DataFrame
    forces = read_csv(str(args.file), args.exclude)

    # Plot the forces
    plot_fd(forces)
    plt.show()
