# single-cell-proteomics
Group Project for BIO 465
Winter 2022


## Purpose of this project
Proteomic mass spectrometry data often uses machine learning to process data more accurately. One example of this is to learn the characteristic features of peptide spectra (see PMID: 18563926). The recent rise of single cell proteomics has enabled us to identify and quantify proteins found in a single cell - greatly advancing our understanding of cellular processes and environmental response. Unfortunately, single cell proteomics data have very different characteristics than traditional proteomics data. Therefore, all of the machine learning models built on traditional data are failing with single cell data. This project created a Bayes Net for the probabilities of features in MS/MS data (fragment ions) and compared it to a Bayes Net made from traditional data.

## Organization
This repository is broken up into several different folders and ipython notebooks
The data folder contains the processed data we used to create the figures and can be downloaded directly.
To create the processed data, we downloaded the raw data from [MassIVE](https://massive.ucsd.edu/). (Single cell data: MSV000087524, bulk data: MSV000087689) 
The code used to generate our data can be found in data_parser.ipynb

The first figures are for understanding our approach to the problem, so the specific data isn't important. The process to recreate these figures can be found in make_figure1.ipynb and make_figure2.ipynb.

There is another ipython notebook which takes the data from the data folder and uses it to train a ML model, which is used to make the remaining figures. All this can be found in that notebook.


## Files
- combine_psm_mzml.py: 
- combine_parsed_psm.ipynb
- data_parser.py: Used by parse_data.ipynb to take parsed psm files (data/parsed_psm) and combines them by data type (e.g. all_sc.tsv)
