from doctest import master
import pandas as pd
import numpy as np
import re

MAX_QVALUE = 0.01
MASS_SECTOR_1 = 600
MASS_SECTOR_2 = 1200
INTENSITY_BIN_1 = 1 / 3
INTENSITY_BIN_2 = 2 / 3
AMINO_ACIDS = {
    "G" : 57.02,
    "A" : 71.04,
    "S" : 87.03,
    "P" : 97.05,
    "V" : 99.07,
    "T" : 101.05,
    "C" : 103.01,
    "I" : 113.08,
    "L" : 113.08,
    "N" : 114.04,
    "D" : 115.03,
    "Q" : 128.06,
    "K" : 128.09,
    "E" : 129.04,
    "M" : 131.04,
    "H" : 137.06,
    "F" : 147.07,
    "R" : 156.1,
    "Y" : 163.06,
    "U" : 150.95,
    "W" : 186.08,
    "O" : 237.15
}

def clean_data(file_path):

    # read in the file
    df = pd.read_csv(file_path, sep='\t')
   
    # filter by q value
    df = df[df["QValue"] <= MAX_QVALUE]

    # remove unwanted columns
    df = df[["Matched Ion Mass-To-Charge Ratios", "Matched Ion Intensities", "peptide", "File Name", "scan", "Base Peak Intensity"]]

    # remove rows where peptide value isn't clean. Some columns have comments or alternate values
    r = re.compile(r"[^A-Z]+")
    df = df[df.apply(lambda x: False if r.search(x.peptide) else True, axis=1)]

    # create the template df with a row for all ions, even the ones missing from the annotations
    template_df = create_template_df(df)

    # create df for mass values
    df_mz = create_mass_df(df)

    # create df for intensity values
    df_intensities = create_intensity_df(df)

    # join mass and intensity dfs with the template df
    master_df = join_tables(template_df, df_mz, df_intensities)

    # fill in missing mass and intensity values for unobserved ions
    master_df = plug_holes(master_df)

    # bin the mass and intensity values
    master_df = bin(master_df)

    return master_df

def create_template_df(df):

    scans = df.scan.tolist()
    peptides = df.peptide.tolist()
    file_names = df["File Name"].tolist()

    all_ions = list()

    for i in range(len(scans)):
        scan = scans[i]
        pep = peptides[i]
        file_name = file_names[i]
        
        B = [[scan, pep, file_name, 'b', p] for p in range(1, len(pep))]
        Y = [[scan, pep, file_name, 'y', p] for p in range(1, len(pep))]
        
        all_ions.extend(B)
        all_ions.extend(Y)

    return pd.DataFrame(all_ions, columns=["scan", "peptide", "file_name", "Ion Type", "Ion Number"])

def create_mass_df(df):
    # create Mass table to join with the complete table
    # "explode" rows to get intensity and mass data for each ion on a single row
    df_mz = df[["Matched Ion Mass-To-Charge Ratios", "peptide", "scan", "File Name"]].copy()
    df_mz["Matched Ion Mass-To-Charge Ratios"] = df_mz["Matched Ion Mass-To-Charge Ratios"].str.split(";")
    df_mz = df_mz.explode("Matched Ion Mass-To-Charge Ratios")
    df_mz["Matched Ion Mass-To-Charge Ratios"] = df_mz["Matched Ion Mass-To-Charge Ratios"].str.split(", ")
    df_mz = df_mz.explode("Matched Ion Mass-To-Charge Ratios")
    df_mz["Matched Ion Mass-To-Charge Ratios"] = df_mz["Matched Ion Mass-To-Charge Ratios"].str.strip("[]")
    df_mz["Matched Ion Mass-To-Charge Ratios"] = df_mz["Matched Ion Mass-To-Charge Ratios"].str.split(":")
    df_mz[["Ion Type", "Mass"]] = df_mz["Matched Ion Mass-To-Charge Ratios"].to_list()
    df_mz.drop("Matched Ion Mass-To-Charge Ratios", axis=1, inplace=True)
    df_mz["Ion Type"] = df_mz["Ion Type"].str.split('+')
    df_mz["Ion Type"] = df_mz["Ion Type"].apply(lambda x: x[0])
    df_mz["Ion Number"] = df_mz["Ion Type"].apply(lambda x: x[1:])
    df_mz["Ion Type"] = df_mz["Ion Type"].apply(lambda x: x[0])
    df_mz = df_mz.astype({"Mass": float})
    df_mz = df_mz.astype({"Ion Number": int})
    df_mz.rename(columns = {"File Name": "file_name"}, inplace = True)

    return df_mz

