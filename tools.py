import numpy as np

def normalize(data):
    if np.max(np.abs(data)) > 0:  # Évitez la division par zéro
        data = data / np.max(np.abs(data))
    return data