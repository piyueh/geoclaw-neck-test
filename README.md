geoclaw-neck-test
=================

This repository includes all necessary components for reproducing neck-test with
GeoClaw v5.5.0. The neck-test is a set of tests to show that the possible 
non-conservative behavior of GeoClaw when the base topography has a neck-like 
(or channel-like) feature.

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

## Contact

Pi-Yueh Chuang pychuang@gwu.edu
