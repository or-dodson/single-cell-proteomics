# Bio 465 Project
*By Evan Dodson, Madelyn Grose, Corbin Day, Robert Oldroyd, and Bryce Lunceford*

## Reproducibility Instructions
Additional detail can be found under the *Additonal Information* section.
1. Install Docker on your machine.
<!-- 2. Clone this git repository to your machine using the command `git clone https://github.com/or-dodson/single-cell-proteomics.git`. -->
2. Run docker using the command `docker run -it -p 8888:8888 evandodson/sc_proteomics /root/single-cell-proteomics/runJupyter.sh`
3. This will start a Jupyter Lab server. To connect to the server, copy and paste the link given in the terminal that looks like `http://127.0.0.1:8888/lab?token=...` into your browser.
4. Once you have access to the Jupyter Lab server, the notebooks need only be run to reproduce the results that we obtained.

## Additional Information
### Installing Docker
Docker can easily be installed on a variety of Operating Systems. For convenience, we provide instructions for Ubuntu, MacOS, and Windows.
* Ubuntu
    * Run the command `sudo apt install docker.io -y && sudo usermod -aG docker $(whoami) && sudo reboot`
* MacOs
    * Follow [these instructions](https://docs.docker.com/desktop/mac/install/)
* Windows
    * Follow [these instructions](https://docs.docker.com/desktop/windows/install/)

### Downloading Data
Cleaned data is included in the docker image, but may also be downloded from [Box](https://byu.box.com/s/hk9d7mnv0fmmnu1y5vzyj86yn15a3toq).

Additionally, raw data files can be downloaded from [Box](https://byu.box.com/s/rnnvt0jyq5r60h3va8mbs14zejh8enag) if desired.

## File Descriptions
Descriptions of files contained in the repository.
* `analyze_data.ipynb`: Performs analysis on the data to show statistical significance.
* `combine_parsed_psm.ipynb`
* `combine_psm_mzml.py`
* `combined_psm_parser.py`
* `data_parser.py`: Used by parse_data.ipynb to take parsed psm files (data/parsed_psm) and combines them by data type (e.g. all_sc.tsv)
* `docker`: Contains the Dockerfile for this project
    * `Dockerfile`: Used by Docker
* `figures`: Folder that contains code to generate the figures
    * `figure3.ipynb`: Contains a function to make figure 3 given proper data.
    * `make_figure3.ipynb`: The notebook that generated Figure 3.
* `ion_tables.ipynb`: Contains code to create ion tables.
* `IonCountChiSquared.ipynb`: Performs $\chi^2$ analysis on the data to show statistical significance.
* `parse_raw_data.ipynb`
* `README.md`: This file
* `runJupyter.sh`: Starts the Jupyter Lab server in the Docker container.
