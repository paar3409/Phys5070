# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 19:45:14 2022

@author: paar3409

This python script is a test of the solution to the Transmon Hamiltonian. The
test is done against results from scqubits, which are known to be correct.
"""
import numpy as np
import scqubits
#import matplotlib.pyplot as plt
import qutip as qt
#import testing stuff
import numpy.testing as npt

#Frist up set up the qubit parameters:

E_C = 280
E_J = 50*E_C
ng_list = np.linspace(-1, 1, 250)
N=100

transmon = scqubits.Transmon(EJ=E_J,
                              EC=E_C,
                              ng=.5,
                              ncut=N)
eigenvals = transmon.get_spectrum_vs_paramvals('ng', ng_list, evals_count=N)
#eigenvals.energy_table now contains the eigenvalues calculated from scqubits

def hamiltonian(Ec, Ej, N, ng):
    """
    Return the transmon hamiltonian as a Qobj instance.
    N is the order that we are using.
    Ec is the charging energy.
    Ej is the Josephson energy.
    ng is the charge of the qubit
    """
    m = np.diag(4 * Ec * (np.arange(-N,N+1)-ng)**2) + 0.5 * Ej * (np.diag(-np.ones(2*N), 1) + 
                                                               np.diag(-np.ones(2*N), -1))
    return qt.Qobj(m)

energies = np.array([hamiltonian(E_C, E_J, N, ng).eigenenergies(eigvals=N) for ng in ng_list])


diffsum = np.sum(np.abs(eigenvals.energy_table-energies))
npt.assert_allclose(diffsum, 0, atol=1e-9)
#This means that the error in less than 1Hz over the total sampled spectrum, which is 25,000 samples
print('Our transmon hamiltonian is within our desired tolerance! ' +
      'That is less than 1 Hz difference over 25,000 spots')