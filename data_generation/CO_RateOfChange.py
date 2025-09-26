import numpy as np


def CO_RateOfChange(y: list, tau: int, sloppy: bool):
    """
    Rate of change of a time series

    Parameters:
    -----------
    y : array-like
        The input time series

        tau : int
        The time delay

        all : bool
        if True, considers all time series points, regardless of the sign of the time series 
        if False, separates the time series into positive, negative and transitions parts and calculates the rate of change of each part separately 
    
    Returns:
    --------
    array-like
        The rate of change of the input time series

    """

    if sloppy == True:
        if tau == 1:
            y=np.array(y)
            # Case tau=1 on the entire time series ( do not consider different taus and not separate the time series into positive,negative parts)
            return np.diff(y)
        else:
            y = np.array(y)

            diff_y=[]
            for i in range(len(y)-tau):
                diff_y.append(y[i+tau]-y[i])
            return np.array(diff_y)

    
    else:
        # Separate the time series into positive, negative and transitions parts
        y = np.array(y)
        ix_pos = np.where(y > 0)[0] # positive part of the time series
        ix_neg = np.where(y < 0)[0] # negative part of the time series
        ix = [ix_pos, ix_neg] 
        n = [len(ix_pos), len(ix_neg)]

        # Calculate the rate of change of each part separately
        roc = [[], []]
        for i in range(2):
            if n[i] > 0:
                roc[ix[i]] = np.diff(y[ix[i]]) #/ y[ix[i]][:-1]
        all_roc = np.concatenate(roc)

        return all_roc
