"""Read forces from .csv file and perform basic stats.

To see command line options, run:
python example_stats.py --help
"""

import matplotlib.pyplot as plt

from forcelib import read_csv, plot_force_v_displacement, _parse_args

if __name__ == '__main__':
    # Read command line arguments
    args = _parse_args(__doc__)

    # Print the command line arguments
    print('Input file: {}'.format(str(args.file)))
    print('Skipped tests: {}'.format(args.exclude))

    # Read the CSV data into a list of pandas.Series
    forces = read_csv(str(args.file), args.exclude)

    # Plot the forces
    plot_force_v_displacement(forces)
    plt.show()

    # Select the first 5 mm of displacement
    first5mm = forces[forces['displacement'] < 5]
    plot_force_v_displacement(first5mm)
    plt.show()

    # Describe basic statistics for the first test by name
    print('Summary stats for Test 1')
    print(first5mm.loc['Test 1'].describe())
    print()  # newline for clarity

    # Describe summary statistics for all tests
    print('Summary stats for all tests')
    print(first5mm.groupby(level='test').describe())
    print()

    # Describe just the mean of the second sample in the list
    # :.3f means format the floating point number to 3 decimal places
    name, group = list(first5mm.groupby(level=0))[1]
    print('{} mean = {:.3f}'.format(name, group['force'].mean()))

    # Select only forces below 6 Newtons
    below6N = first5mm[first5mm['force'] < 6]
    plot_force_v_displacement(below6N)
    plt.show()
