# External imports
import numpy as np

# Internal imports
from default_values import RATE, MIN_FREQ, MAX_FREQ, SIGNAL_SIZE
from tools import highpass_filter

def fft_analyse(data):
    
    # Check types
    if not isinstance(data, np.ndarray):
        raise ValueError("[fft_analyse] ERROR : data must be a numpy.ndarray")
    
    # Filter the data with a highpass filter
    try:
        data = highpass_filter(data)
    except Exception as e:
        print(e)

    fft_spectrum = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(data), 1 / RATE)
    valid_indices = (freqs >= MIN_FREQ) & (freqs <= MAX_FREQ)
    fft_spectrum = fft_spectrum[valid_indices]
    freqs = freqs[valid_indices]
    # Find the fondamental frequency
    fondamental_freq = freqs[np.argmax(np.abs(fft_spectrum))]
    return fondamental_freq

if __name__ == "__main__":
    print("This file is not meant to be run.")
    print("Start testing fft_analyse...")
    data = np.random.random(SIGNAL_SIZE)
    try:
        print(fft_analyse(data))
    except Exception as e:
        print(e)