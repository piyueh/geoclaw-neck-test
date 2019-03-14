#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Distributed under terms of the MIT license.

"""
Create all plots required in Jupyter notebook.
"""
import os
import logging


# logger
logger = logging.getLogger("totalvolume.py")
logger.setLevel(logging.DEBUG)

# log message to std io
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# file log
fh = logging.FileHandler("neck_test_totalvolume.log", "w", "utf-8")
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter(
    '[%(asctime)s][%(name)s][%(levelname)s] %(message)s'))

# add handlers to the logger
logger.addHandler(ch)
logger.addHandler(fh)

def plot_single_volume(cases, subtitle, savepath):
    """Plot a single figure for volume vs time plot."""
    import numpy
    from matplotlib import pyplot

    repo_path = os.path.dirname(os.path.abspath(__file__))

    pyplot.figure(figsize=(6, 6), dpi=100)

    for label, [case, idx, style] in cases.items():
        case = os.path.join(repo_path, case)
        datafile = os.path.join(case, "volume.csv")
        if not os.path.isfile(datafile):
            logger.error("Couldn't find %s. Exit now", datafile)
            raise FileNotFoundError("Couldn't find {}. Exit now".format(datafile))

        data = numpy.loadtxt(os.path.join(case, "volume.csv"), delimiter=",")
        pyplot.plot(data[:, 0], data[:, idx], label=label, **style)

    pyplot.title("Volume v.s. time, {}".format(subtitle))
    pyplot.xlabel(r"$Time\ (sec)$")
    pyplot.ylabel(r"$Volume\ (m^3)$")
    pyplot.ylim(0, 20)
    pyplot.legend(
        loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2, fontsize=10,
        handlelength=3, columnspacing=1)
    pyplot.grid()

    pyplot.savefig(savepath, dpi=100, bbox_inches="tight")

    logger.info("Done creating figure %s", savepath)
    logger.handlers[0].flush()
    logger.handlers[1].flush()

def plot_volumes():
    """Plot volumes."""

    repo_path = os.path.dirname(os.path.abspath(__file__))
    figs_path = os.path.join(repo_path, "figs")

    ls_dict = {
        'solid': (0, ()),
        'loosely dotted': (0, (1, 10)),
        'dotted': (0, (1, 5)),
        'densely dotted': (0, (1, 1)),
        'loosely dashed': (0, (5, 10)),
        'dashed': (0, (5, 5)),
        'densely dashed': (0, (5, 1)),
        'loosely dashdotted': (0, (3, 10, 1, 10)),
        'dashdotted': (0, (3, 5, 1, 5)),
        'densely dashdotted': (0, (3, 1, 1, 1)),
        'loosely dashdotdotted': (0, (3, 10, 1, 10, 1, 10)),
        'dashdotdotted': (0, (3, 5, 1, 5, 1, 5)),
        'densely dashdotdotted': (0, (3, 1, 1, 1, 1, 1))}

    amr_level_1 = {
        "single mesh, dx = 4": [
            "single-mesh-tests/dx=4", 1, {"ls": ls_dict["solid"], "lw": 3.2}],
        "original": [
            "amr-tests/original", 1, {"ls": ls_dict["densely dashdotted"], "lw": 2.9}],
        "update.f90": [
            "amr-tests/fix_update", 1, {"ls": ls_dict["densely dashed"], "lw": 2.6}],
        "flag2refine2.f90": [
            "amr-tests/fix_flag2refine2", 1, {"ls": ls_dict["densely dotted"], "lw": 2.3}],
        "update.f90 + flag2refine2.f90": [
            "amr-tests/fix_update_and_flag2refine2", 1, {"ls": ls_dict["densely dashdotdotted"], "lw": 2.0}]}

    amr_level_2 = {
        "single mesh, dx = 1": [
            "single-mesh-tests/dx=1", 1, {"ls": ls_dict["solid"], "lw": 3.2}],
        "original": [
            "amr-tests/original", 2, {"ls": ls_dict["densely dashdotted"], "lw": 2.9}],
        "update.f90": [
            "amr-tests/fix_update", 2, {"ls": ls_dict["densely dashed"], "lw": 2.6}],
        "flag2refine2.f90": [
            "amr-tests/fix_flag2refine2", 2, {"ls": ls_dict["densely dotted"], "lw": 2.3}],
        "update.f90 + flag2refine2.f90": [
            "amr-tests/fix_update_and_flag2refine2", 2, {"ls": ls_dict["densely dashdotdotted"], "lw": 2.0}]}

    uniform_cases = {
        "dx = 4": ["single-mesh-tests/dx=4", 1, {"ls": ls_dict["solid"], "lw": 3.0}],
        "dx = 2": ["single-mesh-tests/dx=2", 1, {"ls": ls_dict["densely dashed"], "lw": 2.8}],
        "dx = 1": ["single-mesh-tests/dx=1", 1, {"ls": ls_dict["densely dotted"], "lw": 2.6}],
        "dx = 0.5": ["single-mesh-tests/dx=0.5", 1, {"ls": ls_dict["densely dashdotted"], "lw": 2.4}],
        "dx = 0.25": ["single-mesh-tests/dx=0.25", 1, {"ls": ls_dict["densely dashdotdotted"], "lw": 2.2}],
        "dx = 0.125": ["single-mesh-tests/dx=0.125", 1, {"ls": ls_dict["dashed"], "lw": 2.0}]}

    # check and create the folder
    if not os.path.isdir(figs_path):
        os.makedirs(figs_path)

    # single uniform mesh
    figname = os.path.join(figs_path, "volume_single_uniform_mesh.png")
    plot_single_volume(uniform_cases, "single uniform mesh", figname)

    # AMR level 1
    figname = os.path.join(figs_path, "volume_AMR_level_1.png")
    plot_single_volume(amr_level_1, "AMR level 1 (dx=4)", figname)

    # AMR level 2
    figname = os.path.join(figs_path, "volume_AMR_level_2.png")
    plot_single_volume(amr_level_2, "AMR level 2 (dx=1)", figname)

