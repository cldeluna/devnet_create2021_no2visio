#!/usr/bin/python -tt
# Project: network_diagrams_py
# Filename: pgv_draw
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "1/24/21"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
import pygraphviz as pgv
import re
import os
import datetime
import gen_utils


def pgv_diagram(root_info, nei_list, direction="LR", save_dir=os.getcwd(), save_subdir="test_output"):


    # Initialize dictionary of custom icons and their path
    # Custom Icons Provided by Icons8
    # https://icons8.com/?ref=juanpablocorsi734

    ilib = gen_utils.init_icon_lib()
    # dict_keys(['fwlb', 'fwlo', 'fwlr', 'wlcb', 'wlcw', 'sp', 'rtrbc', 'rtrgc', 'rtrblkc', 'swsblk', 'swsb', 'swsbb', 'swsbg', 'wifipm', 'wifib'])


    image_format = "png"
    drawing_filename = f"{root_info['hostname']}_Current_Topology_pgv"
    drawing_fp = os.path.join(save_dir, save_subdir, f"{drawing_filename}.{image_format}")
    root_dev = root_info['hostname']

    # By default the graph is strict in that you cannot have multiple links to the same node and has no directionality
    # G = pgv.AGraph()

    # Since it not uncommon to have redundant links in a network we set strict to false and we can set directionality
    # to true or false as preferred
    G = pgv.AGraph(strict=False, directed=True, mode="hier")

    # Set desired Graph Attributes
    G.graph_attr['label'] = f"{root_dev}\nCurrent Topology\nDrawn with PyGraphviz"
    G.graph_attr['fontname'] = 'arial'
    G.graph_attr['splines'] = 'compound'

    #Add the Root Device Node and set its attributes
    G.add_node(root_dev)
    # Get the Root Device Node and set attributes
    rnode = G.get_node(root_dev)
    rnode.attr['label'] = root_dev
    rnode.attr['image'] = ilib['swsb']
    rnode.attr['labelloc'] = "c"
    # n.attr['bgcolor'] = "grey"
    # n.attr['font color'] = "white"
    rnode.attr['color'] = "#ffffff"

    # Iterate over all the CDP neighbors
    for nei in nei_list:

        # Create and add a node for each destingation host from the CDP Neighbors data
        G.add_node(nei['destination_host'])

        # Get the neighbor node object so we can set its attributes
        nnode = G.get_node(nei['destination_host'])

        # Set the appropriate icon for each type of device
        if re.search("AIR-CT2504", nei['platform']):
            icon = ilib["wlcw"]
        elif re.search("Meraki", nei['platform']):
            icon = ilib['wifipm']
        elif re.search(r'25\d\d', nei['platform']):
            icon = ilib['rtrblkc']
        elif re.search("ASA", nei['platform']):
            icon = ilib['fwlr']
        else:
            icon = ilib["swsb"]

        # Set the Node Attributes
        nnode.attr['label'] = f"{nei['destination_host']}\n{nei['management_ip']}"
        nnode.attr['image'] = icon
        nnode.attr['labelloc'] = "c"
        nnode.attr['shape'] = "none"
        # n.attr['bgcolor'] = "grey"
        nnode.attr['font color'] = "blue"
        nnode.attr['color'] = "#ffffff"

        # Create EDGES (Connections)
        # Connect Root device node to each neighbor node
        G.add_edge(root_dev, nnode, headlabel=nei['remote_port'], minlen="3")

    # Save the DOT file
    # This file can be kept under revision control
    dot_fp = os.path.join(save_dir, save_subdir, f"{drawing_filename}.dot")
    G.write(dot_fp)

    # layout information, see layout() or specify prog=neato|dot|twopi|circo|fdp|nop
    # Default is neato
    layout='dot'
    G.layout(layout)
    G.draw(drawing_fp)

    print(f"\n\nDIAGRAM in {image_format.upper()} Format for {root_dev} Complete:\n\t{drawing_fp}_pgv.{image_format}")

    print(f"\n\nDIAGRAM in DOT Notation for {root_dev} Complete:\n\t{drawing_fp}_pgv.dot\n")


def main():
    """
    Example script using pygraphviz and saved show command output to generate current topology diagram
    :return:
    """

    # Load show version output (saved as JSON)
    root_dev_info = gen_utils.load_json("10.1.10.212_show_version.json")

    # Load show cdp neighbor detail output
    resp = gen_utils.load_json("10.1.10.212_show_cdp_neighbor_detail.json")

    # Draw the Current Topology using pygraphviz
    pgv_diagram(root_dev_info[0], resp)


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python pgv_draw' ")

    #parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    parser.add_argument('-a', '--all', help='Execute all exercises in week 4 assignment', action='store_true',
                        default=False)
    arguments = parser.parse_args()
    main()
