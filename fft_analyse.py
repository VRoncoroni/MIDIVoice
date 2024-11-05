# External imports
import numpy as np

# Internal imports
from default_values import RATE, MIN_FREQ, MAX_FREQ
from tools import highpass_filter

def fft_analyse(data):
    
    # Check types
    if not isinstance(data, np.ndarray):
        raise ValueError("data must be a numpy.ndarray")
    
    # Filtrer les basses fréquences
    try:
        data = highpass_filter(data)
    except Exception as e:
        print(e)
        print("ERR fft_analyse")

    # Calcul de la fréquence avec l'index de la plus grande composante spectrale
    fft_spectrum = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(data), 1 / RATE)
    # Filtrer les fréquences hors de la plage vocale
    valid_indices = (freqs >= MIN_FREQ) & (freqs <= MAX_FREQ)
    fft_spectrum = fft_spectrum[valid_indices]
    freqs = freqs[valid_indices]
    # Trouver la fréquence dominante
    fondamental_freq = freqs[np.argmax(np.abs(fft_spectrum))]
    return fondamental_freq

if __name__ == "__main__":
    print("This file is not meant to be run.")
    print("Start testing fft_analyse...")
    data = np.random.random(1024)
    try:
        print(fft_analyse(data))
    except Exception as e:
        print(e)