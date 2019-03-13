#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Distributed under terms of the MIT license.

"""
Download Clawpack v5.5.0 and decompress it.
"""
import os
import logging


# logger
logger = logging.getLogger("setup.py")
logger.setLevel(logging.DEBUG)

# log message to std io
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# file log
fh = logging.FileHandler("neck_test_setup.log", "w", "utf-8")
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter(
    '[%(asctime)s][%(name)s][%(levelname)s] %(message)s'))

# add handlers to the logger
logger.addHandler(ch)
logger.addHandler(fh)

def download_clawpack():
    """Download Clawpack v5.5.0 tarballs."""
    import requests

    repo_path = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(repo_path, "src")
    tar_path = os.path.join(src_path, "clawpack-v5.5.0.tar.gz")

    if os.path.isfile(tar_path):
        logger.warning("%s already exists. Skip downloading.", tar_path)
        return

    # download clawpack v5.5.0 tarball
    logger.debug("Downloading %s", tar_path)
    response = requests.get(
        "https://github.com/clawpack/clawpack/files/2330639/clawpack-v5.5.0.tar.gz",
        headers={"Accept": "application/vnd.github.v3+json"})
    response.raise_for_status()

    # write the clawpack tarball to local drive
    logger.debug("Saving the tarball to %s", tar_path)
    with open(tar_path, "wb") as f:
        f.write(response.content)

    logger.info("Downloading %s succeeded.", tar_path)

def decompress_clawpack():
    """Decompress Clawpack v5.5.0 tarballs."""
    import tarfile

    repo_path = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(repo_path, "src")
    tar_path = os.path.join(src_path, "clawpack-v5.5.0.tar.gz")
    claw_path = os.path.join(src_path, "clawpack-v5.5.0")

    if not os.path.isfile(tar_path):
        logger.error("%s does not exists! Can't decompress it", tar_path)
        raise FileNotFoundError("{} does not exists! Can't decompress it.".format(tar_path))

    if os.path.isdir(claw_path):
        logger.warning("%s already exists. Skip decompressing.", claw_path)
        return

    # extract to dst/top_level
    logger.debug("Decompressing %s to %s", tar_path, claw_path)
    with tarfile.open(tar_path, "r") as f:
        f.extractall(src_path)

    logger.info("Decompressing %s succeeded.", tar_path)

