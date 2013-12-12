import numpy as np
from scipy import linalg

def Char_Gate(NV,res ,B_field=400):
    """
    Characterize the gate, take the NV centre, the resonance paramters and the Bfield as input
    returns the fidelity with which an x-gate can be implemented.
    """


    #data = np.loadtxt("NV_Sim_8.dat") #Placeholder data to test the script
    #NV = np.vstack((data[:,3],data[:,4]))
    #physical constants
    gamma_c = 1.071e3 #g-factor for C13 in Hz/G
    #Model parameters
    omega_larmor = 2*np.pi*gamma_c*B_field
    tau_larmor = 2*np.pi/omega_larmor
    tau = res[0]
    n_pulses = int(res[1]*2) #So that we do a pi -pulse

    Ix = 0.5 * np.array([[0,1],[1,0]])
    Iz = 0.5* np.array([[1,0],[0,-1]])
    H0 = (omega_larmor)*Iz
    exH0 =linalg.expm(-1j*H0*tau)

    S_final =1
    for idC in range(np.shape(NV)[1]):
        A= 2*np.pi*NV[0,idC]
        B= 2*np.pi*NV[1,idC]  #Converts to radial frequency in Hz/G
        H1 = (A+omega_larmor) *Iz +B*Ix
        exH1 = linalg.expm(-1j*H1*tau)
        V0 = exH0.dot(exH1.dot(exH1.dot(exH0)))
        V1 = exH1.dot(exH0.dot(exH0.dot(exH1)))
        S = np.real(np.trace(np.dot(np.linalg.matrix_power(V0,n_pulses),np.linalg.matrix_power(V1,n_pulses)))/2)
        S_final = S_final *S
    F = (1-(S_final+1)/2) #Converting from probability of measuring +X to fidelity of -X (x-rotation)
    return F
