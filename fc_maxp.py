# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 23:12:52 2020

@author: MG
"""

def maxp (cyl_p, cad): #deifine function

# indent obligatory
    
    import numpy as np
    index_MaxP=np.argmax(cyl_p) #find index of Maxximal pressure 
    PMax=cyl_p[index_MaxP]  # Find maximal pressure value
    PMax_cad=cad[index_MaxP]-360  # find maximal pressure angle
    
    return (PMax, PMax_cad) #returns results