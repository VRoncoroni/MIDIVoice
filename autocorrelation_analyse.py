# External imports
import numpy as np

# Internal imports
from default_values import RATE, MIN_FREQ, MAX_FREQ
from tools import highpass_filter

def autocorrelation_analyse(data):

    # Check types
    if not isinstance(data, np.ndarray):
        raise ValueError("[autocorrelation_analyse] ERROR : data must be a numpy.ndarray")

    # Filter the data with a highpass filter and a lowpass filter
    try:
        data = highpass_filter(data)
        # data = lowpass_filter(data)
    except Exception as e:
        print(e)

    autocorr = np.correlate(data, data, mode='full')
    autocorr = autocorr[len(autocorr)//2:]
    d = np.diff(autocorr)
    start = np.where(d > 0)[0][0]
    peak = np.argmax(autocorr[start:]) + start
    # Find the fondamental frequency
    fondamental_freq = RATE / peak
    if peak <= 0 or fondamental_freq < MIN_FREQ or fondamental_freq > MAX_FREQ:
        fondamental_freq = 0
    if fondamental_freq == 0:
        print("[autocorrelation_analyse] ERR : Frequency not found")
    return fondamental_freq

if __name__ == "__main__":
    print("This file is not meant to be run.")
    print("Start testing autocorrelation_analyse...")
    data = np.random.random(1024)
    try:
        print(autocorrelation_analyse(data))
    except Exception as e:
        print(e)
    print("It's normal if the frequency is 0 because the data is random.")