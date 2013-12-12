import numpy as np
from scipy import linalg
from Calc_axis import Calc_axis

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


    M = np.zeros(np.shape(NV)[0])
    for idC in range(np.shape(NV)[0]):
        A= 2*np.pi*NV[idC,0]
        B= 2*np.pi*NV[idC,1]  #Converts to radial frequency in Hz/G
        H1 = (A+omega_larmor) *Iz +B*Ix
        exH1 = linalg.expm(-1j*H1*tau)
        V0 = exH0.dot(exH1.dot(exH1.dot(exH0)))
        V1 = exH1.dot(exH0.dot(exH0.dot(exH1)))
        n0 = Calc_axis(V0)
        n1 =Calc_axis(V1)
        phi = np.real(2*np.arccos(np.trace(V0)/2))
        M[idC] = 1 - (1-np.dot(n0,n1))*np.sin(n_pulses * phi /2 )**2

    Signal = -M.prod()
    F = (1-(Signal+1)/2)
    return F
