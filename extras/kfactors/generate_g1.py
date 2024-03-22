import argparse
import os
from datetime import datetime as dt

import lhapdf
import numpy as np
import pineappl
import yaml


def get_prediction(folder: str) -> np.ndarray:
    """
    Get predictions by convoluting a PineAPPL grid with a LHAPDF PDF.

    Parameters
    ----------
    folder: str
        Path to the kinematics.yaml grid file.
    pdf_name : str
        The name of the LHAPDF dataset.

    Returns
    -------
    prediction : np.ndarray
        Computed predictions.
    """

    with open(folder + "/kinematics.yaml") as file:
        data = yaml.safe_load(file)

    bins = data["bins"]
    prediction = np.zeros(len(bins))
    for i, bin in enumerate(bins):
        prediction[i] = 1 / (2 * bin["x"]["mid"])

    return prediction


def save_data(
    data: np.ndarray,
    dataset_name: str,
    author_name: str,
    theory_name: str,
    output_name: str = "results",
):
    """
    Save computed data to a file with metadata.

    Parameters
    ----------
    data : np.ndarray
        Computed data.
    dataset_name : str
        Name of the dataset.
    author_name : str
        Name of the author.
    theory_name : str
        Name of the theory.
    output_name : str, optional
        Output folder name, default is "results".
    """
    strf_data = ""
    for i in range(data.shape[0]):
        strf_data += f"{data[i]}  0.0\n"

    date = dt.now().date()
    string = (
        f"""********************************************************************************
SetName: {dataset_name}
Author: {author_name}
Date: {date}
CodesUsed: https://github.com/NNPDF/yadism
TheoryInput: {theory_name}
Warnings: 1/2x normalization for {dataset_name}
********************************************************************************
"""
        + strf_data
    )

    os.makedirs(output_name, exist_ok=True)
    with open(output_name + f"/CF_NRM_{dataset_name}_G1.dat", "w") as file:
        file.write(string)


# Create an argument parser
parser = argparse.ArgumentParser()
parser.add_argument("folder", help="The folder name of the commondata set")
parser.add_argument("--author", help="The name of the author", default="A.J. Hasenack")
parser.add_argument(
    "--theory", help="The theory used, formatted as 'theory_'+int", default="theory_800"
)
parser.add_argument("--output", help="The name of the output folder", default="results")
args = parser.parse_args()

# Extract command line arguments
folder_name = args.folder
author = args.author
theory = args.theory
output = args.output

dataset_name = os.path.splitext(
    os.path.splitext(os.path.basename(os.path.normpath(folder_name)))[0]
)[0]

# Get predictions and save data
data = get_prediction(folder_name)
save_data(data, dataset_name, author, theory, output)
