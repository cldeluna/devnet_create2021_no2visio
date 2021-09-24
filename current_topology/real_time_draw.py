#!/usr/bin/python -tt
# Project: network_diagrams_py
# Filename: real_time_draw.py
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "1/23/21"
__copyright__ = "Copyright (c) 2021 Claudia"
__license__ = "Python"


import re
import os
import json
import dotenv
import argparse
import gen_utils
from scrapli.driver.core import IOSXEDriver

# Import drawing classes from diagrams
from diagrams import Cluster, Diagram, Edge

# Custom Class so that you can use your own icons
from diagrams.custom import Custom

# Generic Network Icons which are part of the diagrams module
# from diagrams.generic.network import Firewall
# from diagrams.generic.network import Router
# from diagrams.generic.network import Subnet
# from diagrams.generic.network import Switch


def replace_space(text):
    return re.sub(r"\s", "_", text)


def get_via_scrapli(
    dev_dict, show_cmd="show cdp neighbor detail", save_as_json=False, debug=False
):
    """
    Function uses scrapli to get show command and parse returning structured data

    :param dev_dict:
    :param show_cmd:
    :param save_as_json:
    :param debug:
    :return:
    """

    if debug:
        print(f"\n----------- in get_via_scrapli with dev_dict {dev_dict}")

    os.environ["NET_TEXTFSM"] = "./ntc-templates/ntc_templates/templates"

    with IOSXEDriver(**dev_dict) as conn:
        response = conn.send_command(show_cmd)

        structured_result = response.textfsm_parse_output()
        if debug:
            print(response.raw_result)
            print(json.dumps(structured_result, indent=4))

    # If option to save output as JSON Is set - save output to JSON
    if save_as_json:
        filename = f"{dev_dict['host']}_{replace_space(show_cmd)}.json"
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(structured_result, json_file, ensure_ascii=False, indent=4)

    if debug:
        for line in structured_result:
            print(line)
        print("---------- out of get_via_scrapli --------------\n")

    return structured_result


def draw_diagram(
    root_info, nei_list, direction="LR", save_dir=os.getcwd(), save_subdir="test_output"
):
    """
    Function to draw diagram of device CDP neighbors using mingrammer diagram module

    :param root_info:
    :param nei_list:
    :param direction:
    :param save_dir:
    :param save_subdir:
    :return:
    """

    # Initialize dictionary of custom icons and their path
    ilib = gen_utils.init_icon_lib()

    # Separate Services devices from the list
    services_cluster_list = []
    all_other_devs_list = []

    for nei in nei_list:
        # print(f"nei in nei list is {nei}")
        if (
            re.search("AIR-CT2504", nei["platform"])
            or re.search("Meraki", nei["platform"])
            or re.search(r"25\d\d", nei["platform"])
            or re.search("ASA", nei["platform"])
        ):
            services_cluster_list.append(nei)

        else:
            all_other_devs_list.append(nei)

    drawing_fp = os.path.join(
        save_dir, save_subdir, f"{root_info['hostname']}_Current_Topology"
    )
    root_dev = root_info["hostname"]
    labelangle = "45"
    label_idx = 2

    # Instantiate the diagram
    # Direction LR = Left to Right
    # Direction TB = Top to Bottom
    with Diagram(
        f"\n{root_dev}\nCurrent Topology",
        filename=drawing_fp,
        outformat="jpg",
        show=False,
        direction=direction,
    ):

        root = Custom(
            f"-- {root_dev} --\nTotal Neighbors: {len(nei_list)}\n{str(root_info['hardware'])}",
            ilib["rtrgc"],
        )

        # ######  Draw any Services type Equipment like Server Switches, Wireless APs, Wireless Controllers, etc.
        with Cluster("Services"):
            """
            Example of line item in list of dictionary nei_list
              {
                "destination_host": "e0cbbc34acf6",
                "management_ip": "10.1.10.35",
                "platform": "Meraki MR33 Cloud Managed AP",
                "remote_port": "Port 0",
                "local_port": "FastEthernet0",
                "software_version": "1",
                "capabilities": "Router Switch"
              },
            """
            # label_idx = 2
            # Include Wireless controllers and Merki in services
            for snei in services_cluster_list:

                # Adjust the icon used for
                if re.search("AIR-CT2504", snei["platform"]):
                    icon = ilib["wlcw"]
                elif re.search("Meraki", snei["platform"]):
                    icon = ilib["wifipm"]
                elif re.search(r"25\d\d", nei["platform"]):
                    icon = ilib["rtrblkc"]
                elif re.search("ASA", snei["platform"]):
                    icon = ilib["fwlr"]
                else:
                    icon = ilib["swsb"]

                edge_label = f"Local Port {snei['local_port']} -- Remote Port {snei['remote_port']}"

                (
                    root
                    >> Edge(
                        label=edge_label,
                        # taillabel=snei['local_port'],
                        headlabel=snei["remote_port"],
                        labelangle=labelangle,
                        labeldistance=str(label_idx),
                        minlen="1",
                    )
                    >> Custom(
                        f"{snei['destination_host']}\n"
                        f"{snei['platform']}\n"
                        f"{snei['management_ip']}",
                        icon,
                    )
                )
                label_idx = +2

        # ###### DRAW ALL OTHER DEVICES
        label_idx = 2
        for nei in all_other_devs_list:

            edge_label = (
                f"Local Port {nei['local_port']} -- Remote Port {nei['remote_port']}"
            )
            other_dev = Custom(
                f"{nei['destination_host']}\n"
                f"{nei['platform']}\n"
                f"{nei['management_ip']}",
                ilib["swsbg"],
            )
            (
                root
                >> Edge(
                    label=edge_label,
                    # taillabel=snei['local_port'],
                    headlabel=nei["remote_port"],
                    labelangle=labelangle,
                    labeldistance=str(label_idx),
                    minlen="3",
                )
                >> other_dev
            )

            label_idx = +2

    print(f"\n\nDIAGRAM for {root_dev} Complete:\n\t{drawing_fp}\n")

    return drawing_fp


def main():

    # Load Credentials from environment variables
    dotenv.load_dotenv(verbose=True)

    # Set Credentials from Environment
    usr = os.environ["NET_USR"]
    pwd = os.environ["NET_PWD"]
    sec = os.environ["NET_PWD"]

    root_device = {
        "host": arguments.device,
        "auth_username": usr,
        "auth_password": pwd,
        "port": arguments.port,
        "auth_strict_key": False,
    }
    # Get device model, hostname, etc.
    root_dev_info = get_via_scrapli(
        root_device, show_cmd="show version", save_as_json=arguments.save
    )

    # Get and Parse a show command using scrapli and TextFSM
    # Default show command fror the get_via_scrapli function is "show cdp neighbor detail"
    resp = get_via_scrapli(root_device, save_as_json=arguments.save)

    draw_diagram(root_dev_info[0], resp, direction=arguments.direction)


# Standard call to the main() function.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sample Script to Draw the CDP Neighbors of an IOS XE device",
        epilog="Usage: ' python real_time_draw.py' ",
    )

    parser.add_argument("device", help="FQDN or IP of IOS XE device")
    parser.add_argument("-a", "--port", help="SSH Port", action="store", default=22)
    parser.add_argument(
        "-d",
        "--direction",
        help="Diagram direction. Valid values are LR, TB, RL",
        action="store",
        default="LR",
    )
    parser.add_argument(
        "-s", "--save", help="Save Parsed Output", action="store_true", default=False
    )
    arguments = parser.parse_args()
    main()
