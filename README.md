# A data-driven approach to identifying statistical indicators of temporal asymmetry
This repository contains all code needed to reproduce analyses presented in our preprint "**A data-driven approach to identifying statistical indicators of temporal asymmetry**". 
Time series and pre-processesd data are openly available (**zenodo**).
The repository also contains code for generating data and running the analysis from scratch.

# Installation

Python dependencies for this repository are managed via [uv](https://docs.astral.sh/uv/). To install uv on Mac/Linux, run the following command in your terminal:

    curl -LsSf https://astral.sh/uv/install.sh | sh

You may also want to install shell autocompletion for ease of use, which you can do by running

    echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bash_profile
    echo 'eval "$(uvx --generate-shell-completion bash)"' >> ~/.bash_profile

after installing uv (if you're on linux and you have a `.bashrc` instead of a `.bash_profile`, change the above accordingly).

To install this repository and its dependencis, run the following in a terminal:
    
    git clone git@github.com:teresa-dn/Time-reversibility.git
    cd Time-reversibility
    uv sync

# Usage
## 1. Using supplied pre-processed data to reproduce results
### Data availability
Data used in "A data-driven approach to identifying statistical indicators of temporal asymmetry" is available at **zenodo**. To run the analysis, place the folder `data-time-reversibility` into the `Time-reversibility` repo.

Time series of the simulated processes are stored in `data-time-reversibility\main-analysis`
## 2. From scratch
### Data generation
To run the python code which generates most of the data files, run the following:

    uv run src/main/data-generation/discrete-time/discrete_data_generation.py
    uv run src/main/data-generation/continuous-time/continuous_data_generation.py

The coloured noise processes are currently written in Matlab and are stored in the `src/main/data-generation/noise_generation/` directory. To generate the data, run the `src/main/data-generation/noise_generation/noise_generator.m` script.

### Notes on package management

uv will create a virtual environment `.venv` for you in the root directory of the project after you first run `uv sync`. Make sure to use this virtual environment when running the Jupyter notebooks in this repositroy!

## Contact

Please contact [Teresa Dalle Nogare](mailto:teresa.dallenogare@sydney.edu.au) with any questions.
