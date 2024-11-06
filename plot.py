import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from tools import normalize
from default_values import SIGNAL_SIZE, RATE, DURATION_OUTPUT, AMPLITUDE_OUTPUT, MIN_FREQ, MAX_FREQ, ANI_INTERVAL

# Fonction pour mettre à jour le graphique
def update_plotAUDIO(
        frame,
        get_data,
        line,
        line2,
        get_nearest_note,
        signal_size=SIGNAL_SIZE,
        duration_output=DURATION_OUTPUT,
        amplitude_output=AMPLITUDE_OUTPUT
    ):
    """ Update the graph with the audio data. """
    
    # Check types
    if not callable(get_data):
        raise ValueError("[update_plotAUDIO] ERROR : get_data must be a function")
    # check type of all parameters
    if not callable(get_nearest_note):
        raise ValueError("[update_plotAUDIO] ERROR : get_nearest_note must be a function")
    # signal_size int
    if not isinstance(signal_size, int):
        raise ValueError("[update_plotAUDIO] ERROR : signal_size must be an int")
    # duration_output float
    if not isinstance(duration_output, float):
        raise ValueError("[update_plotAUDIO] ERROR : duration_output must be a float")
    # amplitude_output float
    if not isinstance(amplitude_output, float):
        raise ValueError("[update_plotAUDIO] ERROR : amplitude_output must be a float")
    
    data = get_data()
    nearest_note = get_nearest_note()
    
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
        rate=RATE
    ):
    """ Update the graph with the FFT data. """
    
    # Check types
    if not callable(get_data):
        raise ValueError("[update_plotFFT] ERROR : get_data must be a function")
    # check type of all parameters
    if not isinstance(rate, int):
        raise ValueError("[update_plotFFT] ERROR : rate must be an int")  
    
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
        get_nearest_note,
        signal_size=SIGNAL_SIZE,
        rate=RATE,
        duration_output=DURATION_OUTPUT,
        amplitude_output=AMPLITUDE_OUTPUT
    ):
    """ Plot the graph with the audio data and the FFT data. """

    # Check types
    if not callable(get_data):
        raise ValueError("[plot_graph] ERROR : get_data must be a function")
    if not callable(get_nearest_note):
        raise ValueError("[plot_graph] ERROR : get_nearest_note must be a function")
    if not isinstance(signal_size, int):
        raise ValueError("[plot_graph] ERROR : signal_size must be an int")
    if not isinstance(rate, int):
        raise ValueError("[plot_graph] ERROR : rate must be an int")
    if not isinstance(duration_output, float):
        raise ValueError("[plot_graph] ERROR : duration_output must be a float")
    if not isinstance(amplitude_output, float):
        raise ValueError("[plot_graph] ERROR : amplitude_output must be a float")
    
    fig, ax = plt.subplots()
    x = np.arange(0, signal_size, 1)
    line, = ax.plot(x, np.random.rand(signal_size))
    ax.set_ylim(-2, 2)
    ax.set_xlim(0, signal_size)
    line2, = ax.plot(x, np.zeros(signal_size), 'r')
    ax.legend(["Signal micro", "Signal de nearest note"], loc="upper right")

    fig2, ax2 = plt.subplots()
    fig2_size = int(signal_size / 2)
    x2 = np.linspace(0, rate / 2, fig2_size, endpoint=False)
    line3, = ax2.plot(x2, np.zeros(fig2_size))
    ax2.set_ylim(0, 1)
    ax2.set_xlim(MIN_FREQ, MAX_FREQ)
    ax2.set_xscale('log')

    try:
        ani = animation.FuncAnimation(fig, update_plotAUDIO, fargs=(
            get_data,
            line,
            line2,
            get_nearest_note,
            signal_size,
            duration_output,
            amplitude_output
        ), interval=ANI_INTERVAL, blit=True)
    except Exception as e:
        print(e)
        return
    
    try:
        ani2 = animation.FuncAnimation(fig2, update_plotFFT, fargs=(
            get_data,
            line3,
            rate
        ), interval=ANI_INTERVAL, blit=True)
    except Exception as e:
        print(e)
        return

    plt.show()

if __name__ == "__main__":
    data = np.random.randint(-100, 100, 1024)
    def get_data():
        return data
    def get_nearest_note():
        return 440
    plot_graph(
        get_data=get_data,
        get_nearest_note=get_nearest_note,
    )