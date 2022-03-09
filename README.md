# single-cell-proteomics
Group Project for BIO 465
Winter 2022


## Purpose of this project
Single cell proteomics is important, but hard.
Single cell data and bulk proteomics data are run through ML and compared

## Organization
This repository is broken up into several different folders and ipython notebooks
Data - This folder contains the data we used to create the figures and can be downloaded directly.
The raw data comes from MassIVE (Single cell data: MSV000087524, bulk data: MSV000087689), and the code used to generate our data can be found in data_parser.ipynb

The first figures are for understanding our approach to the problem, so the specific data isn't important. The process to recreate these figures can be found in make_figure1.ipynb and make_figure2.ipynb.

There is another ipython notebook which takes the data from the data folder and uses it to train a ML model, which is used to make the remaining figures. All this can be found in that notebook.

![Overview of structure and data flow for this project](../main/images/project_structre_overview.png)
