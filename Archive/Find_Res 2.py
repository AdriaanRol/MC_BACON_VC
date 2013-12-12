import numpy as np
from scipy import linalg #For matrix exponential

from Calc_axis import Calc_axis
from find_mins import find_mins
from check_pulse_t import check_pulse_t

def Find_Res(HyperfineStr=[1.4680e+4,2.9361e3] ,B_field =400 ,tau_max=6*1e-6,tau_step = 0.005*1e-6, max_gate_time = 8000*1e-6):
    """
    Finds resonant driving conditions and number of pulses required for a hyperfine strength
    input HyperfineStr in real freq
    but number of pulses unreliable because of dependency on timestep
    """
    #physical constants
    gamma_c = 1.071e3 #g-factor for C13 in MHz/G
    #Model parameters
    timesteps = np.arange(tau_step,tau_max,tau_step)
    omega_larmor = 2*np.pi*gamma_c*B_field
    tau_larmor = 2*np.pi/omega_larmor

    A= 2*np.pi*HyperfineStr[0]
    B= 2*np.pi*HyperfineStr[1]  #Converts to radial frequency in Hz

    Ix = 0.5 * np.array([[0,1],[1,0]])
    Iz = 0.5* np.array([[1,0],[0,-1]])
    H0 = (omega_larmor)*Iz
    H1 = (A+omega_larmor) *Iz +B*Ix

    li_n0 = []
    li_n1=[]
    ax_prod = np.zeros(np.size(timesteps))
    #Char evolution
    for idt, tau in enumerate(timesteps):
        exH0 =linalg.expm(-1j*H0*tau)
        exH1 = linalg.expm(-1j*H1*tau)
        V0 = exH0.dot(exH1.dot(exH1.dot(exH0)))
        V1 = exH1.dot(exH0.dot(exH0.dot(exH1)))
        #li_V0.append(V0)#appending takes shitloads of time. Maybe dump this line
        #li_V1.append(V1)

        n0 = Calc_axis(V0)
        n1 =Calc_axis(V1)
        ax_prod[idt] = np.dot(n0,n1)
    #Find Resonances as minima
    dip_ind = find_mins(ax_prod)
    theta = np.zeros(np.size(dip_ind))
    for idi, ind in enumerate(dip_ind):  #Either save V0's and calc only needed theta or calc all and not save V0
        tau = timesteps[ind]
        exH0 =linalg.expm(-1j*H0*tau)
        exH1 = linalg.expm(-1j*H1*tau)
        V0 = exH0.dot(exH1.dot(exH1.dot(exH0)))
        theta[idi] = np.real(2*np.arccos(np.trace(V0)/2))
    n_pulses = np.divide(np.pi,(2*(np.pi-np.abs(np.pi-theta)))).astype(int)
    tlist = timesteps[dip_ind]
    res = check_pulse_t(tlist, n_pulses, max_gate_time)
    return res
