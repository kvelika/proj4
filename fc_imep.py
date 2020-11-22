# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 23:12:52 2020

@author: MG
"""

def imep (cyl_p, dVth, Vd): #define function

# indent obligatory
    
    import numpy as np
    PdV=cyl_p*dVth #aprekina spiediena un tilpumu izmainu reizinajumu
    PdV_gross=cyl_p[1799:5399]*dVth[1799:5399] # tikai saspiedes un izpletes procesaa

    IMEP=np.trapz(PdV)/Vd #skaitliski integree
    IMEP_gross=np.trapz(PdV_gross/Vd);
    
    

    
    return (IMEP, IMEP_gross) #returns results