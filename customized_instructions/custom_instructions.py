#!/usr/bin/python -tt
# Project: devnet_create2021_no2visio
# Filename: custom_instructions
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
import jinja2
import datetime
import requests
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd


def j2render(cfg_template_values, j2_template, debug=False):

    # #############################################
    # ## Render the Jinja2 Template with the values
    # #############################################

    if debug:
        print(f"j2_template: {j2_template}")

    with open(j2_template) as file_:
        template = jinja2.Template(file_.read())

    rendered = template.render(cfg=cfg_template_values)
    if debug:
        print(rendered)

    return rendered


def mermaid_render(diagram_as_string, filename="mermaid_diagram", save_jpg=False, debug=False):
    """
    Render a Mermaid Ink Diagram from diagram string

    :param diagram_as_string:
    :param filename: optional filename header
    :param debug: optional verbose printing
    :param save_jpg:
    :param debug:
    :return: response.url

    """

    # Directly from Mermaid Tutorial
    # https://mermaid-js.github.io/mermaid/#/Tutorials
    # Manipulating the diagram text to send to Mermaid Ink
    graphbytes = diagram_as_string.encode("ascii")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")

    print(f"\nSending diagram to Mermaid Ink for rendering...")
    response = requests.get('https://mermaid.ink/img/' + base64_string)

    if response.status_code == 200:
        print(f"\t{response.reason} Successfully rendered diagram!!")
        if debug:
            print(response)
            print(response.status_code)
            print(dir(response))
            print(response.url)

        # Create JPG using Matplotlib
        img = Image.open(io.BytesIO(response.content))
        plt.imshow(img)
        jpg_file = f"{filename}_flow_diagram.jpg"
        txt_file = f"{filename}_mermaid_seq_diagram.txt"

        print(f"\nSaving text diagram description for revision control to:\n\t{os.getcwd()} > {txt_file}")
        with open(txt_file, 'w') as fh:
            fh.write(diagram_as_string)

        if save_jpg:
            print(f"\nSaving rendered diagram JPG to:\n\t{os.getcwd()} > {jpg_file}\n")
            plt.savefig(jpg_file)

        if debug:
            print(f"\nURL to Mermaid Ink Diagram:\n{response.url}\n")

    else:
        print(f"\tUnsuccessful API Response {response.status_code} {response.reason}\n")

    return response.url


def main():
    """
    Main function to generate a customized Mermaid sequence diagram for a set of sites supporting a Global
    LoraWan Gateway Deployment
    :return:
    """

    # Date stamp for Report if one already exists
    file_timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    dattim = format(datetime.datetime.now())

    # Use Pandas to read in an Excel file
    excel_file = 'sites_base_stations.xlsx'
    print(f"\nReading Excel file <{excel_file}> "
          f"Site information for each LoraWan Gateway (Base Station) into Pandas DataFrame...")
    df = pd.read_excel(excel_file)
    df.fillna('', inplace=True)

    # Turn dataframe into List of Dictionaries (lod)
    sites_lod = df.to_dict(orient="records")

    # Iterate of the each site dict, generate the custom flow sequence diagram, and generate the report
    for site_dict in sites_lod:
        print(f"\n================ Processing site {site_dict['Site']}...")

        # Bad idea to change the data structure you are iterating over so copy site_dict so we can add values
        # sd (site_dict plus additional values) will be sent to the Jinja2 Report Template
        sd = site_dict.copy()

        flow_j2template = "base_station2tpe_flows_mermaid_seq.j2"

        print(f"\nCreating mermaid drawing in text...")
        diagram_text = j2render(site_dict, flow_j2template)

        diag_url = mermaid_render(diagram_text,filename=f"{site_dict['Site']}")

        # Add new information to the site dict copy, namely the URL and the date
        sd.update({"url": diag_url})
        sd.update({"date": dattim})

        report_j2template = "BaseStation_FWL_Policy_Template.j2"

        markdown_report = j2render(sd, report_j2template)

        output_filename = f"{site_dict['Site']}_BaseStationGW_FWLPolicy.md"
        print(f"\nSaving rendered Markdown Report to:\n\t{os.getcwd()} > {output_filename}\n")
        with open(output_filename, "w") as outfile:
            outfile.write(markdown_report)


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python custom_instructions' ")

    arguments = parser.parse_args()
    main()
