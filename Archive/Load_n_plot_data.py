import numpy as np
import cPickle as pickle
import matplotlib.pyplot as plt

filename = 'simulation_data/NV_C011_F085_Amax_180k_tStep1ns_20131127_1227'
file = open(filename,'r')
N_NV = pickle.load(file)
B_Fields = pickle.load(file)
P_usefull = pickle.load(file)
N_addressable_C = pickle.load(file)

N_rejected =np.sum( np.sum(N_addressable_C,axis=1)==0)
x = np.delete(N_addressable_C, np.where(np.sum(N_addressable_C,axis=1) ==0) , axis =0)
print str(N_rejected) +' of ' +str(N_NV) +'NV centres rejected'

##plotting
plt.figure()
plt.ylabel('Probability that NV-Center is usefull')
plt.xlabel('B-Field [Gauss]')
plt.errorbar(B_Fields,P_usefull,yerr = 1/np.sqrt(N_NV))
plt.ylim([0,1])
plt.xlim([B_Fields[0]-100,B_Fields[-1]+100])

plt.figure()
plt.ylabel('Average number of addressable C')
plt.xlabel('B-Field [Gauss]')
plt.errorbar(B_Fields,np.mean(N_addressable_C,axis=0),yerr = np.std(N_addressable_C,axis=0))
plt.xlim([B_Fields[0]-100,B_Fields[-1]+100])

plt.figure()
plt.ylabel('Average number of addressable C in weakly coupled NVs' )
plt.xlabel('B-Field [Gauss]')
plt.errorbar(B_Fields,np.mean(x,axis=0),yerr = np.std(x,axis=0))
plt.xlim([B_Fields[0]-100,B_Fields[-1]+100])
plt.show()
