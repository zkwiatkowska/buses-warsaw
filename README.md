# Buses Warsaw (BWaw)
Library for downloading and analysing data from API of [UM Warsaw](https://api.um.warszawa.pl/). This project was done as a part of the *Python for Data Analysis* subject in the Faculty of Mathematics, Informatics and Mechanics of University of Warsaw. 

## Installation
In order to install library, you need to clone the repository and run:
```shell script
git clone https://github.com/zkwiatkowska/buses-warsaw.git
cd buses-warsaw
pip install .
```

## Where to start
All code functionality is described in modules docstrings, but also in the prepared notebooks.
To see notebooks, in the **project root** run:
```shell script
jupyter notebook
```
Notebooks are stored [here](examples/notebooks):
- [data download](examples/notebooks/downloading_data.ipynb) - shows how to download and store data,
- [data analysis](examples/notebooks/data_analysis.ipynb) - shows basic insights that can be extracted from code.

## Tests
In order to run test simply run
```shell script
pytest
```

## Other information
If you need any more information about this code, please contact Zuzanna Kwiatkowska (*zk420176@students.mimuw.edu.pl*).
