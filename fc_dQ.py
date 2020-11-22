# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 19:15:56 2020

@author: MG
"""

def dQ (cyl_p, CR, SOI_btdc): #define function
    import numpy as np
    P_cyl_Pa=cyl_p*10**5 #convert bar to Pa

   

    from fc_volume import volume #calculate volume
    Vd, Vc, Vth, dVth, cad =volume (CR)

    SOI=360-SOI_btdc #start of injection
    SOC=340 #start of calculation, degrees
    FOC = 440 # end of calculation, degrees

    g=1.3 #Fixed Gamma

    CAD_R=np.size(cad)
    
     
    for ii in range(0,CAD_R):
        if cad[ii]>=SOC:
            SOCi = ii #index for start of calculation
            break
 
    for ii in range(0,CAD_R):
        if cad[ii]>=FOC:
            FOCi = ii #index for end of calculation
            break    

    # Calculation of pressure differential, central difference +- 5 steps

    dP = np.zeros(((FOCi-SOCi))) #initialize array


    i=0
    for ii in range (SOCi, FOCi):

        dPii = (P_cyl_Pa[ii+5]-P_cyl_Pa[ii-5])/((cad[ii+5]-cad[ii-5]))
        dP=np.insert(dP, i,[dPii], axis=0) #insert new value in array
        dP=np.delete(dP, (FOCi-SOCi), axis=0) #delete last value (zero)
        i=i+1
 

    # create short arrays
    cad_s=cad[SOCi:FOCi]
    P_cyl_Pa_s=P_cyl_Pa[SOCi:FOCi]
    dVth_s=dVth[SOCi:FOCi]
    Vth_s=Vth[SOCi:FOCi]


    dCAD=0.1 
  
    # Heat Release Rate

    dQ=((g/(g-1))*P_cyl_Pa_s*(dVth_s/dCAD)+(1/(g-1))*Vth_s*(dP))

    # Heat Release

    Q=np.cumsum (dQ)*dCAD # in Joules
    Q100=np.max(Q) # maximal value
    Qr=Q/Q100*100 # relative Heat release, %
    IGN_Delay_s=0

    #Size of short array
    Size_s=np.size(cad_s)

   
    #Finding SOI element in short array
    for ii in range (0, Size_s):
        if np.round(cad_s[ii]*10)>=SOI*10:
            SOIs = ii
            break
    #Finding Ignintion Delay element
    for ii in range (0,Size_s):
        if np.round(dQ[ii]*10)>=2: # lielaks par 0.2 (jo dQ*10)
           IGN_Delay_s=ii
           break
    #Finding Heat Release 10% element
    for ii in range (0,Size_s): 
        if np.round(Qr[ii]*10)>=100: 
            HR10s=ii
            break
    #Finding Heat Release 50% element
    for ii in range (0,Size_s):
        if np.round(Qr[ii]*10)>=500: 
            HR50s=ii
            break
    #Finding Heat Release 90% element
    for ii in range (0,Size_s):
        if np.round(Qr[ii]*10)>=900: 
            HR90s=ii
            break
    #IGN_Delay= np.round(cad_s[IGN_Delay_s]-cad_s[0],3)
    IGN_Delay= np.round(cad_s[IGN_Delay_s]-cad_s[SOIs],3)

    HR10cad=np.round(cad_s [HR10s]-360,3)
    HR50cad=np.round(cad_s [HR50s]-360,3)
    HR90cad=np.round(cad_s [HR90s]-360,3)
    SOIcad=np.round(cad_s [SOIs] -360,3)


    HR10=np.round(HR10cad-SOIcad,3)
    HR1050=np.round(HR50cad-HR10cad,3)
    HR1090=np.round(HR90cad-HR10cad,3)

    return (dQ, Q, Qr, IGN_Delay, HR10, HR1050, HR1090, HR50cad, cad_s)
        