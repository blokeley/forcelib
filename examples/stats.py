"""Read forces from .csv file and perform basic stats.

To see command line options, run:
python stats.py --help
"""

import matplotlib.pyplot as plt

from forcelib import read_csv, plot_fd, bar_fmean, _parse_args

if __name__ == '__main__':
    # Read command line arguments
    args = _parse_args(__doc__)

    # Print the command line arguments
    print('Input file: {}'.format(str(args.file)))
    print('Skipped tests: {}'.format(args.exclude))

    # Read the CSV data into a pandas.DataFrame
    forces = read_csv(str(args.file), args.exclude)

    # Plot the forces
    plot_fd(forces, 'All displacements')
    plt.show()

    # Select the first 5 mm of displacement
    first5mm = forces[forces['displacement'] < 5]
    plot_fd(first5mm, 'First 5 mm')
    plt.show()

    # Describe summary statistics for all tests
    print('Summary stats for all tests')
    print(first5mm.groupby(level='test').describe())
    print()  # newline for clarity

    # Print mean force for Test 2
    print('Mean force for Test 2')
    print(first5mm.loc['Test 2']['force'].mean())
    print()  # newline for clarity

    # Bar chart of mean forces
    bar_fmean(first5mm)
    plt.show()

    # If you really want to select the second test by number
    # rather than name, you could try the following.  The
    # [0] selects the first level index (test names) and [1]
    # means selects the second test name.  You could select  Test 2 to Test 5
    # inclusive using
    # tests2to5 = first5mm.loc[first5mm.index.levels[0][1] :
    #                          first5mm.index.levels[0][4]]