def create_intensity_df(df):
    # create Intensity table to join with the complete table
    # "explode" rows to get intensity and mass data for each ion on a single row
    df_intensities = df[["Matched Ion Intensities", "Base Peak Intensity", "peptide", "scan", "File Name"]].copy()
    df_intensities = df_intensities.explode("Matched Ion Intensities")
    df_intensities["Matched Ion Intensities"] = df_intensities["Matched Ion Intensities"].str.split(", ")
    df_intensities = df_intensities.explode("Matched Ion Intensities")
    df_intensities["Matched Ion Intensities"] = df_intensities["Matched Ion Intensities"].str.split(';')
    df_intensities = df_intensities.explode("Matched Ion Intensities")
    df_intensities["Matched Ion Intensities"] = df_intensities["Matched Ion Intensities"].str.strip("[]")
    df_intensities["Matched Ion Intensities"] = df_intensities["Matched Ion Intensities"].str.split(":")
    df_intensities[["Ion Type","Intensity"]] = df_intensities["Matched Ion Intensities"].to_list()
    df_intensities.drop("Matched Ion Intensities", axis=1, inplace=True)

    df_intensities["Ion Type"] = df_intensities["Ion Type"].str.split('+')
    df_intensities["Ion Type"] = df_intensities["Ion Type"].apply(lambda x: x[0])
    df_intensities["Ion Number"] = df_intensities["Ion Type"].apply(lambda x: x[1:])
    df_intensities["Ion Type"] = df_intensities["Ion Type"].apply(lambda x: x[0])
    df_intensities = df_intensities.astype({"Intensity": float})
    df_intensities["Intensity"] = df_intensities["Intensity"] / df_intensities["Base Peak Intensity"]
    df_intensities.drop("Base Peak Intensity", axis=1, inplace=True)

    df_intensities.rename(columns = {'File Name':'file_name'}, inplace = True)
    df_intensities = df_intensities.astype({"Ion Number": int})
    
    return df_intensities

def join_tables(template, mass, intensity):
    # join mass to template
    master_df = pd.merge(template, mass, on = ["scan", "peptide", "file_name", "Ion Type", "Ion Number"], how="left")

    # join intensity to master
    master_df = pd.merge(master_df, intensity, on = ["scan", "peptide", "file_name", "Ion Type", "Ion Number"], how="left")

    return master_df

def plug_holes(df):

    # set missing intensity values to 0
    df['Intensity'] = np.where(df["Intensity"].isna(), 0, df["Intensity"])

    # add in missing mass values
    missing_masses = df.apply(lambda x: convert_peptide_frag_to_mass(x[1], x[4], x[3] == 'y') if pd.isnull(x[5]) else None, axis=1)
    df['Mass'] = np.where(df["Mass"].isna(), missing_masses, df["Mass"])

    return df

def convert_peptide_frag_to_mass(full_peptide, frag_length, y_ion=False):
    mass = 0
    # y_ion is a bool to check whether the fragment mass should be constructed from the front or the back
    if not y_ion:
        for i in range(frag_length):
            mass += AMINO_ACIDS[full_peptide[i]]
    else:
        for i in range(frag_length, 0, -1):
            mass += AMINO_ACIDS[full_peptide[-i]]
            
    return mass

def bin(df):
    df["Mass"] = df["Mass"].apply(lambda x: 1 if x <= MASS_SECTOR_1 else 2 if x <= MASS_SECTOR_2 else 3)
    df.rename(columns={"Mass": "sector"}, inplace=True)
    df["Intensity"] = df["Intensity"].apply(lambda x: "none" if x == 0 else "low" if x <= INTENSITY_BIN_1 else "medium" if x <= INTENSITY_BIN_2 else "high")

    return df
    