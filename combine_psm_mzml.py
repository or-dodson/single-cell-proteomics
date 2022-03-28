import numpy as np
import pandas as pd
import pyteomics.mzml
import re

MAX_QVALUE = 0.01


def _mzml_helper(row, mzml, data_type="all"):
    scan = str(row['scan'])
    my_id = 'controllerType=0 controllerNumber=1 scan='+ str(scan)
    spectrum_dict = mzml.get_by_id(my_id)

    spectrum_id = spectrum_dict['id']
    retention_time = (spectrum_dict['scanList']['scan'][0].get('scan start time', -1))
    mz_array = list(spectrum_dict['m/z array'])
    intensity_array = list(spectrum_dict['intensity array'])
    
    #base peak intensity
    bpi = spectrum_dict['base peak intensity']
    if (data_type == "base_peak_intensity"):
        return bpi

    #precursor information
    precursor = spectrum_dict['precursorList']['precursor'][0]
    precursor_ion = precursor['selectedIonList']['selectedIon'][0]
    precursor_mz = precursor_ion['selected ion m/z']
    if 'peak intensity' in precursor_ion:
        precursor_intenisty =  precursor_ion['peak intensity']
    else:
        precursor_intenisty = None
    if 'charge state' in precursor_ion:
        precursor_charge = int(precursor_ion['charge state'])
    elif 'possible charge state' in precursor_ion:
        precursor_charge = int(precursor_ion['possible charge state'])
    else:
        precursor_charge = 'NAN'

    all_info = [bpi,mz_array,intensity_array,precursor_intenisty]

    return all_info

# Returns more manageable df with both psm and mzml data
def clean_and_combine(psm_path, mzml_path):
    
    # PSM
    psm = pd.read_csv(psm_path, sep = '\t', dtype={'Base Sequence': str, 'Missed Cleavages': str, 'Peptide Monoisotopic Mass':str, 'Mass Diff (Da)':str,'Mass Diff (ppm)':str,'	Protein Accession':str,'Peptide Description':str, 'Notch':str, 'Num Variable Mods':str, 'Decoy': str})

    # remove columns that we don't use
    psm = psm[['Matched Ion Series', 'Matched Ion Mass-To-Charge Ratios', 'Matched Ion Intensities', 'Matched Ion Counts', 'QValue', 'Full Sequence', 'Previous Amino Acid', 'Next Amino Acid', 'File Name', 'Scan Number']]
    
    # remove rows with qvalue over threshold
    psm = psm[psm['QValue'] < MAX_QVALUE]
    
    psm = psm.rename({"Scan Number": "scan", "Full Sequence": "peptide"}, axis=1)
    
    # remove rows where peptide value isn't clean. Some columns have comments or alternate values
    r = re.compile(r"[^A-Z]+")
    psm = psm[psm.apply(lambda x: False if r.search(x.peptide) else True, axis=1)]

    #remove duplicate scans
    psm = psm.sort_values("QValue")
    psm = psm.drop_duplicates(subset=["scan"], keep="first")
    #make sure dtypes are correct
    psm[["scan"]] = psm[["scan"]].apply(pd.to_numeric)

    # MZML
    mzml = pyteomics.mzml.MzML(mzml_path)
    psm['mzml_info'] = psm.apply(lambda row: _mzml_helper(row, mzml),axis=1)
    psm[['Base Peak Intensity', 'mz_array', 'intensity_array', 'precursor_intenisty']] = pd.DataFrame(psm['mzml_info'].tolist(), index= psm.index)
    psm=psm.drop(columns='mzml_info')
    
    return psm