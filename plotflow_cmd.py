#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Distributed under terms of the MIT license.

"""
A executable-like plotting utility for flow depths.
"""
import os
import sys
import argparse
import logging
import numpy
import matplotlib.colors
import matplotlib.colorbar
from matplotlib import pyplot


# logger
logger = logging.getLogger("plotflow_cmd.py")
logger.setLevel(logging.DEBUG)

# file log
fh = logging.FileHandler("neck_test_plotflow_cmd.log", "w", "utf-8")
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s'))

# add handlers to the logger
logger.addHandler(fh)

def plot_single_frame(casepath, frameno, max_level, subtitle, outputfile):
    """Plot flows of a single case."""
    from clawpack import pyclaw

    # paths
    casepath = os.path.abspath(casepath)
    outputpath = os.path.join(casepath, "_output")

    # check file
    if os.path.isfile(outputfile):
        logger.warning("Fig %s already exists. Skip", outputfile)
        logger.handlers[0].flush()
        return

    # a new figure
    fig = pyplot.figure(num=0, figsize=(8, 5), dpi=100)

    # create an axes at 1, 3, 1
    main_ax = fig.add_axes([0.1, 0.38, 0.8, 0.52])

    # solution
    soln = pyclaw.Solution()
    soln.read(frameno, outputpath, file_format="binary", read_aux=True)

    # plot topo first
    for lvl in range(1, max_level+1):
        for state in soln.states:
            if state.patch.level != lvl:
                continue
            main_ax.imshow(
                state.aux[0, :, :].T, origin="lower",
                extent=[state.patch.lower_global[0], state.patch.upper_global[0],
                        state.patch.lower_global[1], state.patch.upper_global[1]],
                vmin=9, vmax=30, cmap=pyplot.get_cmap("terrain"))

    for state in soln.states:
        if state.patch.level != max_level:
            continue
        main_ax.imshow(
            numpy.ma.masked_less(state.q[0, :, :].T, 1e-4),
            origin="lower",
            extent=[state.patch.lower_global[0], state.patch.upper_global[0],
                    state.patch.lower_global[1], state.patch.upper_global[1]],
            vmin=0, vmax=0.2, cmap=pyplot.get_cmap("viridis"))

    main_ax.set_xlim(0, 152)
    main_ax.set_ylim(0, 60)
    main_ax.set_xlabel(r"$x\ (m)$")
    main_ax.set_ylabel(r"$y\ (m)$")

    # plot colorbar in a new axes for topography
    cbar_ax1 = fig.add_axes([0.16, 0.24, 0.68, 0.025])
    cbar1 = matplotlib.colorbar.ColorbarBase(
        cbar_ax1, cmap=pyplot.get_cmap("terrain"), orientation="horization",
        norm=matplotlib.colors.Normalize(vmin=9, vmax=30),
        ticklocation="bottom")
    cbar1.set_label("Elevation (m)")

    # plot colorbar in a new axes for depth
    cbar_ax2 = fig.add_axes([0.16, 0.1, 0.68, 0.025])
    cbar2 = matplotlib.colorbar.ColorbarBase(
        cbar_ax2, cmap=pyplot.get_cmap("viridis"), orientation="horization",
        norm=matplotlib.colors.Normalize(vmin=0, vmax=0.2),
        ticklocation="bottom")
    cbar2.set_label("Depth (m)")

    fig.suptitle("Topography and depth, T={}s".format(int(soln.state.t+0.5)) +
                 "\n({})".format(subtitle),
                 x=0.5, y=0.92, fontsize=12,
                 horizontalalignment="center",
                 verticalalignment="bottom")

    fig.savefig(outputfile, dpi="figure", bbox_inches="tight")
    pyplot.close(fig)

    logger.info("Done creating fig %s", outputfile)
    logger.handlers[0].flush()
    print("Done creating fig {}".format(outputfile))

def plot_case(casepath, casename, framelist, max_level, subtitle):
    """Plot frames in the framelist of a case."""

    # paths
    repo_path = os.path.dirname(os.path.abspath(__file__))
    casepath = os.path.abspath(casepath)
    figspath = os.path.join(repo_path, "figs")
    casefigpath = os.path.join(figspath, casename, "level{:02}".format(max_level))

    # check figs folder
    if not os.path.isdir(casefigpath):
        os.makedirs(casefigpath)

    for fno in framelist:
        outputfile = os.path.join(casefigpath, "depth{:04}.png".format(fno))
        plot_single_frame(casepath, fno, max_level, subtitle, outputfile)

if __name__ == "__main__":

    # CMD argument parser
    parser = argparse.ArgumentParser(description="Plot depth of a case.")

    parser.add_argument(
        '--casepath', dest='casepath', type=str, required=True,
        help='case folder path')

    parser.add_argument(
        '--casename', dest='casename', type=str, required=True,
        help='case name for figure creation')

    parser.add_argument(
        '--framelist', dest='framelist', type=int, required=True, nargs="*",
        help='case name for figure creation')

    parser.add_argument(
        '--level', metavar='level', type=int, required=True,
        help='max level plotted')

    parser.add_argument(
        '--subtitle', metavar='subtitle', type=str, required=True,
        help='subtitle in the plot')

    args = parser.parse_args()

    # paths
    repo_path = os.path.dirname(os.path.abspath(__file__))
    claw_path = os.path.join(repo_path, "src", "clawpack-v5.5.0")

    # add environment variables
    os.environ["CLAW"] = claw_path

    # add clawpack python package search path
    if claw_path != sys.path[0]:
        sys.path.insert(0, claw_path)

    plot_case(args.casepath, args.casename, args.framelist, args.level, args.subtitle)
