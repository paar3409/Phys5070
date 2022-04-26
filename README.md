# Phys5070
Final project repository to reproduce results from https://arxiv.org/pdf/2203.11235.pdf

Goal is to recreate the figures of merit from the paper utilizing a much smaller computational power. This should give some insight into the relevant system dynamics. The figures of merit that this code reproduces are ...

The core of this work is in the Jupyter notebook. There will be a final version of the code that is designed for cluster usage. The cluster script is designed to run as many levels as possible and produce as close an image as possible to the final paper figures.

This simulation is particularly hard because the dimensions quickly increase out of control. Managing the simulation time is the main challenge, although that might not be totally feasible on a simple code that aims to reproduce results from others.