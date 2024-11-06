# External imports
import mido
from mido import Message
import time

# Internal imports
from tools import freq_to_midi

def play_midi_note(midi_out, freq, velocity=127):
    """Joue une note MIDI."""
    note = freq_to_midi(freq)
    midi_out.send(Message('note_on', note=note, velocity=velocity))

def stop_midi_note(midi_out, freq):
    """Arrête une note MIDI."""
    note = freq_to_midi(freq)
    midi_out.send(Message('note_off', note=note))

def freq_manager(midi_out, get_nearest_note, get_playing):
    """Gère les fréquences et les notes MIDI."""
    current_freq = 0
    playing = get_playing()
    while playing:
        nearest_note = get_nearest_note()
        playing = get_playing()
        if nearest_note != current_freq:
            if nearest_note != 0:
                play_midi_note(midi_out, nearest_note)
            if current_freq != 0:
                stop_midi_note(midi_out, current_freq)
            current_freq = nearest_note
        time.sleep(0.1)


if __name__ == "__main__":
    print("This file is not meant to be run.")
    print("Start testing midi")
    # Créer un port MIDI
    midi_ports = mido.get_output_names()
    midi_port_name = next((port for port in midi_ports if "MIDIVoice" in port), None)
    if midi_port_name is None:
        raise ValueError("Port MIDI contenant 'MIDIVoice' non trouvé")
    else:
        print(f"Connexion au port MIDI : {midi_port_name}")
        midi_out = mido.open_output(midi_port_name)
    
    print("Playing a note...")
    play_midi_note(midi_out, 440)
    time.sleep(1)
    print("Stopping the note...")
    stop_midi_note(midi_out, 440)
    print("If LMMS is open, and MIDIVoice selected, you should have heard a sound.")