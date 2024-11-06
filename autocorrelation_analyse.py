# External imports
import numpy as np

# Internal imports
from default_values import RATE, MIN_FREQ, MAX_FREQ
from tools import highpass_filter

def autocorrelation_analyse(data):

    # Check types
    if not isinstance(data, np.ndarray):
        raise ValueError("data must be a numpy.ndarray")

    # Filtrer les basses fréquences et les hautes fréquences
    try:
        data = highpass_filter(data)
        # data = lowpass_filter(data)
    except Exception as e:
        print(e)
        print("ERR fft_analyse")

    autocorr = np.correlate(data, data, mode='full')
    autocorr = autocorr[len(autocorr)//2:]
    freqs = np.fft.rfftfreq(len(data), 1 / RATE)
    # Filtrer les fréquences hors de la plage vocale
    d = np.diff(autocorr)
    start = np.where(d > 0)[0][0]  # Ignorer le début jusqu'à la première pente ascendante
    peak = np.argmax(autocorr[start:]) + start
    # Trouver la fréquence dominante
    fondamental_freq = RATE / peak
    if peak <= 0 or fondamental_freq < MIN_FREQ or fondamental_freq > MAX_FREQ:
        fondamental_freq = 0
    if fondamental_freq == 0:
        print("Fréquence dominante non trouvée ERR autocorrelation_analyse")
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