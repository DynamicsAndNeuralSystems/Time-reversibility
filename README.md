# Time-reversibility

## Data generation
Folder contains code to generate time-series dataset of both discrete-time and continuous-time processes.

## Installation and Usage

Dependencies for this repository are managed via [poetry](https://python-poetry.org/). To install poetry on Mac/Linux, run the following command in your terminal:

    curl -sSL https://install.python-poetry.org | python3 -

and follow the remaining installation steps described [here](https://python-poetry.org/docs/#installing-with-the-official-installer). You may also want to install `poetry shell` for ease of use, which you can do by running

    poetry self add poetry-plugin-shell

after installing poetry.

To install this repository and its dependencis, run the following in a terminal:
    
    git clone git@github.com:teresadallenogare/Time-reversibility.git
    cd Time-reversibility
    poetry install

To run the code which generates most of the data files, run the following:

    poetry shell
    python src/discrete_data_generation.py
    python src/continuous_data_generation.py

The coloured noise processes are currently written in Matlab and are stored in the `src/noise_generation/` directory. To generate the data, run the `src/noise_generation/noise_generator.m` script.

## Contact

Please contact [Teresa Dalle Nogare](mailto:teresa.dallenogare@sydney.edu.au) with any questions.
