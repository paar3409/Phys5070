# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 14:13:47 2022

@author: paar3409

This document tracks the changes that I did to the ipynb. Should make it workable for version control while
I can keep testing with the notebook
"""

import numpy as np
import qutip as qt
import matplotlib.pyplot as plt

##########################################
# Set up the constants
##########################################
E_C = .280 #GHz
E_J = 50*E_C
omega_r = 2*np.pi*7.500 #GHz
g = .250 #GHz
kappa = 0.020 #GHz
omega_d = omega_r

N1 = 6
N2 = 15

assert N1 != 1
assert N2 != 1
##########################################
# Setup the Hamiltonian
##########################################

def hamiltonian(t, drive_amp):
    """
    Return the transmon hamiltonian as a Qobj instance.
    drive_amp is the drive amplitude.
    t is time.
    """
    cos = np.diag(np.ones(N1-1), 1) + np.diag(np.ones(N1-1), -1)
    nt = qt.num(N1)**2 
    transmon = 4 * E_C * ( nt )**2 - 0.5 * E_J * (cos)
                 
    resonator = omega_r*qt.create(N2)*qt.destroy(N2) - 1.j*drive_amp*(qt.destroy(N2)-qt.create(N2))*np.sin(omega_d*t)
    
    interaction = -1.j*g*qt.tensor(qt.num(N1), (qt.destroy(N2)-qt.create(N2)))
    
    Hamilton = qt.tensor(transmon, qt.qeye(N2)) + interaction + qt.tensor(qt.qeye(N1), resonator)
    return Hamilton

##########################################
# Setup the operators, initial states, and variables
##########################################

decay = qt.tensor(qt.qeye(N1), qt.destroy(N2))
nq = qt.tensor(qt.num(N1), qt.qeye(N2))