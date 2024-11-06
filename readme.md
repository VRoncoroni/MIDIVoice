# MIDIVoice

MIDIVoice is an open-source project that enables real-time analysis, visualization, and generation of MIDI signals from the human voice.

Libray used:
- `numpy`
- `matplotlib`
- `sounddevice`
- `mido`
- `loopMIDI`
- `pyaudio`
- `threading`
- `time`
- `scipy`

Software used:
- `Python 3.10.6`
- [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)

## Analyzing Fundamental Frequency Retrieval with Auto-Correlation

Analyzing the fundamental frequency (F0) of an audio signal is a crucial task in signal processing. In this project, we use **auto-correlation** to extract the F0 from the human voice.

### 1. Auto-Correlation

Auto-correlation is a measure of similarity between a signal and a time-shifted version of itself. Mathematically, the auto-correlation of a signal $ x[n] $ is defined as:

$$ R_x[m] = \sum_{n=0}^{N-1} x[n] \cdot x[n-m] $$

where:

- $ R_x[m] $ is the auto-correlation value for the lag $ m $.
- $ x[n] $ is the audio signal.
- $ N $ is the total number of samples in the signal.

### 2. Detecting the Fundamental Frequency

To extract the fundamental frequency $ f_0 $ of an audio signal, we use auto-correlation to find the first significant peak in the auto-correlation. This peak corresponds to the period of the signal, which is inversely proportional to the fundamental frequency:

$$ f_0 = \frac{rate}{m} $$

where:

- $ \text{rate} $ is the sampling rate of the audio signal.
- $ m $ is the index of the first significant peak in the auto-correlation.

### 3. Limitations of Auto-Correlation

Auto-correlation is a simple and effective method to extract the fundamental frequency of an audio signal. However, it can be sensitive to certain artifacts, such as noise, harmonics, and vocal formants. To improve the robustness of the analysis, preprocessing and post-processing techniques, such as smoothing, harmonic suppression, and voice detection, can be used.

For example, we applied a high-pass filter to remove low frequencies and harmonics that could interfere with fundamental frequency detection.

## Fourier Transform Analysis with NumPy

This section explains the use of `np.fft.fft()` and `np.fft.fftfreq()` functions for frequency analysis of an audio signal.

### 1. Discrete Fourier Transform with `np.fft.fft`

The **Discrete Fourier Transform (DFT)** decomposes a time-domain signal $ x[n] $ into its frequency components. Mathematically, the DFT of $ x[n] $, for $ n = 0, 1, \ldots, N-1 $, is defined as:

$$ X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-j \frac{2 \pi}{N} k n} $$

where:
- $ X[k] $ is the frequency component for index $ k $ (the associated frequency).
- $ N $ is the total number of samples in the signal.
- $ j $ is the imaginary unit ($ j^2 = -1 $).
- $ e^{-j \frac{2 \pi}{N} k n} $ is a complex oscillation representing each frequency in the signal.

In Python, this equation is computed by `np.fft.fft(audio_signal)`, which returns an array $ X[k] $ (referred to as `fft_spectrum` in the code).

#### Interpreting Values in `fft_spectrum`

The result `fft_spectrum` is a complex array where each element $ X[k] $ contains:
- The **magnitude** $ |X[k]| $: the amplitude of the frequency corresponding to index $ k $.
- The **phase** $ \arg(X[k]) $: the phase shift of this frequency.

To extract the amplitude of each frequency, we use:
$$ A = |X[k]| = \sqrt{\Re(X[k])^2 + \Im(X[k])^2} $$
where $ \Re(X[k]) $ and $ \Im(X[k]) $ represent the real and imaginary parts of $ X[k] $, respectively.

### 2. Corresponding Frequencies with `np.fft.fftfreq`

To find the frequencies $ f[k] $ represented by each index $ k $ in `fft_spectrum`, we use the `np.fft.fftfreq()` function. This function computes the actual frequencies in Hertz (Hz) corresponding to the indices $ k $.

The frequency associated with each index $ k $ is given by:

$$ f[k] = \frac{k \cdot \text{rate}}{N} $$

where:
- $ f[k] $ is the frequency associated with index $ k $,
- $ \text{rate} $ is the sampling rate (e.g., 44100 Hz),
- $ N $ is the signal size (number of samples in `audio_signal`).

#### Frequency Range Obtained

- Indices $ k = 0, 1, \ldots, N/2 $ represent **positive frequencies**, from 0 Hz up to the **Nyquist frequency** (which is $ \frac{\text{rate}}{2} $).
- Indices $ k = N/2+1, \ldots, N-1 $ represent **negative frequencies** to ensure DFT symmetry.

The Nyquist frequency is the theoretical maximum that can be represented without aliasing and is defined as:

$$ f_{\text{Nyquist}} = \frac{\text{rate}}{2} $$

If `rate = 44100` Hz, the Nyquist frequency is 22050 Hz.

## MIDI Management with `mido` and `loopMIDI`

To generate MIDI signals from the human voice, we use the `mido` library for managing MIDI messages and `loopMIDI` to create virtual MIDI ports.

A virtual MIDI port must be created with `loopMIDI` so that the program can send MIDI messages to other applications. Then, we can use `mido` to send MIDI messages to this virtual port.

The virtual port must be named `MIDIVoice` for the program to work correctly.