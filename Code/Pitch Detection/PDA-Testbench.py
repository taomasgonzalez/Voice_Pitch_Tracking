from pathlib import Path
import numpy as np
from scipy.io import wavfile
import PDA
import matplotlib.pyplot as plt

files = ["saxophone_B3.wav","guitar_G3.wav","trumpet_A4.wav","violin_A4.wav",
         "cello_As2.wav","flute_G5.wav","oboe_E5.wav","banjo_E6.wav","bass-clarinet_F5.wav",
        "tuba_A1.wav","note.wav","pianoChord_C4.wav"]
freq = [247,195,440,440,117,784,659,1319,698,55,370,262]

print("Algorithm Testbench:")
print(" ")

for j in range(0,len(files)):
    fileNameOrigin = files[j]
    data_folder = Path("all-samples/")
    file_to_open = data_folder / fileNameOrigin
    fs, noteData = wavfile.read(file_to_open)
    if type(noteData[0]) == type(np.array([0,0])):
            # convierto en mono
            auxData = []
            for i in range(0,len(noteData)):
                auxData.append(noteData[i][0])
            noteData = auxData
    print("Instrument: %s" % (files[j][:-4]))
    print("Real: ~%s Hz - %s MIDI" % (freq[j],PDA.freqToPitch(freq[j])))
    ACAfreq1 = PDA.autocorrelationAlgorithm(noteData,fs,3000,False)
    ACAfreq2 = PDA.autocorrelationAlgorithm(noteData,fs,3000,True)
    #HPSfreq = PDA.harmonicProductSpectrum(noteData,fs)
    #YINfreq = PDA.YIN(noteData,fs)
    #PDA.cepstrum(noteData,fs,100000)
    print("Autocorrelation: %s Hz - %s MIDI" % (round(ACAfreq1),PDA.freqToPitch(ACAfreq1)))
    print("Clipped Autocorrelation: %s Hz - %s MIDI" % (round(ACAfreq2),PDA.freqToPitch(ACAfreq2)))
    #print("HPS: %s Hz - %s MIDI" % (round(HPSfreq),PDA.freqToPitch(HPSfreq)))
    #print("YIN: %s Hz - %s MIDI" % (round(YINfreq),PDA.freqToPitch(YINfreq)))
    print(" ")

#print("Wav Pitch Testbench:")
#fileNameOrigin = "4notes.wav"
#data_folder = Path("all-samples/")
#file_to_open = data_folder / fileNameOrigin
#fs, noteData = wavfile.read(file_to_open)
#if type(noteData[0]) == type(np.array([0,0])): # convierto en mono
#    auxData = []
#    for i in range(0,len(noteData)):
#        auxData.append(noteData[i][0])
#    noteData = auxData
#pitches, times = PDA.getWavPitch(noteData,fs)
#plt.figure("Pitch")
#plt.plot(np.multiply(noteData,0.005))
#plt.plot(times,pitches,'ro')
#plt.show()
