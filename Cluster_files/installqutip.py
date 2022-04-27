# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 12:40:59 2021

@author: paar3409
"""

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
install("qutip")