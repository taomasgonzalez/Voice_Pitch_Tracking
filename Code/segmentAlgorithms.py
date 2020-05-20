#HFC algorithm

import numpy as np
import math
import scipy.signal as signal 


def notesSegmentation(dataIn, fs, algorithm):
    f, timeRes, thOn, thOff, softOrder = algorithm(dataIn, fs)
    detectionFunction = f
    soft(f, softOrder) #orden 4 de decimación e interpolación
    adaptativeThresh = calculateThreshold(detectionFunction, timeRes, thOn)
    onsets = onsetDetection(detectionFunction, thOn)
    offsets = offsetDetection(detectionFunction, onsets, thOff)
    segmentsOnOff = generateSegments(onsets, offsets, timeRes, fs)

    ################
    
    # x1 = np.linspace(0, len(dataIn)*fs, len(dataIn))
    # x2 = np.linspace(0, len(f)*timeRes, len(f))
    # x3 = np.linspace(0, len(detectionFunction)*timeRes, len(detectionFunction))
    # plt.figure()

    # plt.subplot(311)
    # plt.title("Señal Original de Audio")
    # plt.plot(x1, dataIn)
    # plt.axis('off')



    # plt.subplot(312)
    # plt.title("Señal de Detección")
    # plt.plot(x2, f)
    # plt.axis('off')

    # plt.subplot(313)
    # plt.title("Señal de Detección Suavizada - Onsets y Offsets")
    # plt.xlabel("tiempo (segundos)")
    # plt.ylabel("Magnitud")
    # plt.plot(x3, detectionFunction)
    # plt.plot(onsets*timeRes, detectionFunction[onsets], 'x')
    # plt.plot(offsets*timeRes, detectionFunction[offsets], 'o')

    #################

    return segmentsOnOff

#FUNCIONES DE DETECCIÓN

def HFC(bufferIn,f_s=44100):
    
    k, n, Snn = signal.spectrogram(bufferIn, f_s, nperseg=1024, nfft = 1024)
    Nbins = len(k)
    Ntimes = len(n)
    timeRes = n[-1]/Ntimes
    En = np.zeros(Ntimes)

    for i in range(0, Ntimes-1):
        for j in range(0, Nbins-1):
            En[i] += (j*Snn[j, i])
        En[i] /= Nbins

    thOn = 2500
    thOff = 600
    softOrder = 2

    return En, timeRes, thOn, thOff, softOrder


def spectralDiff(bufferIn, f_s):
    k, n, Snn = signal.spectrogram(bufferIn, f_s)
    Nbins = len(k)
    Ntimes = len(n)
    timeRes = n[-1]/Ntimes
    SD = np.zeros(Ntimes)
    SD[0] = 0

    for i in range(1, Ntimes-1):
        for j in range(0, Nbins-1):
            SD[i] += ((Hx(Snn[j, i] - Snn[j, i-1]))**2)

    thOn = 1000
    thOff = 20
    softOrder = 2
    return SD, timeRes, thOn, thOff, softOrder

def CDC(bufferIn,f_s=44100):
    
    return a, b

#FUNCIONES DE DETECCIÓN DE ONSET

def onsetDetection(detectionFunction, thOn):
    peaks, _ = signal.find_peaks(detectionFunction, height = 0, threshold= 10, distance = 13)
    NfalsePositives = 0
    thresholdOn = thOn
    #cuento la cantidad de falsos positivos
    for i in range(0, len(peaks)):
        if detectionFunction[peaks[i]] < thresholdOn:
            NfalsePositives += 1

    #creo vector que NO tenga en cuenta los falsos positivos
    peaksAux = np.zeros(len(peaks)-NfalsePositives, dtype=int)

    #lleno el nuevo vector con los picos válidos
    
    j = 0
    for i in range(0, len(peaks)):
        if detectionFunction[(peaks[i])] > thresholdOn:
            peaksAux[j] = peaks[i]
            j += 1  

    return peaksAux

#FUNCIONES DE DETECCIÓN DE OFFSET

def offsetDetection(detectionFunction, onsets, thOff):
    offsets = np.zeros(len(onsets), dtype = int)
    thresholdOff = thOff
    isOffsetDetected = False #genero flag para saber si se detecta offset o llega una nota antes de que la anterior se termine

    for i in range(0, len(onsets)): #utilizo todos los onsets para hallar los offsets

        isOffsetDetected = False #reseteo flag

        if i < (len(onsets)-1): #si no estoy en el ultimo pico (se toma el ultimo pico como un caso particular)
            current = onsets[i]  #marco desde que pico comenzar a buscar
            limit = onsets[i+1]  #como mucho busco hasta el proximo pico

        else: #estoy en el ulitmo pico
            current = onsets[i]
            limit = len(detectionFunction)

        while( (current < limit) and (not isOffsetDetected) ):  #incio la busqueda
        
            if detectionFunction[current] < thresholdOff:  #se logra hallar un offset
                isOffsetDetected = True

            current += 1
        
        #al salir del ciclo while completo el offset
        offsets[i] = current

    return offsets

#FUNCIONES QUE UNEN EL ONSET Y EL OFFSET (FORMAN EL SEGMENTO)

def generateSegments(onsets, offsets, timeRes, fs):
    Nnotes = len(onsets)          #se supone que el tamaño del vector de onsets y el vector de offsets es el mismo y es igual al numero de notas
    segments = np.zeros((Nnotes,2), dtype = int) #matriz, cada fila represente una nota, la primer columna representa el onset y la siguiente el offset

    for i in range(0, Nnotes):
        segments[i, 0] = (int)(onsets[i] * timeRes * fs)
        segments[i, 1] = (int)(offsets[i] * timeRes * fs)
    

    return segments


#FUNCIONES ÚTILES

def Hx(x):
    return (x + abs(x))/2

    
def soft(dataIn, nOrden):
    if (nOrden % 2 == 0):
        dataDown = signal.decimate(dataIn, nOrden)
        dataUp = signal.resample(dataDown, len(dataDown)*nOrden)
        return dataUp
    else:
        return dataIn

def calculateThreshold(detectionFunction, timeRes, thInit):
    thAdaptative = thInit
    return thAdaptative

    
    
    


