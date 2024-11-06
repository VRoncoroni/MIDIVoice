# MIDIVoice

MIDIVoice est un projet open-source qui permet d'analyser, de visualiser et de générer en live des signaux MIDI à partir de la voix humaine.

## Analyse de la récupération de la fréquence fondamentale avec l'auto-corrélation

L'analyse de la fréquence fondamentale (F0) d'un signal audio est une tâche essentielle en traitement du signal. Dans ce projet, nous utilisons l'**auto-corrélation** pour extraire la F0 de la voix humaine.

### 1. Auto-corrélation

L'auto-corrélation est une mesure de la similarité entre un signal et une version décalée de lui-même. Mathématiquement, l'auto-corrélation d'un signal $ x[n] $ est définie comme :

$$ R_x[m] = \sum_{n=0}^{N-1} x[n] \cdot x[n-m] $$

où :

- $ R_x[m] $ est la valeur de l'auto-corrélation pour le décalage $ m $.
- $ x[n] $ est le signal audio.
- $ N $ est le nombre total d'échantillons dans le signal.

### 2. Détection de la fréquence fondamentale

Pour extraire la fréquence fondamentale $ f_0 $ d'un signal audio, on utilise l'auto-corrélation pour trouver le premier pic significatif de l'auto-corrélation. Ce pic correspond à la période du signal, qui est inversement proportionnelle à la fréquence fondamentale :

$$ f_0 = \frac{rate}{m} $$

où :

- $ \text{rate} $ est le taux d'échantillonnage du signal audio.
- $ m $ est l'indice du premier pic significatif de l'auto-corrélation.

### 3. Limitations de l'auto-corrélation

L'auto-corrélation est une méthode simple et efficace pour extraire la fréquence fondamentale d'un signal audio. Cependant, elle peut être sensible à certains artefacts, tels que le bruit, les harmoniques et les formants vocaux. Pour améliorer la robustesse de l'analyse, on peut utiliser des techniques de prétraitement et de post-traitement, comme le lissage, la suppression des harmoniques et la détection de la voix.

Par exemple nous avons utiliser un filtre passe-haut pour supprimer les fréquences basses et les harmoniques qui peuvent interférer avec la détection de la fréquence fondamentale.

## Analyse de la Transformée de Fourier avec NumPy

Dans cette section, nous expliquons en détail l'utilisation des fonctions `np.fft.fft()` et `np.fft.fftfreq()` pour l'analyse fréquentielle d'un signal audio.

### 1. Transformée de Fourier discrète avec `np.fft.fft`

La **Transformée de Fourier discrète (DFT)** décompose un signal temporel $ x[n] $ en ses composantes fréquentielles. Mathématiquement, la DFT de $ x[n] $, pour $ n = 0, 1, \ldots, N-1 $, est définie comme :

$$ X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-j \frac{2 \pi}{N} k n} $$

où :
- $ X[k] $ est la composante fréquentielle pour l'indice $ k $ (la fréquence associée).
- $ N $ est le nombre total d'échantillons dans le signal.
- $ j $ est l'unité imaginaire ($ j^2 = -1 $).
- $ e^{-j \frac{2 \pi}{N} k n} $ est une oscillation complexe qui représente chaque fréquence dans le signal.

En Python, cette équation est calculée par `np.fft.fft(audio_signal)`, qui retourne un tableau $ X[k] $ (appelé `fft_spectrum` dans le code).

#### Interprétation des valeurs dans `fft_spectrum`

Le résultat `fft_spectrum` est un tableau complexe où chaque élément $ X[k] $ contient :
- La **magnitude** $ |X[k]| $ : l'amplitude de la fréquence correspondant à l'indice $ k $.
- La **phase** $ \arg(X[k]) $ : le décalage de phase de cette fréquence.

Pour extraire l'amplitude de chaque fréquence, on utilise :
$$ 	A = |X[k]| = \sqrt{\Re(X[k])^2 + \Im(X[k])^2} $$
où $ \Re(X[k]) $ et $ \Im(X[k]) $ représentent respectivement la partie réelle et la partie imaginaire de $ X[k] $.

### 2. Fréquences correspondantes avec `np.fft.fftfreq`

Pour savoir quelles fréquences $ f[k] $ sont représentées par chaque indice $ k $ dans `fft_spectrum`, on utilise la fonction `np.fft.fftfreq()`. Cette fonction calcule les fréquences réelles en Hertz (Hz) correspondant aux indices $ k $.

La fréquence associée à chaque indice $ k $ est donnée par :

$$ f[k] = \frac{k \cdot 	{rate}}{N} $$

où :
- $ f[k] $ est la fréquence associée à l'indice $ k $,
- $ \text{rate} $ est le taux d'échantillonnage (par exemple, 44100 Hz),
- $ N $ est la taille du signal (nombre d'échantillons dans `audio_signal`).

#### Gamme de fréquences obtenues

- Les indices $ k = 0, 1, \ldots, N/2 $ représentent les **fréquences positives**, de 0 Hz jusqu'à la **fréquence de Nyquist** (qui est $ \frac{\text{rate}}{2} $).
- Les indices $ k = N/2+1, \ldots, N-1 $ représentent les **fréquences négatives** pour assurer la symétrie de la DFT.

La fréquence de Nyquist est le maximum théorique que l’on peut représenter sans aliasing et est définie par :

$$ f_{\text{Nyquist}} = \frac{\text{rate}}{2} $$

Dans le cas où `rate = 44100` Hz, la fréquence de Nyquist est de 22050 Hz.

## Gestion MIDI avec `mido` et `loopMIDI`

Pour générer des signaux MIDI à partir de la voix humaine, nous utilisons la bibliothèque `mido` pour la gestion des messages MIDI et `loopMIDI` pour créer des ports MIDI virtuels.

Il faut créer un port MIDI virtuel avec `loopMIDI` pour que le programme puisse envoyer des messages MIDI à d'autres applications. Ensuite, on peut utiliser `mido` pour envoyer des messages MIDI à ce port virtuel.

Le port virtuel doit être nommé `MIDIVoice` pour que le programme fonctionne correctement.