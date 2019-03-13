#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Distributed under terms of the MIT license.

"""
Calculate total volume and plot them.
"""
import os
import sys
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

def get_volumes_single_frame(maxlvl, solution):
    """
    Get volumes from the solution of a single time frame.
    """
    import numpy

    volumes = numpy.zeros(maxlvl, dtype=numpy.float64)
    for state in solution.states:
        p = state.patch
        level = p.level
        volumes[level-1] += (numpy.sum(state.q[0, :, :]) * p.delta[0] * p.delta[1])

    return volumes

def create_volume_datafile(casepath):
    """Create a volume.csv for a case."""
    import numpy

    casepath = os.path.abspath(casepath)
    out_path = os.path.join(casepath, "_output")
    repo_path = os.path.dirname(os.path.abspath(__file__))
    claw_path = os.path.join(repo_path, "src", "clawpack-v5.5.0")

    logger.info("Creating total volume datafile for case %s", casepath)
    if os.path.isfile(os.path.join(casepath, "volume.csv")):
        logger.warning("%s exists. Skip.", os.path.join(casepath, "volume.csv"))
        logger.handlers[0].flush()
        logger.handlers[1].flush()
        return

    # add environment variables
    os.environ["CLAW"] = claw_path

    # add clawpack python package search path
    if claw_path != sys.path[0]:
        sys.path.insert(0, claw_path)

    # import utilities
    from clawpack import pyclaw

    # get # of frames from setrun.py
    if casepath != sys.path[0]:
        sys.path.insert(0, casepath)
    import setrun # import the setrun.py
    rundata = setrun.setrun() # get ClawRunData object
    nframes = rundata.clawdata.num_output_times + 1
    nlevels = rundata.amrdata.amr_levels_max
    del rundata
    del sys.modules["setrun"]
    del sys.path[0]

    data = numpy.zeros((nframes, 1+nlevels), dtype=numpy.float64)
    for fno in range(0, nframes):
        # empty solution object
        soln = pyclaw.Solution()

        # read
        soln.read(fno, out_path, file_format="binary", read_aux=False)

        # calculate total volume at each grid level
        data[fno, 0] = soln.state.t
        data[fno, 1:] = get_volumes_single_frame(nlevels, soln)

    numpy.savetxt(os.path.join(casepath, "volume.csv"), data, delimiter=",")
    logger.info("Done creating total volume datafile.")
    logger.handlers[0].flush()
    logger.handlers[1].flush()

def create_all_volume_datafiles():
    """Create volume.csv in all cases."""

    repo_path = os.path.dirname(os.path.abspath(__file__))

    cases = [
        "amr-tests/fix_update", "amr-tests/fix_flag2refine2",
        "amr-tests/fix_update_and_flag2refine2", "amr-tests/original",
        "single-mesh-tests/dx=4", "single-mesh-tests/dx=2",
        "single-mesh-tests/dx=1", "single-mesh-tests/dx=0.5",
        "single-mesh-tests/dx=0.25", "single-mesh-tests/dx=0.125"]

    for case in cases:
        case = os.path.join(repo_path, case)
        create_volume_datafile(case)

if __name__ == "__main__":
    create_all_volume_datafiles()
