import numpy as np
from scipy.signal import butter, lfilter
from default_values import RATE

def normalize(data):
    """ Normalize Data. """
    if data is None:
        raise ValueError("[normalize] ERROR : data is None")

    if np.max(np.abs(data)) > 0:
        data = data / np.max(np.abs(data))
    return data

def find_nearest_note(real_note):
    """ Find the nearest note to the real note. """
    
    #Check type
    if not isinstance(real_note, float):
        raise ValueError("[find_nearest_note] ERROR : real_note must be a float")  
    
    # Tableau des fréquences des notes de la gamme tempérée
    notes_freq = np.array([0, 82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77, 1046.50, 1108.73, 1174.66, 1244.51, 1318.51, 1396.91, 1479.98, 1567.98, 1661.22, 1760.00, 1864.66, 1975.53, 2093.00, 2217.46, 2349.32, 2489.02, 2637.02, 2793.83, 2959.96, 3135.96, 3322.44, 3520.00, 3729.31, 3951.07, 4186.01])
    notes_names = ["None", "La2", "La#2/Si♭2", "Si2", "Do3", "Do#3/Ré♭3", "Ré3", "Ré#3/Mi♭3", "Mi3", "Fa3", "Fa#3/Sol♭3", "Sol3", "Sol#3/La♭3", "La3", "La#3/Si♭3", "Si3", "Do4", "Do#4/Ré♭4", "Ré4", "Ré#4/Mi♭4", "Mi4", "Fa4", "Fa#4/Sol♭4", "Sol4", "Sol#4/La♭4", "La4", "La#4/Si♭4", "Si4", "Do5", "Do#5/Ré♭5", "Ré5", "Ré#5/Mi♭5", "Mi5", "Fa5", "Fa#5/Sol♭5", "Sol5", "Sol#5/La♭5", "La5", "La#5/Si♭5", "Si5", "Do6", "Do#6/Ré♭6", "Ré6", "Ré#6/Mi♭6", "Mi6", "Fa6", "Fa#6/Sol♭6", "Sol6", "Sol#6/La♭6", "La6", "La#6/Si♭6", "Si6", "Do7", "Do#7/Ré♭7", "Ré7", "Ré#7/Mi♭7", "Mi7", "Fa7", "Fa#7/Sol♭7", "Sol7", "Sol#7/La♭7", "La7", "La#7/Si♭7", "Si7", "Do8"]

    # Trouver la note la plus proche de la fréquence donnée
    index = np.argmin(np.abs(notes_freq - real_note))
    if index > len(notes_freq) - 1 and index > len(notes_names) - 1:
        raise ValueError("[find_nearest_note] ERROR : Index out of range")
    nearest = notes_freq[index]
    # nearest_note_name = notes_names[index]

    return nearest

def highpass_filter(data, cutoff=80, fs=RATE, order=5):
    """ Highpass filter the audio data. """

    # Check types
    if not isinstance(data, np.ndarray):
        raise ValueError("[highpass_filter] ERROR : data must be a numpy.ndarray")
    if not isinstance(cutoff, int):
        raise ValueError("[highpass_filter] ERROR : cutoff must be an int")
    if not isinstance(fs, int):
        raise ValueError("[highpass_filter] ERROR : fs must be an int")
    if not isinstance(order, int):
        raise ValueError("[highpass_filter] ERROR : order must be an int")
    if not isinstance(data, np.ndarray):
        raise ValueError("[highpass_filter] ERROR : data must be a numpy.ndarray")

    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    y = lfilter(b, a, data)
    return y

def lowpass_filter(data, cutoff=800, fs=RATE, order=5):
    """ Lowpass filter the audio data. """

    # Check types
    if not isinstance(data, np.ndarray):
        raise ValueError("[lowpass_filter] ERROR : data must be a numpy.ndarray")
    if not isinstance(cutoff, int):
        raise ValueError("[lowpass_filter] ERROR : cutoff must be an int")
    if not isinstance(fs, int):
        raise ValueError("[lowpass_filter] ERROR : fs must be an int")
    if not isinstance(order, int):
        raise ValueError("[lowpass_filter] ERROR : order must be an int")

    if data is None:
        raise ValueError("[lowpass_filter] ERROR : data is None")

    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, data)
    return y

def freq_to_midi(frequency):
    if frequency <= 0:
        raise ValueError("[freq_to_midi] ERROR : The frequency must be positive.")
    return round(69 + 12 * np.log2(frequency / 440))

if __name__ == "__main__":
    print("This file is not meant to be run.")
    print("Start testing tools...")
    data = np.random.randint(-1000, 1000, 1024)

    print("Start testing normalize...")
    try:
        print(data)
        normalized_data = normalize(data)
        print(normalized_data)
        if np.max(np.abs(normalized_data)) > 1:
            raise ValueError("[normalize] ERROR : Wrong normalization")
    except Exception as e:
        print(e)

    print("Start testing find_nearest_note...")
    try:
        real_note = 438.0
        nearest_note = find_nearest_note(real_note)
        if nearest_note != 440.0:
            raise ValueError("[find_nearest_note] ERROR : Wrong note")
        print("Real note : ", real_note, " Hz", "Nearest note : ", nearest_note , "Hz")
    except Exception as e:
        print(e)

    print("Start testing highpass_filter...")
    try:
        print(highpass_filter(data))
    except Exception as e:
        print(e)
    print("Start testing lowpass_filter...")
    try:
        print(lowpass_filter(data))
    except Exception as e:
        print(e)

    print("Start testing freq_to_midi...")
    try:
        value = freq_to_midi(440)
        print(freq_to_midi(440))
        if value != 69:
            raise ValueError("[freq_to_midi] ERROR : Wrong value")
    except Exception as e:
        print(e)