def setup_clawpack():
    """Run the setup.py in Clawpack-v5.5.0."""
    import subprocess

    repo_path = os.path.dirname(os.path.abspath(__file__))
    claw_path = os.path.join(repo_path, "src", "clawpack-v5.5.0")

    # save CWD, go to clawpack dir
    cwd = os.path.abspath(os.getcwd())
    logger.debug("Changing directory from %s to %s.", cwd, claw_path)
    os.chdir(claw_path)

    # execute `python setup.py symlink-only`
    logger.debug("Running python setup.py symlink-only")
    job = subprocess.run(
        ["python", "setup.py", "symlink-only"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        job.check_returncode()
    except subprocess.CalledProcessError:
        logger.error(job.stderr.decode("UTF-8"))
        logger.error("Setting up Clawpack v5.5.0 failed. Exit setup.")
        raise

    # go back to previous cwd
    logger.debug("Changing directory from %s to %s.", claw_path, cwd)
    os.chdir(cwd)

    logger.info("Setting up Clawpack-v5.5.0 succeeded.")

def build_executables():
    """Compile and build executables."""
    import subprocess

    repo_path = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(repo_path, "src")

    makefiles = [
        os.path.join(src_path, "Makefile.original"),
        os.path.join(src_path, "Makefile.update"),
        os.path.join(src_path, "Makefile.flag2refine2"),
        os.path.join(src_path, "Makefile.update_and_flag2refine2")]

    os.environ["CLAW"] = os.path.join(src_path, "clawpack-v5.5.0")

    if not os.path.isdir(os.path.join(repo_path, "bin")):
        os.makedirs(os.path.isdir(os.path.join(repo_path, "bin")))

    for makefile in makefiles:
        logger.debug("Running make .exe for %s.", makefile)
        job = subprocess.run(
            ["make", "-f", makefile, ".exe"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            job.check_returncode()
        except subprocess.CalledProcessError:
            logger.error(job.stderr.decode("UTF-8"))
            logger.error("Building target in %s failed. Exit.", makefile)
            raise

    logger.info("Building executables succeeded.")

def create_topo():
    """Create topo.asc for the tests."""
    import numpy
    import rasterio

    X, Y = numpy.meshgrid(
        numpy.linspace(-0.5, 200.5, 202),
        numpy.linspace(-0.5, 100.5, 102))

    logger.debug("Setting up elevation values")

    # init
    elevation = numpy.zeros((102, 202), dtype=numpy.float64)

    # inclined entrance
    elevation[X <= 80.] = (80. - X[X <= 80.]) * numpy.tan(numpy.pi/36.)

    # mountains and channels
    idx_base = (X <= 90.)
    idx_low = numpy.logical_and(idx_base, (X-90.)**2+Y**2 <= 48.5**2)
    idx_high = numpy.logical_and(idx_base, (X-90.)**2+(Y-100.)**2 <= 48.5**2)
    elevation[idx_low] = numpy.sqrt(48.5**2-(X[idx_low]-90.)**2-Y[idx_low]**2)
    elevation[idx_high] = numpy.sqrt(48.5**2-(X[idx_high]-90.)**2-(Y[idx_high]-100.)**2)

    idx_base = numpy.logical_and(X > 90., X <= 110)
    idx_low = numpy.logical_and(idx_base, Y <= 48.5)
    idx_high = numpy.logical_and(idx_base, Y >= 51.5)
    elevation[idx_low] = numpy.sqrt(48.5**2-Y[idx_low]**2)
    elevation[idx_high] = numpy.sqrt(48.5**2-(Y[idx_high]-100.)**2)

    idx_base = (X >= 110.)
    idx_low = numpy.logical_and(idx_base, (X-110.)**2+Y**2 <= 48.5**2)
    idx_high = numpy.logical_and(idx_base, (X-110.)**2+(Y-100.)**2 <= 48.5**2)
    elevation[idx_low] = numpy.sqrt(48.5**2-(X[idx_low]-110.)**2-Y[idx_low]**2)
    elevation[idx_high] = numpy.sqrt(48.5**2-(X[idx_high]-110.)**2-(Y[idx_high]-100.)**2)

    # pool
    idx_low = numpy.logical_and(X >= 145., X <= 165.)
    idx_high = numpy.logical_and(Y >= 34.5, Y <= 65.5)
    idx_base = numpy.logical_and(idx_low, idx_high)
    elevation[idx_base] = -1.0

    # clip high elevation values, because we don't need them
    elevation[elevation > 20.] = 20.

    # lift the elevation to above sea level
    elevation += 10.0

    profile = rasterio.profiles.Profile({
        "driver": "AAIGrid", "width": 202, "height": 102, "count": 1,
        "crs": rasterio.crs.CRS.from_epsg(3857),
        "transform": rasterio.transform.from_origin(-1., 101., 1., 1.),
        "dtype": elevation.dtype, "nodata": -9999})

    repo_path = os.path.dirname(os.path.abspath(__file__))
    topodir_path = os.path.join(repo_path, "topodata")
    if not os.path.isdir(topodir_path):
        os.makedirs(topodir_path)

    logger.debug("Writing to topodata/topo.asc")
    with rasterio.open(os.path.join(topodir_path, "topo.asc"), mode="w", **profile) as raster:
        raster.write_band(1, elevation)

    logger.info("Creating topo file succeeded.")

if __name__ == "__main__":
    download_clawpack()
    decompress_clawpack()
    setup_clawpack()
    build_executables()
    create_topo()
