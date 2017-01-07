"""Plot forces and displacements versus time.

To see command line options, run:
python plot.py --help
"""

import matplotlib.pyplot as plt

from forcelib import read_csv, plot_fdt,  _parse_args

if __name__ == '__main__':
    # Read command line arguments
    args = _parse_args(__doc__)

    # Print the command line arguments
    print('Input file: {}'.format(str(args.file)))
    print('Skipped tests: {}'.format(args.exclude))

    # Read the CSV data into a pandas.DataFrame
    forces = read_csv(str(args.file), args.exclude)

    # Plot forces and displacement versus time
    plot_fdt(forces, str(args.file))
    plt.show()

    # To plot events too, use
    # plot_fdt(forces, str(args.file), True)
    # plt.show()
