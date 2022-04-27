# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 14:13:47 2022

@author: paar3409

This script is intended to be plugged in to a computer cluster. Parameters are
at the top and allows one to change a parameter and run the script again.
Since it is for a cluster I made the design choice of keeping it a script and
not making it a class, this is purely since I can keep track of things by filename
and because it is files what you input to the cluster not as much objects.

This document also tracks the changes that I did to the ipynb. Should make it workable for version control while
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
omega_r = 7.500 #GHz
g = .250 #GHz
kappa = 2*np.pi*0.020 #GHz
omega_d = omega_r

N1 = 8
N2 = 100

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

times = np.linspace(0, 2/kappa, 1001) #0 to kappta*t=1 honestly IDK how they made their figure look like it does. RIP
drive1 = 2*np.pi*0.28

decay = qt.tensor(qt.qeye(N1), qt.destroy(N2))
nq = qt.tensor(qt.num(N1), qt.qeye(N2))
nr = qt.tensor(qt.qeye(N1), qt.num(N2))

init_g = qt.tensor(qt.basis(N1),qt.basis(N2))
init_e = qt.tensor(qt.basis(N1,2),qt.basis(N2))

args = {}
#args = {'drive_amp': drive1}
opts = qt.Options(store_states=True)
#opts = qt.Options(store_states=True, nsteps = 5000)

########################################
# Run the time solver
##########################################

def H(t, dummy):
    return hamiltonian(t, drive1)

result_init_e = qt.mesolve(H, init_e, times, [kappa*decay], [nq,nr], args = args, options = opts, progress_bar = True)
result_init_g = qt.mesolve(H, init_g, times, [kappa*decay], [nq,nr], args = args, options = opts, progress_bar = True)

states_g = []
for i in range(len(result_init_g.states)):
    lewd = []
    for j in range(N1):
        lewd.append(result_init_g.states[i].ptrace(0)[j,j])
    states_g.append(lewd)

states_e = []
for i in range(len(result_init_e.states)):
    lewd = []
    for j in range(N1):
        lewd.append(result_init_e.states[i].ptrace(0)[j,j])
    states_e.append(lewd)
##########################################
# Plot the results
##########################################

fig,ax = plt.subplots()
# make a plot
#ax.plot(times, result_init_g.expect[0], color = 'black')
ax.plot(np.linspace(0,len(times)-1, len(times)), result_init_g.expect[0], color = 'black', linewidth =4)

ax.set_ylim([-0.5, N1-0.5])
ax.imshow(np.log10(np.abs(states_g)).T,origin="lower", aspect='auto', interpolation='none',cmap='Blues')
#ax.colorbar()
ax.set_xlabel("time",fontsize=14)
ax.set_ylabel("Nt",color="black",fontsize=14)
# twin object for two different y-axis on the sample plot
ax2=ax.twinx()
ax2.plot(np.linspace(0,len(times)-1, len(times)), result_init_g.expect[1], color = 'r', linewidth =4)
ax2.set_ylabel("Nr",color="red",fontsize=14, rotation=-90)
plt.savefig('Panel1a.png')
plt.show()

plt.figure(2)
fig,ax = plt.subplots()
# make a plot
#ax.plot(times, result_init_e.expect[0], color = 'black')
ax.plot(np.linspace(0,len(times)-1, len(times)), result_init_e.expect[0], color = 'black', linewidth =4)

ax.set_ylim([-0.5, N1-0.5])
ax.imshow(np.log10(np.abs(states_e)).T,origin="lower", aspect='auto', interpolation='none',cmap='Blues')
#ax.colorbar()
ax.set_xlabel("time",fontsize=14)
ax.set_ylabel("Nt",color="black",fontsize=14)
# twin object for two different y-axis on the sample plot
ax2=ax.twinx()
ax2.plot(np.linspace(0,len(times)-1, len(times)), result_init_e.expect[1], color = 'r', linewidth =4)
ax2.set_ylabel("Nr",color="red",fontsize=14, rotation=-90)

plt.savefig('Panel1b.png')
plt.show()

##########################################
# Save the results to get them out of pythhon
##########################################

qt.qsave(result_init_g, 'ground-data')
qt.qsave(result_init_e, 'excited-data')