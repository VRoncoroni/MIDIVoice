# External imports
import time
import numpy as np

# Internal imports
from default_values import TIME_SLEEP

def nearest_note_update(set_nearest_note, get_nearest_note_circular_buffer, get_playing):
    """" Nearest note update """

    #Check types
    if not callable(set_nearest_note):
        raise ValueError("[nearest_note_update] ERROR : set_nearest_note must be a function")
    if not callable(get_nearest_note_circular_buffer):
        raise ValueError("[nearest_note_update] ERROR : get_nearest_note_circular_buffer must be a function")
    if not callable(get_playing):
        raise ValueError("[nearest_note_update] ERROR : get_playing must be a function")
    
    nearest_note_circular_buffer = get_nearest_note_circular_buffer()
    playing = get_playing()

    # Need NEAREST_NOTE_CIRCULAR_BUFFER_SIZE same notes to update nearest note
    while playing:
        playing = get_playing()
        nearest_note_circular_buffer = get_nearest_note_circular_buffer()
        if np.all(nearest_note_circular_buffer == nearest_note_circular_buffer[0]):
            set_nearest_note(nearest_note_circular_buffer[0])
        else:
            set_nearest_note(0.0)
        time.sleep(TIME_SLEEP)

if __name__ == "__main__":
    print("This file is not meant to be run.")
    print("Start testing nearest_note_update...")

    def set_nearest_note(note):
        print(f"Setting nearest note to {note} Hz")

    def get_nearest_note_circular_buffer():
        return np.array([440.0, 440.0, 440.0, 440.0])
    
    playing = True
    def get_playing():
        global playing
        return playing

    try:
        nearest_note_update(
            set_nearest_note,
            get_nearest_note_circular_buffer,
            get_playing
        )
    except KeyboardInterrupt:
        print("Interrupted by user")
        playing = False
    except Exception as e:
        print(e)