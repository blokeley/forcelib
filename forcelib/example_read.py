"""Read forces from .csv file."""

import logging

from forcelib import read_forces, _parse_args


def setup_logging(level, logfile=__file__ + '.log'):
    """Set up logging module to log at given level to given file.

    Args:
    level (int): logging level (use logging.DEBUG etc.)
    logfile (str): string or file-like object to log to

    Returns:
    logging.Logger: the root logger
    """
    logger = logging.getLogger()
    handler = logging.FileHandler(logfile, mode='w')
    fmt = '%(asctime)-15s %(levelname)-8s %(message)s'
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
    return logger


if __name__ == '__main__':
    """Main program."""
    args = _parse_args(__doc__)

    # Set up logging
    logfile = args.file.with_suffix('.log')
    logger = setup_logging(logging.INFO, str(logfile))

    logger.info('Input file: {}'.format(str(args.file)))
    logger.info('Skipped tests: {}'.format(args.exclude))

    forces = read_forces(str(args.file), args.exclude)

#    dataframes = []
#
#    for test_id in test_ids:
#        # Create a DataFrame for each test
#        # Columns are 0-indexed and test_ids are 1-indexed
#        forces_col = data.iloc[:, (4*test_id)-1].values
#        distances_col = data.iloc[:, 4*test_id].values
#        df = pd.DataFrame(forces_col, index=distances_col, columns=[test_id])
#
#        print(test_id)
#        fname = '{} {}.csv'.format(CSV.stem, test_id)
#        df.to_csv(fname)
#        dataframes.append(df)
#
#    forces = pd.concat(dataframes, axis=1)
