TIME_SLEEP = 0.05
RATE = 44100
DURATION_OUTPUT = 0.1
AMPLITUDE_OUTPUT = 0.6
MIN_FREQ = 80
MAX_FREQ = 2000
SIGNAL_SIZE = 1024
ANALYSE_TYPE = {
    "fft": "0",
    "autocorrelation": "1"
}
NEAREST_NOTE_CIRCULAR_BUFFER_SIZE = 4
DEFAULT_MIDI_VELOCITY = 100
ANI_INTERVAL = 50

if __name__ == "__main__":
    print("This file is not meant to be run.")
    print("TIME_SLEEP", TIME_SLEEP)
    print("RATE", RATE)
    print("DURATION_OUTPUT", DURATION_OUTPUT)
    print("AMPLITUDE_OUTPUT", AMPLITUDE_OUTPUT)
    print("MIN_FREQ", MIN_FREQ)
    print("MAX_FREQ", MAX_FREQ)
    print("SIGNAL_SIZE", SIGNAL_SIZE)
    print("ANALYSE_TYPE", ANALYSE_TYPE)
    print("NEAREST_NOTE_CIRCULAR_BUFFER_SIZE", NEAREST_NOTE_CIRCULAR_BUFFER_SIZE)
    print("DEFAULT_MIDI_VELOCITY", DEFAULT_MIDI_VELOCITY)
    print("ANI_INTERVAL", ANI_INTERVAL)