#!/usr/bin/python -tt
# Project: devnet_create2021_no2visio
# Filename: app_flow_requirements
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "9/23/21"
__copyright__ = "Copyright (c) 2021 Claudia"
__license__ = "Python"

import argparse
import base64
import os
import io
import requests
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd


def main():

    # Use Pandas to read in an Excel file

    include_ips = arguments.include_ips
    verbose = arguments.verbose

    excel_file = "base_station2tpe_flows.xlsx"
    print(
        f"\nReading Excel file <{excel_file}> containing Actility ThingPark Enterprise (TPE) LoRaWan Application Flow Requirements into Pandas DataFrame..."
    )
    df = pd.read_excel(excel_file)
    df.fillna("", inplace=True)

    if verbose:
        print(f"\nExample of DataFrame:\n{df.head}")

    # Turn dataframe into List of Dictionaries (lod)
    policy_lod = df.to_dict(orient="records")

    # Initialize a list to hold each line of the Mermaid Diagram
    print(f"\nProcessing data and creating Mermaid Sequence Diagram...")
    sequence_diagram = list()

    # Add header line
    sequence_diagram.append("sequenceDiagram")

    for line in policy_lod:
        # Sequence Diagram
        ips = ""
        if include_ips:
            ips = line["Destination Hosts/Ips"]

        if line["Type"] == "Unidirectional":
            li = f"    {line['From System']}->>+{line['To System']}: {line['Type']} {line['Protocol']} {line['Destination Port']} {ips}"
            sequence_diagram.append(li)
        elif line["Type"] == "Bidirectional":
            li = f"    {line['From System']}->>+{line['To System']}: {line['Type']} {line['Protocol']} {line['Destination Port']} {ips}"
            sequence_diagram.append(li)
            li = f"    {line['To System']}->>+{line['From System']}: {line['Type']} {line['Protocol']} {line['Destination Port']} {ips}"
            sequence_diagram.append(li)

    # Convert list to string to send to Mermaid
    diagram_as_string = "\n".join(sequence_diagram)

    if verbose:
        print(f"\nSequence Diagram:")
        print(diagram_as_string)

    # Directly from Mermaid Tutorial
    # https://mermaid-js.github.io/mermaid/#/Tutorials
    # Manipulating the diagram text to send to Mermaid Ink
    graphbytes = diagram_as_string.encode("ascii")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")

    print(f"\nSending diagram to Mermaid Ink for rendering...")
    response = requests.get("https://mermaid.ink/img/" + base64_string)

    if response.status_code == 200:
        print(f"\t{response.reason} Successfully rendered diagram!!")
        if verbose:
            print(response)
            print(response.status_code)
            print(dir(response))
            print(response.url)

        # Create JPG using Matplotlib
        img = Image.open(io.BytesIO(response.content))
        plt.imshow(img)
        _ = excel_file.split(".")
        jpg_file = f"{_[0]}.jpg"
        txt_file = f"{_[0]}_mermaid_seq_diagram.txt"

        print(
            f"\nSaving text diagram description for revision control to:\n\t{os.getcwd()} > {txt_file}\n"
        )
        with open(txt_file, "w") as fh:
            fh.write(diagram_as_string)

        print(f"\nSaving rendered diagram JPG to:\n\t{os.getcwd()} > {jpg_file}\n")
        plt.savefig(jpg_file)

        print(f"\nURL to Mermaid Ink Diagram:\n{response.url}\n")

    else:
        print(f"\tUnsuccessful API Response {response.status_code} {response.reason}\n")


# Standard call to the main() function.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script Description",
        epilog="Usage: ' python app_flow_requirements' ",
    )
    parser.add_argument(
        "-i",
        "--include_ips",
        help="Show IPs in Sequence diagram",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help="Print values along the way",
        action="store_true",
        default=False,
    )
    arguments = parser.parse_args()
    main()
