import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sounddevice as sd
import threading
from scipy.signal import butter, lfilter
import time

# Initialiser PyAudio et le flux audio une seule fois
p = pyaudio.PyAudio()
rate = 44100
min_freq = 80     # Fréquence minimale pour la voix humaine
max_freq = 800    # Fréquence maximale pour la voix humaine
analyse_type = "autocorrelation"  # Type d'analyse de fréquence (fft ou autocorrelation)
signal_size = 1024
duration_output = 0.1
amplitude_output = 0.6
plot = False

stream_input = p.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=signal_size)
nearest_note = 0
playing = True

# Fonction pour obtenir les données audio
def get_audio_data():
    data = np.frombuffer(stream_input.read(signal_size, exception_on_overflow=False), dtype=np.int16)
    return data

def play_tone():
    global nearest_note, playing, rate, duration_output, amplitude_output
    t = np.linspace(0, duration_output, int(rate*duration_output), endpoint=False)
    with sd.OutputStream(samplerate=rate, channels=1) as stream_output:
        current_frequency = nearest_note
        wave = amplitude_output * np.sin(2 * np.pi * current_frequency * t)
        while playing:
            if nearest_note != current_frequency:
                print(f"Changement de note : {current_frequency} Hz -> {nearest_note} Hz")
                current_frequency = nearest_note
                wave = amplitude_output * np.sin(2 * np.pi * current_frequency * t)
            stream_output.write(wave.astype(np.float32))

def find_nearest_note(real_note):
    global nearest_note
    # Tableau des fréquences des notes de la gamme tempérée de 80 Hz à 800 Hz
    notes_freq = [0, 82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61]
    notes_names = ["None", "La2", "La#2/Si♭2", "Si2", "Do3", "Do#3/Ré♭3", "Ré3", "Ré#3/Mi♭3", "Mi3", "Fa3", "Fa#3/Sol♭3", "Sol3", "Sol#3/La♭3", "La3", "La#3/Si♭3", "Si3", "Do4", "Do#4/Ré♭4", "Ré4", "Ré#4/Mi♭4", "Mi4", "Fa4", "Fa#4/Sol♭4", "Sol4", "Sol#4/La♭4", "La4", "La#4/Si♭4", "Si4", "Do5", "Do#5/Ré♭5", "Ré5", "Ré#5/Mi♭5", "Mi5", "Fa5", "Fa#5/Sol♭5", "Sol5", "Sol#5/La♭5", "La5", "La#5/Si♭5", "Si5", "Do6"]
    
    # Trouver la note la plus proche de la fréquence donnée
    index = np.argmin(np.abs(notes_freq - real_note))
    nearest_note = notes_freq[index]
    nearest_note_name = notes_names[index]
    print(f"Note la plus proche : {nearest_note_name} ({nearest_note} Hz)")

def highpass_filter(data, cutoff=80, fs=rate, order=5):
    nyq = 0.5 * fs  # Fréquence de Nyquist
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    y = lfilter(b, a, data)
    return y

def fft_analyse(data):
    # Filtrer les basses fréquences
    data = highpass_filter(data)

    # Calcul de la fréquence avec l'index de la plus grande composante spectrale
    fft_spectrum = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(data), 1 / rate)
    # Filtrer les fréquences hors de la plage vocale
    valid_indices = (freqs >= min_freq) & (freqs <= max_freq)
    fft_spectrum = fft_spectrum[valid_indices]
    freqs = freqs[valid_indices]
    # Trouver la fréquence dominante
    fondamental_freq = freqs[np.argmax(np.abs(fft_spectrum))]
    return fondamental_freq

def autocorrelation_analyse(data):
    # Filtrer les basses fréquences
    data = highpass_filter(data)

    autocorr = np.correlate(data, data, mode='full')
    autocorr = autocorr[len(autocorr)//2:]
    freqs = np.fft.rfftfreq(len(data), 1 / rate)
    # Filtrer les fréquences hors de la plage vocale
    d = np.diff(autocorr)
    start = np.where(d > 0)[0][0]  # Ignorer le début jusqu'à la première pente ascendante
    peak = np.argmax(autocorr[start:]) + start
    # Trouver la fréquence dominante
    fondamental_freq = rate / peak
    if peak <= 0 or fondamental_freq < min_freq or fondamental_freq > max_freq:
        fondamental_freq = 0
    if fondamental_freq == 0:
        print("Fréquence dominante non trouvée ERR autocorrelation_analyse")
    return fondamental_freq

def analyse_freq():
    while playing:
        global nearest_note
        data = get_audio_data()
        power = np.mean(data.astype(np.float32)**2)
        # Lorsque la puissance du signal est suffisante, analyse la note jouée
        if power > 300000:
            if analyse_type == "fft":
                fondamental_freq = fft_analyse(data)
            else:
                fondamental_freq = autocorrelation_analyse(data)
            # print(f"Fréquence dominante : {fondamental_freq} Hz")
            if fondamental_freq != 0:
                find_nearest_note(fondamental_freq)
        else :
            nearest_note = 0
        time.sleep(0.05)

analyse_freq_thread = threading.Thread(target=analyse_freq, daemon=True)
analyse_freq_thread.start()  # Démarrer le thread

def normalize(data):
    if np.max(np.abs(data)) > 0:  # Évitez la division par zéro
        data = data / np.max(np.abs(data))
    return data

# Fonction pour mettre à jour le graphique
def update_plot(frame):
    global nearest_note
    data = get_audio_data()
    # Normaliser data
    data = normalize(data)
    line.set_ydata(data)

    t = np.linspace(0, duration_output, signal_size, endpoint=False)
    wave = amplitude_output * np.sin(2 * np.pi * nearest_note * t)
    # Normaliser wave
    wave = normalize(wave)
    line3.set_ydata(wave)

    return line, line3

def update_plot2(frame):
    data = get_audio_data()
    
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
    line2.set_data(freqs, amplitudes)  
    return line2,

if plot:
    # Graph de l'onde sonore
    fig, ax = plt.subplots()
    x = np.arange(0, signal_size, 1)
    line, = ax.plot(x, np.random.rand(signal_size))
    ax.set_ylim(-2, 2)
    ax.set_xlim(0, signal_size)
    line3, = ax.plot(x, np.zeros(signal_size), 'r')
    #legende
    ax.legend(["Signal micro", "Signal de nearest note"], loc="upper right")

    # Graphique frequenciel
    fig2, ax2 = plt.subplots()
    x2 = np.linspace(0, rate / 2, int(signal_size / 2), endpoint=False)
    line2, = ax2.plot(x2, np.zeros(int(signal_size / 2))) # Initialiser le graphique avec des zéros
    ax2.set_ylim(0, 1)  # Ajustez les limites pour les amplitudes normalisées
    ax2.set_xlim(20, 900)  # Limite de fréquence
    ax2.set_xscale('log')

    # Lancer l'animation
    ani = animation.FuncAnimation(fig, update_plot, interval=25, blit=True)
    ani2 = animation.FuncAnimation(fig2, update_plot2, interval=25, blit=True)

    # Afficher le graphique
    plt.show()

try:
    play_tone()
except KeyboardInterrupt: # Pour arrêter le programme
    print("Arrêt du programme")



# Fermer le flux et PyAudio après la fin de l'animation
stream_input.stop_stream()
stream_input.close()
p.terminate()

playing = False