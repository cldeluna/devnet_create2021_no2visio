#!/usr/bin/python -tt
# Project: devnet_create2021_no2visio
# Filename: app_flow_requirements
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "9/23/21"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
import pandas as pd


def main():

    # Use Pandas to read in an Excel file

    excel_file = 'base_station2tpe_connreq.xlsx'
    df = pd.read_excel(excel_file)
    df.fillna('', inplace=True)

    print(df)

    policy_lod = df.to_dict(orient="records")

    include_ips = False
    sequence_diagram = []

    nodes = set()
    src_nodes = set()
    dst_nodes = set()

    for line in policy_lod:
        print(line)

        if line['From System'] not in src_nodes:
            src_nodes.add(line['From System'])
            nodes.add(line['From System'])

        if line['To System'] not in dst_nodes:
            dst_nodes.add(line['To System'])
            nodes.add(line['To System'])

    print(src_nodes)
    print(dst_nodes)
    print(nodes)

    sequence_diagram.append("sequenceDiagram")

    for line in policy_lod:
        # Sequence Diagram
        ips = ""
        if include_ips:
            ips = line['Destination Hosts/Ips']

        if line['Type'] == "Unidirectional":
            li = f"    {line['From System']}->>+{line['To System']}: {line['Type']} {line['Protocol']} {line['Destination Port']} {ips}"
            sequence_diagram.append(li)
        elif line['Type'] == "Bidirectional":
            li = f"    {line['From System']}->>+{line['To System']}: {line['Type']} {line['Protocol']} {line['Destination Port']} {ips}"
            sequence_diagram.append(li)
            li = f"    {line['To System']}->>+{line['From System']}: {line['Type']} {line['Protocol']} {line['Destination Port']} {ips}"
            sequence_diagram.append(li)

    print(f"\nSequence Diagram")
    for line in sequence_diagram:
        print(line)



# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python app_flow_requirements' ")
    arguments = parser.parse_args()
    main()
