# Phys5070
Final project repository to reproduce results from https://arxiv.org/pdf/2203.11235.pdf

Goal is to recreate the figures of merit from the paper utilizing a much smaller computational power. This should give some insight into the relevant system dynamics. The figures of merit that this code reproduces are ...

The core of this work is in the Jupyter notebook. There will be a final version of the code that is designed for cluster usage. The cluster script is designed to run as many levels as possible and produce as close an image as possible to the final paper figures.

This simulation is particularly hard because the dimensions quickly increase out of control. Managing the simulation time is the main challenge, although that might not be totally feasible on a simple code that aims to reproduce results from others.
Another simulation challenge is incorporating the semiclassical physics present when we have high readout occupations. For this project I did not incorporate them as they are mostly relevant at points where we can no longer simulate (large Hilbert spaces, whcih are computationally expensive).

I have written a summary of the results in the Word document present. It includes computed figures and explanations of their features. The purpose of this is to explain the structure of the project and the results from the cluster computation, which is code that would take hours to run.