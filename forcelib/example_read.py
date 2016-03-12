"""Read forces from .csv file."""

import logging

import matplotlib.pyplot as plt

from forcelib import read_forces, plot, _parse_args

if __name__ == '__main__':
    """Main program."""
    args = _parse_args(__doc__)

    # Set up logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info('Input file: {}'.format(str(args.file)))
    logger.info('Skipped tests: {}'.format(args.exclude))

    # Read the CSV data into a list of pandas.Series
    forces = read_forces(str(args.file), args.exclude)

    # Plot the forces
    plot(forces)
    plt.show()
