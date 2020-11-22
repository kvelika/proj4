# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 20:48:50 2020

@author: MG

"""
import numpy as np
import scipy.io as spio # to import matlab
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)


# Initial parameters
#Choose compression ratio according to data: 14 or 19

CR=14 # compression ratio, other option CR=19

Speed=900 # rpm

if CR==14:
    Data = spio.loadmat('Data_CR14.mat')
elif CR==19:
    Data = spio.loadmat('Data_CR19.mat')
    
P_Test1 = Data ['P_mot'] # import variable from mat file
P_Test2 = Data ['P_adv5']
P_Test3 = Data ['P_adv11']
P_Test4 = Data ['P_adv15']

P_Test1=np.squeeze(P_Test1) #removes axes with length 1
P_Test2=np.squeeze(P_Test2)
P_Test3=np.squeeze(P_Test3)
P_Test4=np.squeeze(P_Test4)




SOI_Test1=0 # start of injection, CAD BTDC
SOI_Test2=5
SOI_Test3=11
SOI_Test4=15

#labels for plots

label_Test1='Motoring'
label_Test2='SOI 5'
label_Test3='SOI 11'
label_Test4='SOI 15'

#labels for bar plot
labels_line_all = [label_Test1, label_Test2, label_Test3, label_Test4]
labels_line_fired = [label_Test2, label_Test3, label_Test4]





from fc_volume import volume #call function to calculate volume
Vd, Vc, Vth, dVth, cad =volume (CR)

#Create cylinder volume plot

fig, ax = plt.subplots()
ax.grid()
ax.set_ylabel('Volume, $cm^3$')
ax.set_xlabel('CAD \n \n Fig.1. Cylinder Volume During Engine Cycle')

maxval=np.max(Vth*10**6)
ylim=maxval+50
ax.set_xlim(-360, 360)
ax.set_ylim(0, ylim)

ax.xaxis.set_major_locator(MultipleLocator(60)) # distribute major ticks on x axis

line, = ax.plot(cad-360, Vth*10**6, label=('Volume'))

plt.show()

# Create cylinder pressure plot
fig, ax = plt.subplots()
ax.grid()
ax.set_ylabel('Pressure, bar')
ax.set_xlabel('CAD \n \n Fig.2. Pressure changes in cylinder')

maxval=np.max([np.max(P_Test1), np.max(P_Test2), np.max(P_Test3), np.max(P_Test4)])
ylim=maxval+5
ax.set_xlim(-100, 100)
ax.set_ylim(0, ylim)
ax.xaxis.set_major_locator(MultipleLocator(20)) # distribute major ticks on x axis
line, = ax.plot(cad-360, P_Test1, label=label_Test1)
line, = ax.plot(cad-360, P_Test2, label=label_Test2)
line, = ax.plot(cad-360, P_Test3, label=label_Test3)
line, = ax.plot(cad-360, P_Test4, label=label_Test4)
ax.legend()
plt.show()


# Create cylinder pressure/volume plot
fig, ax = plt.subplots()
ax.grid() #create grid
ax.set_ylabel('Pressure, bar')
ax.set_xlabel('Volume, $cm^3$ \n \n Fig.3. Pressure/ volume diagram')

maxval=np.max([np.max(P_Test1), np.max(P_Test2), np.max(P_Test3), np.max(P_Test4)])
ylim=maxval+5
ax.set_xlim(0, 750) #set axe limits
ax.set_ylim(0, ylim)
line, = ax.plot(Vth*10**6, P_Test1, label=label_Test1) #create multilple line plots
line, = ax.plot(Vth*10**6, P_Test2, label=label_Test2)
line, = ax.plot(Vth*10**6, P_Test3, label=label_Test3)
line, = ax.plot(Vth*10**6, P_Test4, label=label_Test4)
ax.legend()
plt.show()

# Create cylinder pressure/volume log plot
fig, ax = plt.subplots()
ax.grid() #create grid
ax.set_ylabel('Pressure, bar')
ax.set_xlabel('Volume, $cm^3$ \n \n Fig.4. Pressure/ volume diagram in log scale')

maxval=np.log(np.max([np.max(P_Test1), np.max(P_Test2), np.max(P_Test3), np.max(P_Test4)]))
ylim=maxval+5
#ax.set_xlim(0, 750) #set axe limits
#ax.set_ylim(0, ylim)
ax.set_xscale('log')
ax.set_yscale('log')
ax.xaxis.set_major_locator(MultipleLocator(30)) # distribute major ticks on x axis
ax.yaxis.set_major_locator(MultipleLocator(10)) # distribute major ticks on y axis
line, = ax.plot((Vth*10**6), (P_Test1), label=label_Test1) #create multilple line plots
line, = ax.plot(Vth*10**6, P_Test2, label=label_Test2)
line, = ax.plot(Vth*10**6, P_Test3, label=label_Test3)
line, = ax.plot(Vth*10**6, P_Test4, label=label_Test4)
ax.legend()
plt.show()



from fc_maxp import maxp #call function to find maximal pressure and angle
PMax_Test1, PMax_cad_Test1 =maxp (P_Test1, cad)
PMax_Test2, PMax_cad_Test2 =maxp (P_Test2, cad)
PMax_Test3, PMax_cad_Test3 =maxp (P_Test3, cad)
PMax_Test4, PMax_cad_Test4 =maxp (P_Test4, cad)

from fc_imep import imep #call function to calculate IMEP
IMEP_Test1, IMEP_gross_Test1 =imep (P_Test1, dVth, Vd)
IMEP_Test2, IMEP_gross_Test2 =imep (P_Test2, dVth, Vd)
IMEP_Test3, IMEP_gross_Test3 =imep (P_Test3, dVth, Vd)
IMEP_Test4, IMEP_gross_Test4 =imep (P_Test4, dVth, Vd)

# Create bar plot for IMEP_gross
IMEP = [IMEP_gross_Test1, IMEP_gross_Test2 ,IMEP_gross_Test3,IMEP_gross_Test4]
labels = ['Mot', 'Adv5', 'Adv11', 'Adv15']
x = np.arange(np.size(IMEP)) # creates array for bar order
fig, ax = plt.subplots()
plt.bar(x, IMEP,width=0.3,color=['C0','C1', 'C2', 'C3'])

for index, value in enumerate(x):
    plt.text(value, (IMEP[index]+0.2), str(np.round(IMEP[index],2)),horizontalalignment='center')
    
ax.set_ylabel('IMEP_{gross}, bar')
ax.set_xlabel('Test Mode \n \n Fig.5. Indicated Mean Effective  Pressure, Gross')

ylim=np.round((np.max(IMEP)+1),2)
ax.set_ylim(-1, ylim)
plt.xticks(x, labels)
plt.show()

# Create bar plot for Pmax
Pmax = [PMax_Test1, PMax_Test2 ,PMax_Test3,PMax_Test4]

x = np.arange(np.size(Pmax)) # creates array for bar order
fig, ax = plt.subplots()
plt.bar(x, Pmax,width=0.3, color=['C0','C1', 'C2', 'C3'])

for index, value in enumerate(x):
    plt.text(value, (Pmax[index]+2), str(np.round(Pmax[index],1)),horizontalalignment='center')
    
ax.set_ylabel('Pressure, bar')
ax.set_xlabel('Test Mode \n \n Fig.6. Maximal Pressure')

ylim=np.round((np.max(Pmax)+10),2)
ax.set_ylim(0, ylim)
plt.xticks(x, labels_line_all)
plt.show()

# Create bar plot for Pmax cad
Pmax_cad = [PMax_cad_Test2,PMax_cad_Test3,PMax_cad_Test4]

x = np.arange(np.size(Pmax_cad)) # creates array for bar order
fig, ax = plt.subplots()
plt.bar(x, Pmax_cad,width=0.3, color=['C1', 'C2', 'C3'])

for index, value in enumerate(x):
    plt.text(value, (Pmax_cad[index]+0.5), str(np.round(Pmax_cad[index],1)),horizontalalignment='center')
    
ax.set_ylabel('CAD, ATDC')
ax.set_xlabel('Test Mode  \n \n Fig.7. Maximal Pressure Angle')

ylim=np.round((np.max(Pmax_cad)+1),2)
ax.set_ylim(0, ylim)
plt.xticks(x, labels_line_fired)
plt.show()

#Calculation of average temperature in cylinder

from fc_Tcyl import Tcyl #call function to calculate combustion parameters

Tcyl_Test1, cad_st= Tcyl (P_Test1, CR, Speed)
Tcyl_Test2, cad_st= Tcyl (P_Test2, CR, Speed)
Tcyl_Test3, cad_st= Tcyl (P_Test3, CR, Speed)
Tcyl_Test4, cad_st= Tcyl (P_Test4, CR, Speed)

# Create average temperature in cylinder plot
fig, ax = plt.subplots()
ax.grid() #create grid
ax.set_ylabel('Temperature, K')
ax.set_xlabel('CAD   \n \n Fig.8. Average Temperature in Cylinder')

maxval=np.max([np.max(Tcyl_Test1), np.max(Tcyl_Test2), np.max(Tcyl_Test3), np.max(Tcyl_Test4)])
ylim=maxval+120
ax.set_xlim(-80, 120) #set axe limits
ax.set_ylim(300, ylim)
ax.xaxis.set_major_locator(MultipleLocator(20)) # distribute major ticks on x axis
ax.yaxis.set_major_locator(MultipleLocator(100)) # distribute major ticks on y axis
line, = ax.plot(cad_st-360, Tcyl_Test1, label=label_Test1) #create multilple line plots
line, = ax.plot(cad_st-360, Tcyl_Test2, label=label_Test2)
line, = ax.plot(cad_st-360, Tcyl_Test3, label=label_Test3)
line, = ax.plot(cad_st-360, Tcyl_Test4, label=label_Test4)
ax.legend()
plt.show()

# Calculate burn rate


from fc_dQ import dQ #call function to calculate combustion parameters

dQ_Test1, Q_Test1, Qr_Test1, IGN_Delay_Test1, HR10_Test1, HR1050_Test1, HR1090_Test1, HR50cad_Test1, cad_s= dQ (P_Test1, CR, SOI_Test1)
dQ_Test2, Q_Test2, Qr_Test2, IGN_Delay_Test2, HR10_Test2, HR1050_Test2, HR1090_Test2, HR50cad_Test2, cad_s= dQ (P_Test2, CR, SOI_Test2)
dQ_Test3, Q_Test3, Qr_Test3, IGN_Delay_Test3, HR10_Test3, HR1050_Test3, HR1090_Test3, HR50cad_Test3, cad_s= dQ (P_Test3, CR, SOI_Test3)
dQ_Test4, Q_Test4, Qr_Test4, IGN_Delay_Test4, HR10_Test4, HR1050_Test4, HR1090_Test4, HR50cad_Test4, cad_s= dQ (P_Test4, CR, SOI_Test4)

# Create apparent heat release rate plot
fig, ax = plt.subplots()
ax.grid() #create grid
ax.set_ylabel('AHRR, J/deg')
ax.set_xlabel('CAD \n \n Fig.9. Apparent Heat Release Rate')

maxval=np.max([np.max(dQ_Test1), np.max(dQ_Test2), np.max(dQ_Test3), np.max(dQ_Test4)])
ylim=maxval+5
ax.set_xlim(-20, 80) #set axe limits
ax.set_ylim(-3, ylim)
ax.xaxis.set_major_locator(MultipleLocator(10)) # distribute major ticks on x axis
ax.yaxis.set_major_locator(MultipleLocator(5)) # distribute major ticks on y axis


line, = ax.plot(cad_s-360, dQ_Test1, label=label_Test1) #create multilple line plots
line, = ax.plot(cad_s-360, dQ_Test2, label=label_Test2)
line, = ax.plot(cad_s-360, dQ_Test3, label=label_Test3)
line, = ax.plot(cad_s-360, dQ_Test4, label=label_Test4)
ax.legend()
plt.show()

# Create apparent heat release plot
fig, ax = plt.subplots()
ax.grid() #create grid
ax.set_ylabel('AHR, J')
ax.set_xlabel('CAD \n \n Fig.10. Apparent Heat Release')

maxval=np.max([np.max(Q_Test1), np.max(Q_Test2), np.max(Q_Test3), np.max(Q_Test4)])
ylim=maxval+40
ax.set_xlim(-20, 80) #set axe limits
ax.set_ylim(-60, ylim)
ax.xaxis.set_major_locator(MultipleLocator(10)) # distribute major ticks on x axis
ax.yaxis.set_major_locator(MultipleLocator(100)) # distribute major ticks on y axis
line, = ax.plot(cad_s-360, Q_Test1, label=label_Test1) #create multilple line plots
line, = ax.plot(cad_s-360, Q_Test2, label=label_Test2)
line, = ax.plot(cad_s-360, Q_Test3, label=label_Test3)
line, = ax.plot(cad_s-360, Q_Test4, label=label_Test4)
ax.legend()
plt.show()

# Create apparent heat release plot
fig, ax = plt.subplots()
ax.grid() #create grid
ax.set_ylabel('AHR, %')
ax.set_xlabel('CAD \n \n Fig.11. Apparent Relative Heat Release')

ax.set_xlim(-20, 80) #set axe limits
ax.set_ylim(-10, 105)
ax.xaxis.set_major_locator(MultipleLocator(10)) # distribute major ticks on x axis
ax.yaxis.set_major_locator(MultipleLocator(10)) # distribute major ticks on y axis
line, = ax.plot(cad_s-360, Qr_Test1, label=label_Test1) #create multilple line plots
line, = ax.plot(cad_s-360, Qr_Test2, label=label_Test2)
line, = ax.plot(cad_s-360, Qr_Test3, label=label_Test3)
line, = ax.plot(cad_s-360, Qr_Test4, label=label_Test4)
ax.legend()
plt.show()

# Create bar plot for Ignition Delay
Ignition_Delay = [IGN_Delay_Test2,IGN_Delay_Test3,IGN_Delay_Test4]

x = np.arange(np.size(Ignition_Delay)) # creates array for bar order
fig, ax = plt.subplots()
plt.bar(x, Ignition_Delay,width=0.3,color=['C1', 'C2', 'C3'])

for index, value in enumerate(x):
    plt.text(value, (Ignition_Delay[index]+0.5), str(np.round(Ignition_Delay[index],1)),horizontalalignment='center')
    
ax.set_ylabel('CAD')
ax.set_xlabel('Test Mode  \n \n Fig.12. Ignition Delay')

ylim=np.round((np.max(Ignition_Delay)+1),2)
ax.set_ylim(0, ylim)
plt.xticks(x, labels_line_fired)
plt.show()

# Create zoomed apparent heat release rate plot
fig, ax = plt.subplots()
ax.grid() #create grid
ax.set_ylabel('AHRR, J/deg')
ax.set_xlabel('CAD \n \n Fig.13. Apparent Heat Release Rate')

maxval=np.max([np.max(dQ_Test1), np.max(dQ_Test2), np.max(dQ_Test3), np.max(dQ_Test4)])
ylim=maxval+5
ax.set_xlim(-18, 2) #set axe limits
ax.set_ylim(-3, 2)
ax.xaxis.set_major_locator(MultipleLocator(1)) # distribute major ticks on x axis
ax.yaxis.set_major_locator(MultipleLocator(0.5)) # distribute major ticks on y axis
line, = ax.plot(cad_s-360, dQ_Test1, label=label_Test1) #create multilple line plots

# automatic annotation
x_Test2=-SOI_Test2
y_Test2=dQ_Test2[(200-SOI_Test2*10)]

x_Test3=-SOI_Test3
y_Test3=dQ_Test3[(200-SOI_Test3*10)]

x_Test4=-SOI_Test4
y_Test4=dQ_Test4[(200-SOI_Test4*10)]

arrow_SOI_Test2 = ax.annotate('SOI ' + str(SOI_Test2), xy=(x_Test2, y_Test2), xytext=(x_Test2 -1.5, y_Test2 + 1),
            arrowprops=dict(arrowstyle = '->', connectionstyle = 'arc3',facecolor='orange'))
arrow_SOI_Test3 = ax.annotate('SOI ' + str(SOI_Test3), xy=(x_Test3, y_Test3), xytext=(x_Test3 -1.5, y_Test3 + 1),
            arrowprops=dict(arrowstyle = '->', connectionstyle = 'arc3',facecolor='green'))
arrow_SOI_Test4 = ax.annotate('SOI ' + str(SOI_Test4), xy=(x_Test4, y_Test4), xytext=(x_Test4 -1.5 , y_Test4 + 1),
            arrowprops=dict(arrowstyle = '->', connectionstyle = 'arc3',facecolor='red'))

line, = ax.plot(cad_s-360, dQ_Test2, label=label_Test2)
line, = ax.plot(cad_s-360, dQ_Test3, label=label_Test3)
line, = ax.plot(cad_s-360, dQ_Test4, label=label_Test4)
ax.legend()
plt.show()

# Create bar plot for 50% AHR
HR50cad = [HR50cad_Test2,HR50cad_Test3,HR50cad_Test4]

x = np.arange(np.size(HR50cad)) # creates array for bar order
fig, ax = plt.subplots()
plt.bar(x, HR50cad,width=0.3,color=['C1', 'C2', 'C3'])

for index, value in enumerate(x):
    plt.text(value, (HR50cad[index]+1), str(np.round(HR50cad[index],1)),horizontalalignment='center')
    
ax.set_ylabel('CAD')
ax.set_xlabel('Test Mode \n \n Fig.14. Angle of 50% AHR')

ylim=np.round((np.max(HR50cad)+3),2)
ax.set_ylim(0, ylim)
plt.xticks(x, labels_line_fired)
plt.show()

# Create bar plot for duration of 10% AHR
HR10 = [HR10_Test2,HR10_Test3,HR10_Test4]

x = np.arange(np.size(HR10)) # creates array for bar order
fig, ax = plt.subplots()
plt.bar(x, HR10,width=0.3,color=['C1', 'C2', 'C3'])

for index, value in enumerate(x):
    plt.text(value, (HR10[index]+1), str(np.round(HR10[index],1)),horizontalalignment='center')
    
ax.set_ylabel('CAD')
ax.set_xlabel('Test Mode \n \n Fig.15. Duration of 10% AHR')

ylim=np.round((np.max(HR10)+3),2)
ax.set_ylim(0, ylim)
plt.xticks(x, labels_line_fired)
plt.show()

# Create bar plot for duration of 10% - 50% AHR
HR1050 = [HR1050_Test2,HR1050_Test3,HR1050_Test4]

x = np.arange(np.size(HR1050)) # creates array for bar order
fig, ax = plt.subplots()
plt.bar(x, HR1050,width=0.3,color=['C1', 'C2', 'C3'])

for index, value in enumerate(x):
    plt.text(value, (HR1050[index]+1), str(np.round(HR1050[index],1)),horizontalalignment='center')
    
ax.set_ylabel('CAD')
ax.set_xlabel('Test Mode \n \n Fig.16. Duration of 10-50% AHR')

ylim=np.round((np.max(HR1050)+3),2)
ax.set_ylim(0, ylim)
plt.xticks(x, labels_line_fired)
plt.show()

# Create bar plot for duration of 10% - 90% AHR
HR1090 = [HR1090_Test2,HR1090_Test3,HR1090_Test4]

x = np.arange(np.size(HR1090)) # creates array for bar order
fig, ax = plt.subplots()
plt.bar(x, HR1090,width=0.3,color=['C1', 'C2', 'C3'])

for index, value in enumerate(x):
    plt.text(value, (HR1090[index]+1), str(np.round(HR1090[index],1)),horizontalalignment='center')
    
ax.set_ylabel('CAD')
ax.set_xlabel('Test Mode \n \n Fig.17. Duration of 10-90% AHR')

ylim=np.round((np.max(HR1090)+3),2)
ax.set_ylim(0, ylim)
plt.xticks(x, labels_line_fired)
plt.show()



