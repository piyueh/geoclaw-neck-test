geoclaw-neck-test
=================

This repository includes all necessary components for reproducing neck-test with
GeoClaw v5.5.0. The neck-test is a set of tests to show that the possible 
non-conservative behavior of GeoClaw when the base topography has a neck-like 
(or channel-like) feature.

-----------------------------
## Steps to reproduce results

To reporduce the results, follow these commands (on Linux):

```
$ python setup.py
$ python run.py
$ python totalvolume.py
$ python create_plots.py
```

The followings are the dependencies required. The versions of these dependencies 
are the ones I used. It doesn't mean other versions do not work. It's just saying 
I don't know what will happen if other versions are used.

1. gfortran 8
2. python 3.6.8
3. numpy 1.15.4
4. matplotlib 3.0.2

My test environment is Arch Linux with kernel 5.0.0-arch1-1-ARCH.

----------
## Results

### Using a single-level mesh for a simulation

#### dx = 4

![dx=4 animation]("figs/single-mesh-tests/dx=4/level01/animation.gif")

#### dx = 2

![dx=2 animation]("figs/single-mesh-tests/dx=2/level01/animation.gif")

#### dx = 1

![dx=1 animation]("figs/single-mesh-tests/dx=1/level01/animation.gif")

#### dx = 0.5

![dx=0.5 animation]("figs/single-mesh-tests/dx=0.5/level01/animation.gif")

#### dx = 0.25

![dx=0.25 animation]("figs/single-mesh-tests/dx=0.25/level01/animation.gif")

#### dx = 0.125

![dx=0.125 animation]("figs/single-mesh-tests/dx=0.125/level01/animation.gif")

#### Conservation of fluid volumes

![volume vs time]("figs/volume_single_uniform_mesh.png")

----------
## Contact

Pi-Yueh Chuang pychuang@gwu.edu
