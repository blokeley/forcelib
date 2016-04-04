"""Read forces from .csv file and perform basic stats.

To see command line options, run:
python stats.py --help
"""

import matplotlib.pyplot as plt

from forcelib import read_csv, plot_force_v_displacement, _parse_args

if __name__ == '__main__':
    # Read command line arguments
    args = _parse_args(__doc__)

    # Print the command line arguments
    print('Input file: {}'.format(str(args.file)))
    print('Skipped tests: {}'.format(args.exclude))

    # Read the CSV data into a pandas.DataFrame
    forces = read_csv(str(args.file), args.exclude)

    # Plot the forces
    plot_force_v_displacement(forces)
    plt.show()

    # Select the first 5 mm of displacement
    first5mm = forces[forces['displacement'] < 5]
    plot_force_v_displacement(first5mm)
    plt.show()

    # Describe summary statistics for all tests
    print('Summary stats for all tests')
    print(first5mm.groupby(level='test').describe())
    print()  # newline for clarity

    # Print mean force for Test 2
    print('Summary stats for Test 2')
    print(first5mm.loc['Test 2'].mean())
    print()  # newline for clarity
