"""Read forces from .csv file and perform basic stats.

To see command line options, run:
python example_stats.py --help
"""

import matplotlib.pyplot as plt

from forcelib import read_forces, plot, _parse_args

if __name__ == '__main__':
    # Read command line arguments
    args = _parse_args(__doc__)

    # Print the command line arguments
    print('Input file: {}'.format(str(args.file)))
    print('Skipped tests: {}'.format(args.exclude))

    # Read the CSV data into a list of pandas.Series
    forces = read_forces(str(args.file), args.exclude)

    # Plot the forces
    plot(forces)
    plt.show()

    # Select the first 5 mm of displacement
    # s.index is the array of displacement.  We select only the rows where
    # displacement < 5 by using s[s.index < 5]
    first5mm = [s[s.index < 5] for s in forces]
    plot(first5mm)
    plt.show()

    # Describe basic statistics for the first sample in the list
    # Note that the first element in a Python list has index 0
    print()  # newline for clarity
    print(first5mm[0].describe())
    print()  # newline for clarity

    # Describe just the mean of the second sample in the list
    # :.3f means format the floating point number to 3 decimal places
    print('{} mean = {:.3f}'.format(first5mm[1].name, first5mm[1].mean()))

    # Select only forces below 6 Newtons
    below6N = [s[s < 6] for s in first5mm]
    plot(below6N)
    plt.show()
