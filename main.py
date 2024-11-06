# External imports
import pyaudio
import numpy as np
import threading
import time
import mido

# Internal imports
from plot import plot_graph
from tools import find_nearest_note
from default_values import RATE, DURATION_OUTPUT, AMPLITUDE_OUTPUT, SIGNAL_SIZE, ANALYSE_TYPE, NEAREST_NOTE_CIRCULAR_BUFFER_SIZE, TIME_SLEEP
from play_tone import play_tone
from fft_analyse import fft_analyse
from autocorrelation_analyse import autocorrelation_analyse
from midi import freq_manager
from nearest_note_update import nearest_note_update

# Init variables
p = pyaudio.PyAudio()
analyse_type = ANALYSE_TYPE["fft"] # "fft" or "autocorrelation"
plot = True
sound = True
stream_input = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=SIGNAL_SIZE)

# Global
nearest_note = 0.0
nearest_note_circular_buffer = np.zeros(NEAREST_NOTE_CIRCULAR_BUFFER_SIZE)
playing = True

# GETTER AND SETTER

def get_nearest_note():
    """ Return the nearest note to the current frequency. """
    global nearest_note
    return nearest_note

def set_nearest_note(note):
    """ Set the nearest note to the current frequency. """
    global nearest_note
    nearest_note = note

def get_playing():
    """ Return the playing state. """
    global playing
    return playing

def get_nearest_note_circular_buffer():
    """ Return the circular buffer of the nearest note. """
    global nearest_note_circular_buffer
    return nearest_note_circular_buffer

def roll_nearest_note_circular_buffer(note):
    """ Roll the circular buffer of the nearest note. """
    global nearest_note_circular_buffer
    nearest_note_circular_buffer[:-1] = nearest_note_circular_buffer[1:]
    nearest_note_circular_buffer[-1] = note

def get_audio_data():
    """ Get the audio data from the input stream. """
    data = np.frombuffer(stream_input.read(SIGNAL_SIZE, exception_on_overflow=False), dtype=np.int16)
    return data

# FUNCTIONS

def analyse_freq():
    while playing:
        global nearest_note
        data = get_audio_data()
        power = np.mean(data.astype(np.float32)**2)
        # If the power is high enough, analyse the frequency
        if power > 1000000:
            if analyse_type == ANALYSE_TYPE["fft"]:
                try:
                    fondamental_freq = fft_analyse(data)
                except Exception as e:
                    print(e)
            elif analyse_type == ANALYSE_TYPE["autocorrelation"]:
                try:
                    fondamental_freq = autocorrelation_analyse(data)
                except Exception as e:
                    print(e)
            if fondamental_freq != 0:
                roll_nearest_note_circular_buffer(find_nearest_note(fondamental_freq))
        else :
            roll_nearest_note_circular_buffer(0.0)
        time.sleep(TIME_SLEEP)

if __name__ == "__main__":
    # Create the MIDI output port
    midi_ports = mido.get_output_names()
    midi_port_name = next((port for port in midi_ports if "MIDIVoice" in port), None)
    if midi_port_name is None:
        raise ValueError("[MAIN] ERROR : Port MIDI : 'MIDIVoice' not found")
    else:
        print(f"Port MIDI : {midi_port_name} found")
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
    nearest_note_update_thread = threading.Thread(target=nearest_note_update, args=(
        set_nearest_note,
        get_nearest_note_circular_buffer,
        get_playing
    ), daemon=True)

    # Start threads
    try:
        analyse_freq_thread.start()
        nearest_note_update_thread.start()
        if(sound):
            play_tone_thread.start()
        midi_thread.start()
    except Exception as e:
        print(e)
    
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
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(e)

    # END Main loop
    playing = False
    midi_out.close()
    stream_input.stop_stream()
    stream_input.close()
    p.terminate()