# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 19:45:14 2022

@author: paar3409

This python script is a test of the solution to the Transmon Hamiltonian. The
test is done against results from scqubits, which are known to be correct.
"""
import numpy as np
import scqubits
import matplotlib.pyplot as plt
#import testing stuff


#Frist up set up the qubit parameters:

EC = 280
EJ = 50*EC
ng_list = np.linspace(-1, 1, 220)

transmon = scqubits.Transmon(EJ=30.02,
                              EC=1.2,
                              ng=.5,
                              ncut=31)
eigenvals = transmon.get_spectrum_vs_paramvals('ng', ng_list, evals_count=5)
#eigenvals.energy_table now contains the eigenvalues calculated from scqubits
transmon.plot_evals_vs_paramvals('ng', ng_list, evals_count=5, subtract_ground=False)