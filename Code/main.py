from scipy.io import wavfile as wav
import segmentAlgorithms as SDA
import PDA as PDA
import frontend as front
from midiBuilder import MidiBuilder
import GraphSpectrogram as gs
import os

AUDIO_PATH = ".\\Audios\\"


def create_midi(file_path):
    # obtengo el audio monofónico 
    instrument = 1      # Grand Piano

    fs, audio = wav.read(file_path)
    audio_mono = audio
    audio_mono = audio_mono / max(audio_mono)
    midi_filer = MidiBuilder(1000, instrument)

    # get the window intervals to partition the audio
    note_segments = SDA.notes_segmentation(len(audio_mono), fs, window_seconds=0.032, overlap_seconds=0.01)

    # find the pitch of each segment. notes_fo[i] will be -1 if the segment is unvoiced
    freqs_fo, pitches_fo = PDA.assign_pitch(audio_mono, fs, note_segments, PDA.YIN)

    # with open('somefile.txt', 'a') as the_file:
    #     for freq_fo in freqs_fo:
    #         the_file.write(freq_fo + '\n')
    print(freqs_fo)
    # Se genera el archivo midi correspondiente para corroborar que se detectaron las notas correctamente
    # midi_filer.play_notes(note_segments, fs, pitches_fo, file_name)

    # A partir de la frecuencia fundamental de cada nota se averigua el nombre de las mismas
    # notes_name = PDA.translateNotes(pitches_fo)
    # Se muestran gráficamente el resultado
    # front.show_results(notes_name, note_segments, audio_mono)


# front.print_instructions()
# selected_option = input()
# #
# if selected_option == front.CREATE_MIDI:
#     create_midi()
# elif selected_option == front.SPECTROGRAM:
#     f_name = get_wav_file_from_user()
#     gs.GraphSpectrogram(AUDIO_PATH + f_name)
# else:
#     # error
#     print("Opcion invalida\n")

# file_name = "punteoSongPiano"
# create_midi(AUDIO_PATH + file_name + ".wav")
create_midi("lar_F01_sa1" + ".wav")







