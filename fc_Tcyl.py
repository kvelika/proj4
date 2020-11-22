# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 19:15:56 2020

@author: MG
"""

def Tcyl (cyl_p, CR, Speed): #define function
    import numpy as np
    P_cyl_Pa=cyl_p*10**5 #convert bar to Pa


    from fc_volume import volume #calculate volume
    Vd, Vc, Vth, dVth, cad =volume (CR)


    T1=65+273.15 #initial temperature, K
    P1=np.mean(P_cyl_Pa [2100:2120]) #Pressure at the beginning of compression
    
    SOC=240 #start of calculation, degrees
    FOC = 510 # end of calculation, degrees


    CAD_R=np.size(cad)
    
     
    for ii in range(0,CAD_R):
        if cad[ii]>=SOC:
                SOCi = ii #index for start of calculation
                break
 
    for ii in range(0,CAD_R):
        if cad[ii]>=FOC:
                FOCi = ii #index for end of calculation
                break    
       
    cad_st=cad[SOCi:FOCi]
    P_cyl_Pa_s=P_cyl_Pa[SOCi:FOCi]
    Vth_s=Vth[SOCi:FOCi]

    Ri=287 # specific gas constant, air, J/kg K
    
    ro1=P1/(Ri*T1) # air density at the beginning of compression, kg/m3
    
    m_air=ro1*(Vc+Vd) #mass of air in cylinder, kg
    
    #fuel supply 13 ml/min
    
    m_fuel=(13*0.84/1000)/(Speed/2) #kg
    m_air_fuel=m_air+m_fuel
    
    T=(P_cyl_Pa_s*Vth_s)/(m_air_fuel*Ri) #temperature changes in K

    return (T, cad_st)
