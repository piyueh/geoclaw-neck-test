#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Distributed under terms of the MIT license.

"""
Create topography file.
"""
import os
import numpy
import rasterio

def create_topo(folder):
    """Create topo.asc for the tests."""

    xbg = ybg = -1.0
    xed = 201.0
    yed = 101.0
    Nx = 202
    Ny = 102
    dx = dy = 1.0

    x = numpy.linspace(xbg+dx/2, xed-dx/2, Nx)
    y = numpy.linspace(ybg+dy/2, yed-dy/2, Ny)
    X, Y = numpy.meshgrid(x, y)

    # init
    elevation = numpy.zeros((Ny, Nx), dtype=numpy.float64)

    # incline
    elevation[:, x <= 80.] = (80. - X[:, x <= 80.]) * numpy.tan(numpy.pi/36.)

    # mountains and channels
    for j, yj in enumerate(y):
        for i, xi in enumerate(x):
            if xi <= 90.:
                if ((xi - 90.)**2 + (yj - 0.)**2) <= 48.5**2:
                    elevation[j, i] = numpy.sqrt(48.5**2-(xi-90.)**2-yj**2)
                elif ((xi - 90.)**2 + (yj - 100.)**2) <= 48.5**2:
                    elevation[j, i] = numpy.sqrt(48.5**2-(xi-90.)**2-(yj-100.)**2)
            elif 90 < xi <= 110.:
                if yj <= 49.:
                    elevation[j, i] = numpy.sqrt(48.5**2 - yj**2)
                elif yj >= 51:
                    elevation[j, i] = numpy.sqrt(48.5**2 - (yj-100.)**2)
            else:
                if ((xi - 110.)**2 + (yj - 0.)**2) <= 48.5**2:
                    elevation[j, i] = numpy.sqrt(48.5**2-(xi-110.)**2-yj**2)
                elif ((xi - 110.)**2 + (yj - 100.)**2) <= 48.5**2:
                    elevation[j, i] = numpy.sqrt(48.5**2-(xi-110.)**2-(yj-100.)**2)

    # pool
    temp, = numpy.where(numpy.logical_and(x>=145, x<=165))
    colbg = temp[0]
    coled = temp[-1] + 1

    temp, = numpy.where(numpy.logical_and(y>=34.5, y<=65.5))
    rowbg = temp[0]
    rowed = temp[-1] + 1

    elevation[rowbg:rowed, colbg:coled] = -1.0

    # lift the elevation to above sea level
    elevation = elevation + 10.0

    profile = rasterio.profiles.Profile()
    profile["driver"] = "AAIGrid"
    profile["width"] = Nx
    profile["height"] = Ny
    profile["count"] = 1
    profile["crs"] = rasterio.crs.CRS.from_epsg(3857)
    profile["transform"] = rasterio.transform.from_origin(xbg, yed, dx, dy)
    profile["dtype"] = elevation.dtype
    profile["nodata"] = -9999

    with rasterio.open(os.path.join(folder, "topo.asc"), mode="w", **profile) as raster:
        raster.write_band(1, elevation)

if __name__ == "__main__":
    create_topo("./")
