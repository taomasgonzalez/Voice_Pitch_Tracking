from wav_gen import WaveManagement
from scipy.io import wavfile as wav
import segmentAlgorithms as SDA
import PDA as PDA

wav_man = WaveManagement()
# SAMPLES_PATH = ".\\SampleChords"
SAMPLES_PATH = ".\\SampleNotes"


def trim_wavs(data, note_segments, fs, notes_name):
    repeated_names = []
    for i in range(len(note_segments)):
        aux = data[note_segments[i][0]-10000:note_segments[i][1]+20000]
        name = notes_name[i]
        while name in repeated_names:
            name = name + "a"
        repeated_names.append(name)
        wav_man.generate_wav(finished=True, data=aux, n_channels=1, sample_width=2,
                             frame_rate=fs, file_name=SAMPLES_PATH + "\\" + name+'.wav')


fileName = "sample_chords"
# fileName = "sample_notes"

filePath = fileName + ".wav"

fs, audio = wav.read(filePath)
audioMono = audio

# Se detectan los intervalos de tiempo donde predominan las notas musicales
noteSegments = SDA.notesSegmentation(audioMono, fs, SDA.HFC)

# Se averigua el pitch de las notas de cada intervalo hallado
notesFo = PDA.assignPitch(audioMono, fs, noteSegments, PDA.autocorrelationAlgorithm)

# A partir de la frecuencia fundamental de cada nota se averigua el nombre de las mismas
notesName = PDA.translateNotes(notesFo)

# notesName = []
# for i in range(len(noteSegments)):
#     notesName.append('Chord' + str(i))

trim_wavs(audioMono, noteSegments, fs, notesName)
