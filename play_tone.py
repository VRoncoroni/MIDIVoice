import numpy as np
import sounddevice as sd
from default_values import RATE, DURATION_OUTPUT, AMPLITUDE_OUTPUT

def play_tone(get_nearest_note, get_playing, rate=RATE, duration_output=DURATION_OUTPUT, amplitude_output=AMPLITUDE_OUTPUT):
    """Joue une onde sinusoïdale à la fréquence de la note la plus proche."""

    # Check types
    if not callable(get_nearest_note):
        raise ValueError("get_nearest_note must be a function")
    if not callable(get_playing):
        raise ValueError("get_playing must be a function")
    if not isinstance(rate, int):
        raise ValueError("rate must be an int")
    if not isinstance(duration_output, float):
        raise ValueError("duration_output must be a float")
    if not isinstance(amplitude_output, float):
        raise ValueError("amplitude_output must be a float")

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
                print(f"Changement de note : {current_frequency} Hz -> {nearest_note} Hz")
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
