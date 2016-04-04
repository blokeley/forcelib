# forcelib

Read CSV files from Emperor software used with Mecmesin tensometers.

The author has no affiliation with Mecmesin.


## Advantages over Microsoft Excel

- `forcelib` is able to handle large datasets.  For example, Excel might
  struggle with 1,000,000 rows or 1,000 tests.

- Easy indexing and slicing of data, for example: by time; displacement;
  or force.  See examples in the [examples](examples) directory.

- Easy plotting, even of large datasets, using `plot_force_v_displacement`
  or custom plotting plotting functions which are easy to write.

- Calculation of the work done (area under the force-displacement curve)
  using the `work` function.


# Requirements

The recommended set-up is to install
[Anaconda](https://www.continuum.io/downloads).  Ensure that you install the
Python 3.4+ verion. If you do this, you will have all of the requirements
satisfied.

The actual requirements are:

- Python 3.4+
- pandas
- numpy
- matplotlib


# Installation

## Official method

1. `git checkout https://github.com/blokeley/forcelib/`
2. `cd forcelib`
3. `pip install -e .`

To update:

1. `git pull`

## Quick-and-dirty method

1. Copy https://raw.githubusercontent.com/blokeley/forcelib/master/forcelib/forcelib.py
   to the directory in which you will be working

If there is much demand from other users, I would consider uploading the
package to PyPI.

# Usage

See the [example programs](examples):

You can run them by typing at the command line a variant like:

`python read.py example_forces_big.csv`

- [read.py](examples/read.py) This is the simplest example.  It reads the
  given CSV file and plots the forces versus displacement.

- [stats.py](examples/stats.py) Select a sub-set of the displacement results
  and calculate certain statistics.

- [work.py](examples/work.py) Calculate the work done (integral of force with
  respect to displacement) during each test.

# Licence

This package is licensed under the MIT licence.  See the [LICENSE](LICENSE)
[sic] file for further details.