def plot_flows():
    """Plot flows of all cases in parallel."""
    import time
    import subprocess

    # paths
    repo_path = os.path.dirname(os.path.abspath(__file__))
    figs_path = os.path.join(repo_path, "figs")
    cmd = os.path.join(repo_path, "plotflow_cmd.py")

    if not os.path.isdir(figs_path):
        os.makedirs(figs_path)

    # AMR cases
    amr_cases_lvl1 = {
        "AMR/original/level 1": ["amr-tests/original", 1],
        "AMR/new update.f90/level 1": ["amr-tests/fix_update", 1],
        "AMR/new flag2refine2.f90/level 1": ["amr-tests/fix_flag2refine2", 1],
        "AMR/new update.f90 & flag2refine2.f90/level 1": [
            "amr-tests/fix_update_and_flag2refine2", 1]}

    amr_cases_lvl2 = {
        "AMR/original/level 2": ["amr-tests/original", 2],
        "AMR/new update.f90/level 2": ["amr-tests/fix_update", 2],
        "AMR/new flag2refine2.f90/level 2": ["amr-tests/fix_flag2refine2", 2],
        "AMR/new update.f90 & flag2refine2.f90/level 2": [
            "amr-tests/fix_update_and_flag2refine2", 2]}

    uniform_cases = {
        "unifrom mesh/dx = 4": ["single-mesh-tests/dx=4", 1],
        "unifrom mesh/dx = 2": ["single-mesh-tests/dx=2", 1],
        "unifrom mesh/dx = 1": ["single-mesh-tests/dx=1", 1],
        "unifrom mesh/dx = 0.5": ["single-mesh-tests/dx=0.5", 1],
        "unifrom mesh/dx = 0.25": ["single-mesh-tests/dx=0.25", 1],
        "unifrom mesh/dx = 0.125": ["single-mesh-tests/dx=0.125", 1]}

    try:
        nprocs = int(os.environ["OMP_NUM_THREADS"])
    except KeyError:
        nprocs = int(os.cpu_count()/2)

    for caseset in [amr_cases_lvl1, amr_cases_lvl2, uniform_cases]:
        for casename, [casepath, level] in caseset.items():
            logger.info("Creating figures for %s with %d CPU threads.", casename, nprocs)
            jobs = []
            stdfiles = []
            for i in range(nprocs):

                target = os.path.join(figs_path, casepath, "level{:02}".format(level))
                if not os.path.isdir(target):
                    os.makedirs(target)
                stdfiles.append(open(os.path.join(
                    target, "stdout.{:02}.txt".format(i)), "w"))
                framelist = list(range(i, 361, nprocs))

                jobs.append(subprocess.Popen(
                    ["python", cmd, "--casename", casepath,
                     "--casepath", casepath, "--level", str(level),
                     "--subtitle", casename, "--framelist"] +
                    str(framelist).strip("[]").replace(",", "").split(),
                    cwd=repo_path, stdout=stdfiles[-1], stderr=stdfiles[-1]))

                logger.info("Thread %d, STDOUT/STDERR file: %s", i, stdfiles[-1].name)

            while any([job.poll() is None for job in jobs]):
                time.sleep(5)

            for i in range(nprocs):
                stdfiles[i].close()

            logger.info("Done creating figures for %s.", casename)

if __name__ == "__main__":
    plot_volumes()
    plot_flows()
