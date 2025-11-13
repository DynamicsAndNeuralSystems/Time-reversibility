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
Data used in "A data-driven approach to identifying statistical indicators of temporal asymmetry" is available at **zenodo**. To run the analysis, place the folder `data-tr` into the `Time-reversibility` repo.

#### Pre-processed data
The folder `data-tr/main-analysis/data-analysis/` contains:
- `df_TS_DataMat_diff.csv`: pre-processed dataset of feature differences, $\Delta f_i = f_i -\tilde{f_i}$, $i\in\{1,...,6082\}$ between a feature $f_i$ computed on forward time series and reversed, $\tilde f_i$;
- `common_ops.csv`: set of features after pre-processing;


#### Time series
Time series of the simulated discrete-time and continuous-time processes are stored in `data-tr/main-analysis/time-series/data-dsct` and `data-tr/main-analysis/time-series/data-cnt`, respectively. Each folder named after a process contains 100 realizations 5000-samples long forward in time (files named `[process_label]_[idx_ts].txt`) and the respective 100 realizations flipped in time (`[process_label]_reverse_[idx_ts].txt`).

#### _hctsa_ matrices
Matrices obtained from the _hctsa_ analysis of the time series above are contained in `data-tr/main-analysis/hctsa/hctsa-dsct` and `data-tr/main-analysis/hctsa/hctsa-cnt`, respectively. Each folder contains:

- `HCTSA_frwd.mat` file resulting from the _hctsa_ analysis of forward time series;
- `HCTSA_bkwd.mat` file resulting from the _hctsa_ analysis of reversed time series;

### Analysis 
Code for the analysis of the feature difference dataset `df_TS_DataMat_diff.csv` is in the [python](/src/main/python/) folder.

#### Time-reversal invariant features
The notebook [1-zero_features.ipynb](src/main/python/1-zero_features.ipynb) extracts features that are insensitive to time reversibility.

#### Statistics for reversibility
The notebook [2-1NN_classification.ipynb](src/main/python/2-1NN_classification.ipynb) assigns the accuracy of classification between the reversible and irreversible groups to each feature $f_i$. We used the performance of a 1-nearest neighbor (1-NN) classifier in the space of each $f_i$, evaluated using a leave-one-process-out cross-validation strategy.

The notebook [3-feature_selection.ipynb](src/main/python/3-feature_selection.ipynb) extracts the set of top-performing features, characterized by an accuracy greater than a given threshold. We chose 72% to encompass a sufficiently large set of features for analysis. Distributions of $|\Delta f_i|$ can be reproduced using the notebook [4-boxes.ipynb](src/main/python/4-boxes.ipynb).
<p align="center">
  <img src="src/figures-paper/Distribution.png" width="800">
</p>

#### Statistical signatures of irreversibility are process-dependent
The notebook [5-min_max.ipynb](src/main/python/5-min_max.ipynb) analyses the strength and weaknesses of diverse top-performing features in detecting the reversibility of specific simulated processes computing the accuracy of classification per process (referred to as "left-out accuracy"). The notebook can be used to reproduce figures (a) and (d) below while distributions of $|\Delta f|$ in (b) and (c) can be reproduced using the notebook [4-boxes.ipynb](src/main/python/4-boxes.ipynb).
<p align="center">
  <img src="src/figures-paper/Min-Max.png" width="800">
</p>

#### Additional visualizations
The notebook [6-inspect_good_features.ipynb](src/main/python/6-inspect_good_features.ipynb) contains a hierarchical clustering analysis to identify similarities across features.

The notebook [7-plot_distributions.ipynb](src/main/python/7-plot_distributions.ipynb) contains an alternative plot of the distribution of $|\Delta f|$ per process.


## 2. From scratch
### Data generation
To run the python code which generates most of the data files, run the following:

    uv run src/main/data-generation/discrete-time/discrete_data_generation.py
    uv run src/main/data-generation/continuous-time/continuous_data_generation.py

The coloured noise processes are currently written in Matlab and are stored in the `src/main/data-generation/noise_generation/` directory. To generate the data, run the `src/main/data-generation/noise_generation/noise_generator.m` script.

### _hctsa_ analysis
To run the analysis you need to have [_hctsa_](https://github.com/benfulcher/hctsa) installed.
#### Step 1
**Set-up time series**: input files `INP_ts_[dsct/cnt]_[frwd/bkwd].txt` with the path of time series for the _hctsa_ run can be created using [INP_file_generation_dsct.py](src/main/analysis-_hctsa_/run/INP_file_generation_dsct.py) and [INP_file_generation_cnt.py](src/main/analysis-hctsa/run/INP_file_generation_cnt.py) files.

**Set-up features**: input files with operations [INP_ops.txt](src/main/analysis-hctsa/run/INP_ops.txt) and [INP_mops.txt](src/main/analysis-hctsa/run/INP_mops.txt) for the _hctsa_ run.

#### Step 2
Run the _hctsa_ analysis following the instructions in the comprehensive [documentation](https://time-series-features.gitbook.io/hctsa-manual/).

#### Step 3
**Create csv files** (optional): if you want csv files of the results run the script [create_csv.m](src/main/analysis-hctsa/pre-processing/create_csv.m).

**Create matrix of differences**: 

### Notes on package management

uv will create a virtual environment `.venv` for you in the root directory of the project after you first run `uv sync`. Make sure to use this virtual environment when running the Jupyter notebooks in this repositroy!

## Contact

Please contact [Teresa Dalle Nogare](mailto:teresa.dallenogare@sydney.edu.au) with any questions.
