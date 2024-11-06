# Default values

RATE = 44100
DURATION_OUTPUT = 0.1
AMPLITUDE_OUTPUT = 0.6
MIN_FREQ = 80
MAX_FREQ = 2000
SIGNAL_SIZE = 1024
# Type d'analyse de fréquence (fft ou autocorrelation)
ANALYSE_TYPE = {
    "fft": "0",
    "autocorrelation": "1"
}

if __name__ == "__main__":
    print("This file is not meant to be run.")
    print("RATE", RATE)
    print("DURATION_OUTPUT", DURATION_OUTPUT)
    print("AMPLITUDE_OUTPUT", AMPLITUDE_OUTPUT)
    print("MIN_FREQ", MIN_FREQ)
    print("MAX_FREQ", MAX_FREQ)
    print("SIGNAL_SIZE", SIGNAL_SIZE)
    print("ANALYSE_TYPE", ANALYSE_TYPE)