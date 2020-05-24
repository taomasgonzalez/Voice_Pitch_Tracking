import numpy as np
from scipy.signal import fftconvolve, find_peaks, decimate
from scipy.fftpack import rfft, irfft, ifftshift
from collections import deque
import matplotlib.pyplot as plt
import os


# MEJORAS:
# implementar diff con fft


def sgn(data):
    # determino threshold
    length = len(data)
    firstThird = round(len(data) / 3)
    lastThird = round(len(data) / 1.5)
    auxData1 = data[:firstThird]
    auxData2 = data[lastThird:]
    max1 = np.amax(auxData1)
    max2 = np.amax(auxData2)
    max = min(max1, max2)
    # max = np.amax(data)
    Cl = 0.70 * max
    # aplico transformacion
    data = np.array(data)
    for i in range(0, len(data)):
        if data[i] >= Cl:
            data[i] = 1
        elif data[i] <= -Cl:
            data[i] = -1
        else:
            data[i] = 0
    return data


# Si no encuentra frecuencia fundamental, devuelve fo = 44100
# Cuanto mas grande noteData mejor la aproximacion a la fpitch (aprox 3000 minimo)
def autocorrelationAlgorithm(noteData, fs, clippingStage=True):
    fo = 0
    # selecciono mejor parte de la nota
    # plt.figure(1)
    # plt.plot(noteData)
    # plt.figure(2)
    # plt.plot(noteData)
    # plt.show()
    # autocorrelacion
    x1=np.zeros(len(noteData))
    if clippingStage:
        x1[:-int(fs/500)] = sgn(noteData[:-int(fs/500)])
        x2 = sgn(noteData[::-1])
    else:
        x1[:-int(fs/500)] = noteData[:-int(fs/500)]
        x2 = noteData[::-1]

    correlation = fftconvolve(x1, x2, mode='full')
    correlation = correlation[correlation.size // 2:]

    # busco primer maximo
    max = 0.5* np.amax(correlation)
    peaks, _ = find_peaks(correlation, height=max, distance=21)

    """plt.plot(correlation)
    print(peaks)
    if len(peaks) > 0:
      plt.plot(peaks, correlation[peaks], "x")
    plt.show()"""

    if len(peaks) > 0:
        xMax = peaks[0]
    else:
        xMax = -fs
    # determino frequencia
    fo = fs / xMax
    return fo


def harmonicProductSpectrum(noteData, fs, hNro=7):
    fo = 0
    # aplico ventana
    window = np.hanning(len(noteData))
    noteData = np.multiply(window, noteData)
    # fft de los datos
    fftData = rfft(noteData)
    fftData = abs(fftData[:])
    k = np.arange(len(noteData))
    T = (2 * len(noteData)) / fs
    fftF = k / T
    fftArray = []
    fftArray.append(fftData)
    # downsample for un factor de 2 a hNro
    for i in range(2, hNro + 1):
        auxfft = decimate(fftData, i)
        auxfft = abs(auxfft[:])
        # relleno con ceros para que coincidan en tamaño
        cant = len(fftData) - len(auxfft)
        zeros = np.zeros(cant)
        auxfft = np.concatenate((auxfft, zeros))
        fftArray.append(auxfft)
    # multiplico todas las fft de fftArray
    hpsArray = []
    for i in range(0, len(fftData)):
        auxElement = 1
        for j in range(0, hNro):
            auxElement = auxElement * fftArray[j][i]
        hpsArray.append(auxElement)
    # elimino picos antes de los 20Hz
    index = 0
    while fftF[index] < 20:
        index = index + 1
    for i in range(0, index):
        hpsArray[i] = 0
    # busco frecuencia del maximo de la nueva funcion
    fo = fftF[np.argmax(hpsArray)]
    return fo


def cepstrum(noteData, fs):
    # aplico ventana
    window = np.hanning(len(noteData))
    noteData = np.multiply(window, noteData)
    # calculo cepstrum
    powerSpectrum = np.abs(rfft(noteData)) ** 2
    cepstrum = np.abs(irfft(np.log(powerSpectrum))) ** 2


def fftxcorr(data):
    xp = ifftshift((data - np.average(data)) / np.std(data))
    n, = xp.shape
    xp = np.r_[xp[:n // 2], np.zeros_like(xp), xp[n // 2:]]
    fftArray = rfft(xp)  # aplico fft
    Sxx = np.absolute(fftArray) ** 2  # convierto a densidad espectral
    xcorr = irfft(Sxx)  # antitransformo
    return xcorr


def differenceFunction(data, tauMax, fs, form='fft'):
    diff = np.array([], dtype=np.int64)
    data = np.array(data, dtype=np.int64)
    if form == 'fft':
        r0 = fftxcorr(data)
        #        plt.plot(r0)
        #        plt.show()
        for i in range(1, len(data)):
            rTau = fftxcorr(data[i:len(data)])  # ???
            auxDiff = r0[0] - 2 * r0[i] - rTau[0]
            np.append(diff, auxDiff)
    elif form == 'cumsum':
        t = int(fs * tauMax)
        for i in range(1, t):
            sum = np.int64(0)
            aux = np.int64(0)
            for j in range(0, len(data) - t):
                aux = (data[j] - data[j + i]) ** 2
                sum += aux
            diff = np.append(diff, sum)
    return diff


def YIN(data, fs, tauMax=1 / 40, form='cumsum', th=0.13):

    # let s call len(data) = w
    # we will start by calculating DF = sum(j = 1, w, (x(j) - x(j+tau))^2)
    # DF = sum(j=1, w, x(j) ^ 2) -2 * sum(j=1, w, x(j)*x(j+tau)) + sum(j=1, w, x(j+tau) ^ 2)
    # calculate power and z(tau)
    # where power = sum(j = 1, w, x^2(j))
    # and z(tau) = sum(j = 1, w, x^2(j+w))
    t = int(fs * tauMax)
    power = 0
    sub_powers = list()

    for i in range(1, len(data)):
        power += data[i]**2

    # z(tau) = sum(j = 1, w, x^2(j+w)) = sum(j = tau + 1, w + tau, x^2(j))
    # z(tau) = sum(j = tau + 1, w, x^2(j)) as x(w+1) = 0 and so on...
    # z(tau) = sum(j=1, w, x ^ 2(j))  - sum(j=1, tau, x ^ 2(j))
    # z(tau) = sum(j=1, w, x ^ 2(j)) - sum(j=1, tau, x ^ 2(j))
    # z(tau) = power - sum(j=1, tau, x ^ 2(j))
    # tau can take values from tau = 1 to t
    sub_powers.append(0)       # j = 0, no power just in case.
    sub_powers.append(power - data[1]**2)

    for i in range(2, t):

        if i < len(data):
            sub_powers.append(sub_powers[i-1] - data[i-1]**2)
        else:
            # may be optimized filling the rest with zeroes directly
            sub_powers.append(0)

    correl = fftconvolve(data, data, mode='same')
    # should not add 1 as first value, as we will just be needing diff to claculate cmdf
    diff = np.array([power - 2 * correl[i] + sub_powers[i] for i in range(1, t)], dtype=np.int64)

    cmdf = list()
    cmdf.append(1)
    g_tau = 0

    for i in range(len(diff)):
        g_tau = g_tau + diff[i]
        if g_tau != 0:
            cmdf.append((i + 1) * diff[i] / g_tau)
        else:
            cmdf.append((i + 1) * diff[i] / (10 ** (-10)))

    # find fundamental frequency
    n = 0
    peaks = find_peaks(np.multiply(-1, cmdf), -th)
    if len(peaks[0]) > 0:
        n = peaks[0][0]
        plt.plot(np.multiply(-1, cmdf))
        plt.show()
    if n > 0:
        fo = fs / n
    else:
        fo = fs

    return fo


def freqToPitch(freq):
    pitch = 0
    if freq > 0:
        pitch = round(12 * np.log2(freq / 440) + 69)
    return pitch


def getWavPitch(audio, fs, wLen=4096, wStep=2048, fMin=40):
    """
    Obtiene pitch de un audio
    :param audio: Audio signal (list of float) sig == audio
    :param fs: sampling rate (int) sr == fs
    :param wLen: size of the analysis window (samples)
    :param wStep: size of the lag between two consecutives windows (samples)
    :param fMin: Minimum fundamental frequency that can be detected (hertz) f0_min == fMin
    :returns:
        * pitches: arreglo con los pitches correspondientes a cada tiempo
        * times: tiempos a los cuales refiere la estimacion de pitch (en samples)
    """

    timeScale = range(0, len(audio) - wStep, wStep)  # valores para ventanas para analisis
    times = [t for t in timeScale]  # guardo arreglo con tiempos del audio divido por fs para tener tiempos reales
    frames = [audio[t:t + wLen] for t in timeScale]  # intervalos a los cuales aplicarle el algoritmo de largo wLen

    pitches = []  # donde voy a guardar cada pitch detectado
    max = np.amax(audio)  # maximo valor del audio

    for i, frame in enumerate(frames):
        # LLamo a algoritmo de deteccion
        if np.amax(frame) > 0.09 * max:  # hay nota en el frame
            fAux = autocorrelationAlgorithm(frame, fs, 5000, 'True')
            # fAux = harmonicProductSpectrum(frame,fs,20000)
            # fAux = YIN(frame,fs,1/40,5000)
        else:
            fAux = 0
        if fAux <= (fs / 2):
            pitches.append(fAux)
        else:
            pitches.append(0)
        os.system('cls')
        # print("%s frames of %s finished" % (i+1,len(frames)))
    for i in range(0, len(pitches)):
        pitches[i] = freqToPitch(pitches[i])
    for i in range(1, len(pitches) - 1):
        if pitches[i - 1] == pitches[i + 1] and pitches[i] != pitches[i - 1]:
            pitches[i] = pitches[i - 1]
        elif pitches[i - 1] != pitches[i + 1] and pitches[i] != pitches[i - 1] and pitches[i] != pitches[i + 1]:
            pitches[i] = pitches[i - 1]
    return pitches, times


def is_voiced(window):
    return True


def assign_pitch(data_in, fs, segments, algorithm):
    n_windows = len(segments[:])
    notes_fo = np.zeros(n_windows, dtype=int)
    freqs_fo = np.zeros(n_windows, dtype=int)

    for i in range(0, n_windows):
        if segments[i][0] == 1:
            print("De ",segments[i][0]/fs,"sec a ", segments[i][1]/fs," sec")
            f = algorithm(data_in[segments[i][1]:segments[i][2]], fs)
            freqs_fo[i] = f
            notes_fo[i] = freqToPitch(freqs_fo[i])
        else:
            notes_fo[i] = 0

    return freqs_fo, notes_fo


def translateNotes(notesFo):
    midiKeyBegin = 21

    notesTable = ["A0", "A0#", "B0", "C1", "C1#", "D1", "D1#", "E1", "F1", "F1#", "G1", "G1#",
                  "A1", "A1#", "B1", "C2", "C2#", "D2", "D2#", "E2", "F2", "F2#", "G2", "G2#",
                  "A2", "A2#", "B2", "C3", "C3#", "D3", "D3#", "E3", "F3", "F3#", "G3", "G3#",
                  "A3", "A3#", "B3", "C4", "C4#", "D4", "D4#", "E4", "F4", "F4#", "G4", "G4#",
                  "A4", "A4#", "B4", "C5", "C5#", "D5", "D5#", "E5", "F5", "F5#", "G5", "G5#",
                  "A5", "A5#", "B5", "C6", "C6#", "D6", "D6#", "E6", "F6", "F6#", "G6", "G6#",
                  "A6", "A6#", "B6", "C7", "C7#", "D7", "D7#", "E7", "F7", "F7#", "G7", "G7#",
                  "A7", "A7#", "B7", "C8", "C8#", "D8", "D8#", "E8", "F8", "F8#", "G8", "G8#"]

    Nnotes = len(notesFo)

    notesTranslated = []  # Se crea una lista para las notas traducidas

    for i in range(0, Nnotes):
        if isValidMidiKey(notesFo[i]):
            notesTranslated.append(notesTable[notesFo[i] - midiKeyBegin])
        else:
            notesTranslated.append("unKnownPitch")

    notesTranslatedArray = np.asarray(notesTranslated)

    return notesTranslatedArray


def isValidMidiKey(midiKey):
    ret = False
    if (midiKey < 109 and midiKey > 20):
        ret = True

    return ret
