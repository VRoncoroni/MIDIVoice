
# Analyse de la Transformée de Fourier avec NumPy

Dans cette section, nous expliquons en détail l'utilisation des fonctions `np.fft.fft()` et `np.fft.fftfreq()` pour l'analyse fréquentielle d'un signal audio.

## 1. Transformée de Fourier discrète avec `np.fft.fft`

La **Transformée de Fourier discrète (DFT)** décompose un signal temporel $ x[n] $ en ses composantes fréquentielles. Mathématiquement, la DFT de $ x[n] $, pour $ n = 0, 1, \ldots, N-1 $, est définie comme :

$$ X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-j \frac{2 \pi}{N} k n} $$

où :
- $ X[k] $ est la composante fréquentielle pour l'indice $ k $ (la fréquence associée).
- $ N $ est le nombre total d'échantillons dans le signal.
- $ j $ est l'unité imaginaire ($ j^2 = -1 $).
- $ e^{-j \frac{2 \pi}{N} k n} $ est une oscillation complexe qui représente chaque fréquence dans le signal.

En Python, cette équation est calculée par `np.fft.fft(audio_signal)`, qui retourne un tableau $ X[k] $ (appelé `fft_spectrum` dans le code).

### Interprétation des valeurs dans `fft_spectrum`

Le résultat `fft_spectrum` est un tableau complexe où chaque élément $ X[k] $ contient :
- La **magnitude** $ |X[k]| $ : l'amplitude de la fréquence correspondant à l'indice $ k $.
- La **phase** $ \arg(X[k]) $ : le décalage de phase de cette fréquence.

Pour extraire l'amplitude de chaque fréquence, on utilise :
$$ 	A = |X[k]| = \sqrt{\Re(X[k])^2 + \Im(X[k])^2} $$
où $ \Re(X[k]) $ et $ \Im(X[k]) $ représentent respectivement la partie réelle et la partie imaginaire de $ X[k] $.

## 2. Fréquences correspondantes avec `np.fft.fftfreq`

Pour savoir quelles fréquences $ f[k] $ sont représentées par chaque indice $ k $ dans `fft_spectrum`, on utilise la fonction `np.fft.fftfreq()`. Cette fonction calcule les fréquences réelles en Hertz (Hz) correspondant aux indices $ k $.

La fréquence associée à chaque indice $ k $ est donnée par :

$$ f[k] = \frac{k \cdot 	{rate}}{N} $$

où :
- $ f[k] $ est la fréquence associée à l'indice $ k $,
- $ \text{rate} $ est le taux d'échantillonnage (par exemple, 44100 Hz),
- $ N $ est la taille du signal (nombre d'échantillons dans `audio_signal`).

### Gamme de fréquences obtenues

- Les indices $ k = 0, 1, \ldots, N/2 $ représentent les **fréquences positives**, de 0 Hz jusqu'à la **fréquence de Nyquist** (qui est $ \frac{\text{rate}}{2} $).
- Les indices $ k = N/2+1, \ldots, N-1 $ représentent les **fréquences négatives** pour assurer la symétrie de la DFT.

La fréquence de Nyquist est le maximum théorique que l’on peut représenter sans aliasing et est définie par :

$$ f_{\text{Nyquist}} = \frac{\text{rate}}{2} $$

Dans le cas où `rate = 44100` Hz, la fréquence de Nyquist est de 22050 Hz.
