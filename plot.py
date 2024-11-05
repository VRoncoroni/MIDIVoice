import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from tools import normalize

# Fonction pour mettre à jour le graphique
def update_plotAUDIO(
        frame,
        get_data,
        line,
        line2,
        nearest_note=440.0,
        signal_size=1024,
        duration_output=0.1,
        amplitude_output=0.4
    ):
    """ Met à jour les données du graphique avec les données audio et une onde sinusoïdale. """
    
    
    # if get_data is not a fonction, raise
    if not callable(get_data):
        raise ValueError("get_data must be a function")
    # check type of all parameters
    if not isinstance(nearest_note, float):
        raise ValueError("nearest_note must be a float")
    # signal_size int
    if not isinstance(signal_size, int):
        raise ValueError("signal_size must be an int")
    # duration_output float
    if not isinstance(duration_output, float):
        raise ValueError("duration_output must be a float")
    # amplitude_output float
    if not isinstance(amplitude_output, float):
        raise ValueError("amplitude_output must be a float")
    
    data = get_data()
    
    # Normaliser data
    data = normalize(data)
    line.set_ydata(data)
    t = np.linspace(0, float(duration_output), int(signal_size), endpoint=False)
    wave = amplitude_output * np.sin(2 * np.pi * nearest_note * t)
    
    # Normaliser wave
    wave = normalize(wave)
    line2.set_ydata(wave)

    return line, line2

def update_plotFFT(
        frame,
        get_data,
        line,
        rate=44100
    ):
    """Met à jour le graphique avec le spectre FFT des données audio."""
    
    # if get_data is not a fonction, raise
    if not callable(get_data):
        raise ValueError("get_data must be a function")
    # check type of all parameters
    if not isinstance(rate, int):
        raise ValueError("rate must be an int")  
    
    data = get_data()
    
    # Appliquer la FFT
    fft_spectrum = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(data), 1 / rate)
    
    # Calculer les amplitudes et ne garder que les valeurs positives
    amplitudes = np.abs(fft_spectrum)[:len(fft_spectrum) // 2]
    freqs = freqs[:len(freqs) // 2]  # Ne garder que les fréquences positives

    # Normaliser les amplitudes
    if np.max(amplitudes) > 0:  # Pour éviter la division par zéro
        amplitudes = amplitudes / np.max(amplitudes)

    # Mettre à jour le graphique
    line.set_data(freqs, amplitudes)  
    return line,

def plot_graph(
        get_data,
        nearest_note=440.0,
        signal_size=1024,
        rate=44100,
        duration_output=0.1,
        amplitude_output=0.4
    ):
    """Crée les graphiques et lance les animations pour les données audio."""
    
    # Graph de l'onde sonore
    fig, ax = plt.subplots()
    x = np.arange(0, signal_size, 1)
    line, = ax.plot(x, np.random.rand(signal_size))
    ax.set_ylim(-2, 2)
    ax.set_xlim(0, signal_size)
    line2, = ax.plot(x, np.zeros(signal_size), 'r')
    #legende
    ax.legend(["Signal micro", "Signal de nearest note"], loc="upper right")

    # Graphique frequenciel
    fig2, ax2 = plt.subplots()
    fig2_size = int(signal_size / 2)
    x2 = np.linspace(0, rate / 2, fig2_size, endpoint=False)
    line3, = ax2.plot(x2, np.zeros(fig2_size))
    ax2.set_ylim(0, 1)
    ax2.set_xlim(20, 900)
    ax2.set_xscale('log')

    # Lancer l'animation

    try:
        ani = animation.FuncAnimation(fig, update_plotAUDIO, fargs=(
            get_data,
            line,
            line2,
            nearest_note,
            signal_size,
            duration_output,
            amplitude_output
        ), interval=25, blit=True)
    except Exception as e:
        print(e)
        print("Error in update_plotAUDIO")
        return
    
    try:
        ani2 = animation.FuncAnimation(fig2, update_plotFFT, fargs=(
            get_data,
            line3,
            rate
        ), interval=25, blit=True)
    except Exception as e:
        print(e)
        print("Error in update_plotFFT")
        return

    # Afficher le graphique
    plt.show()

if __name__ == "__main__":
    data = np.random.randint(-100, 100, 1024)
    def get_data():
        return data
    plot_graph(get_data=get_data)