# External imports
import numpy as np
import sounddevice as sd

# Internal imports
from default_values import RATE, DURATION_OUTPUT, AMPLITUDE_OUTPUT

def play_tone(get_nearest_note, get_playing, rate=RATE, duration_output=DURATION_OUTPUT, amplitude_output=AMPLITUDE_OUTPUT):
    """ Play a tone with the given frequency. """

    # Check types
    if not callable(get_nearest_note):
        raise ValueError("[play_tone] ERROR : get_nearest_note must be a function")
    if not callable(get_playing):
        raise ValueError("[play_tone] ERROR : get_playing must be a function")
    if not isinstance(rate, int):
        raise ValueError("[play_tone] ERROR : rate must be an int")
    if not isinstance(duration_output, float):
        raise ValueError("[play_tone] ERROR : duration_output must be a float")
    if not isinstance(amplitude_output, float):
        raise ValueError("[play_tone] ERROR : amplitude_output must be a float")

    t = np.linspace(0, duration_output, int(rate*duration_output), endpoint=False)
    with sd.OutputStream(samplerate=rate, channels=1) as stream_output:
        nearest_note = get_nearest_note()
        playing = get_playing()
        current_frequency = nearest_note
        wave = amplitude_output * np.sin(2 * np.pi * current_frequency * t)
        while playing:
            playing = get_playing()
            nearest_note = get_nearest_note()
            if nearest_note != current_frequency:
                print(f"Note change : {current_frequency} Hz -> {nearest_note} Hz")
                current_frequency = nearest_note
                wave = amplitude_output * np.sin(2 * np.pi * current_frequency * t)
            stream_output.write(wave.astype(np.float32))


if __name__ == "__main__":
    print("This file is not meant to be run.")

    print("Start testing play_tone...")
    print("Ctrl+C to stop")
    def get_nearest_note():
        return 440
    def get_playing():
        return True
    
    try:
        play_tone(
            get_nearest_note,
            get_playing
        )
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(e)
