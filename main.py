# External imports
import pyaudio
import numpy as np
import threading
import time
import mido

# Internal imports
from plot import plot_graph
from tools import find_nearest_note
from default_values import RATE, DURATION_OUTPUT, AMPLITUDE_OUTPUT, SIGNAL_SIZE, ANALYSE_TYPE
from play_tone import play_tone
from fft_analyse import fft_analyse
from autocorrelation_analyse import autocorrelation_analyse
from midi import freq_manager


# Init variables
p = pyaudio.PyAudio()
analyse_type = ANALYSE_TYPE["fft"]  # Type d'analyse de fréquence (fft ou autocorrelation)
plot = False
sound = False
stream_input = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=SIGNAL_SIZE)

# Global
nearest_note = 0.0
playing = True

# GETTER AND SETTER

def get_nearest_note():
    """Renvoie la note la plus proche de la fréquence actuelle."""
    global nearest_note
    return nearest_note

def get_playing():
    """Renvoie l'état de lecture."""
    global playing
    return playing

# FUNCTIONS

def get_audio_data():
    """Renvoie les données audio actuelles."""
    data = np.frombuffer(stream_input.read(SIGNAL_SIZE, exception_on_overflow=False), dtype=np.int16)
    return data


def analyse_freq():
    while playing:
        global nearest_note
        data = get_audio_data()
        power = np.mean(data.astype(np.float32)**2)
        # Lorsque la puissance du signal est suffisante, analyse la note jouée
        if power > 1000000:
            if analyse_type == ANALYSE_TYPE["fft"]:
                try:
                    fondamental_freq = fft_analyse(data)
                except Exception as e:
                    print(e)
                    print("ERR analyse_freq")
            elif analyse_type == ANALYSE_TYPE["autocorrelation"]:
                try:
                    fondamental_freq = autocorrelation_analyse(data)
                except Exception as e:
                    print(e)
                    print("ERR analyse_freq")
            if fondamental_freq != 0:
                nearest_note = find_nearest_note(fondamental_freq)
        else :
            nearest_note = 0.0
        time.sleep(0.05)


if __name__ == "__main__":
    # Créer un port MIDI
    midi_ports = mido.get_output_names()
    midi_port_name = next((port for port in midi_ports if "MIDIVoice" in port), None)
    if midi_port_name is None:
        raise ValueError("Port MIDI contenant 'MIDIVoice' non trouvé")
    else:
        print(f"Connexion au port MIDI : {midi_port_name}")
        midi_out = mido.open_output(midi_port_name)
    
    analyse_freq_thread = threading.Thread(target=analyse_freq, daemon=True)
    play_tone_thread = threading.Thread(target=play_tone, args=(
        get_nearest_note,
        get_playing,
        RATE,
        DURATION_OUTPUT,
        AMPLITUDE_OUTPUT
    ), daemon=True)

    midi_thread = threading.Thread(target=freq_manager, args=(
        midi_out,
        get_nearest_note,
        get_playing
    ), daemon=True)

    # Démarrer les threads
    try:
        analyse_freq_thread.start()
        if(sound):
            play_tone_thread.start()
        midi_thread.start()
    except Exception as e:
        print(e)
        print("ERR start thread")
    
    # Main loop
    try:
        if(plot):
            plot_graph(
                get_audio_data,
                get_nearest_note,
                SIGNAL_SIZE,
                RATE,
                DURATION_OUTPUT,
                AMPLITUDE_OUTPUT
            )
        else:
            while True:
                time.sleep(1)
    except KeyboardInterrupt: # Pour arrêter le programme
        print("Arrêt du programme")
    except Exception as e:
        print(e)

    # END loop
    playing = False

    midi_out.close()
    # Fermer le flux et PyAudio après la fin de l'animation
    stream_input.stop_stream()
    stream_input.close()
    p.terminate()