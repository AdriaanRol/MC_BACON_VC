import numpy as np
def Find_Res(HyperfineStr,B_field,tau_range=4):
    """
    Finds resonant driving conditions and number of pulses required for a hyperfine strength
    NOW A PLACEHOLDER FUNCTION THAT RETURNS RANDOM OUTPUT
    """
    k = np.random.randint(1,4, size = 1)
    tau = np.random.rand(k)
    tau = np.sort(tau,axis =0)
    n_pulses = np.random.randint(20,size = k)
    res = np.column_stack((tau,n_pulses))
    return res
