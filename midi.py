# External imports
import mido
from mido import Message
import time

# Internal imports
from tools import freq_to_midi
from default_values import TIME_SLEEP, DEFAULT_MIDI_VELOCITY

def play_midi_note(midi_out, freq, velocity=DEFAULT_MIDI_VELOCITY):
    """ Play a MIDI note. """
    note = freq_to_midi(freq)
    midi_out.send(Message('note_on', note=note, velocity=velocity))

def stop_midi_note(midi_out, freq):
    """ Stop a MIDI note. """
    note = freq_to_midi(freq)
    midi_out.send(Message('note_off', note=note))

def freq_manager(midi_out, get_nearest_note, get_playing):
    """ Manage the frequency to play. """
    current_freq = 0
    playing = get_playing()
    while playing:
        nearest_note = get_nearest_note()
        playing = get_playing()
        if nearest_note != current_freq:
            print(f"Note change : {current_freq} Hz -> {nearest_note} Hz")
            if nearest_note != 0:
                play_midi_note(midi_out, nearest_note)
            if current_freq != 0:
                stop_midi_note(midi_out, current_freq)
            current_freq = nearest_note
        time.sleep(TIME_SLEEP)


if __name__ == "__main__":
    print("This file is not meant to be run.")
    print("Start testing midi")
    # Créer un port MIDI
    midi_ports = mido.get_output_names()
    midi_port_name = next((port for port in midi_ports if "MIDIVoice" in port), None)
    if midi_port_name is None:
        raise ValueError("[MIDI MAIN] ERROR : Port MIDI 'MIDIVoice' not found")
    else:
        print(f"Port MIDI : {midi_port_name} found")
        midi_out = mido.open_output(midi_port_name)
    
    print("Playing a note...")
    play_midi_note(midi_out, 440)
    time.sleep(1)
    print("Stopping the note...")
    stop_midi_note(midi_out, 440)
    print("If LMMS is open, and MIDIVoice selected, you should have heard a sound.")