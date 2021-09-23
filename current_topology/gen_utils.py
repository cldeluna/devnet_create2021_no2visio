#!/usr/bin/python -tt
# Project: network_diagrams_py
# Filename: gen_utils
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "1/23/21"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
import os
import json

# https://icons8.com/license
# https://icons8.com/
# <a target="_blank" href="https://icons8.com/icons/set/switch">Switch icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
def init_icon_lib():
    """
    Dictionary of icons and locations
    :return: icon_lib - a dictionary of icon locations
    """

    cdw = os.getcwd()
    icon_folder = "icons"

    icon_lib = {
        "fwlb": os.path.join(cdw, icon_folder, "icons8-firewall-50-blue.png"),
        "fwlo": os.path.join(cdw, icon_folder, "icons8-firewall-50-orange.png"),
        "fwlr": os.path.join(cdw, icon_folder, "icons8-firewall-50-red.png"),
        "wlcb": os.path.join(cdw, icon_folder, "icons8-game-controller-50-blue.png"),
        "wlcw": os.path.join(cdw, icon_folder, "icons8-game-controller-wireless.png"),
        "sp": os.path.join(cdw, icon_folder, "icons8-internet-hub-50.png"),
        "rtrbc": os.path.join(cdw, icon_folder, "icons8-router-50-circle-blue.png"),
        "rtrgc": os.path.join(cdw, icon_folder, "icons8-router-50-circle-green.png"),
        "rtrblkc": os.path.join(cdw, icon_folder, "icons8-router-50.png"),
        "swsblk": os.path.join(cdw, icon_folder, "icons8-switch-50-square-black.png"),
        "swsb": os.path.join(cdw, icon_folder, "icons8-switch-50-square-blue.png"),
        "swsbb": os.path.join(cdw, icon_folder, "icons8-switch-50-squareb-black.png"),
        "swsbg": os.path.join(cdw, icon_folder, "icons8-switch-50-squareb-green.png"),
        "wifipm": os.path.join(cdw, icon_folder, "icons8-wi-fi-50-purplemaze.png"),
        "wifib": os.path.join(cdw, icon_folder, "icons8-wi-fi-50-blue.png"),

    }

    return icon_lib


def sub_dir(output_subdir, debug=False):
    # Create target Directory if does not exist
    if not os.path.exists(output_subdir):
        os.mkdir(output_subdir)
        print("Directory ", output_subdir, " Created ")
    else:
        if debug:
            print("Directory ", output_subdir, " Already Exists")


def load_json(json_payload_file):

    with open(json_payload_file) as payload:
        data = json.load(payload)

    return data


def main():
    pass


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Utility Functions for Repository. Not intended to execute directly",
                                     epilog="Usage: ' python gen_utils' ")

    arguments = parser.parse_args()
    main()
