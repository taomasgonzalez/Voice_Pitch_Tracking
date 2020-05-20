from scipy.io import wavfile as wav
import segmentAlgorithms as SDA
import PDA as PDA
import frontend as front
from midiBuilder import MidiBuilder
import GraphSpectrogram as gs
import os

AUDIO_PATH = ".\\Audios\\"


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# Valida que un string recibido sea un numero natural
def is_valid_number(arg):
    if isfloat(arg):    # valido el argumento
        arg_f = float(arg)
        if arg_f <= 0:
            return "El numero ingresado debe ser positivo\n"
        elif arg_f == float("inf") or arg_f >= 10e9:
            return "El numero ingresado debe tener un valor finito\n"

    else:
        return "Error de sintaxis\n"

    return "Ok"     # El numero parece ser valido


def get_wav_file_from_user():
    valid = False
    i = 0
    wav_dict = dict()
    for file in os.listdir(AUDIO_PATH):
        i += 1
        if file.endswith(".wav"):
            print(str(i)+')'+file)
            wav_dict[i] = file
    while not valid:
        num_str = input("Por favor seleccione el .wav deseado ingresando el numero previo al nombre\n")
        result_str = is_valid_number(num_str)
        if result_str == 'Ok':
            num = int(num_str)
            if num in wav_dict:
                valid = True
                file_name = wav_dict[num]
                return file_name
        else:
            valid = False
            print(result_str)


def create_midi():
    # obtengo el audio monofónico 
    instrument = 1      # Grand Piano -- despues habria que agregar un diccionario si hace falta
    file_name = "punteoSongPiano"
    file_path = AUDIO_PATH + file_name + ".wav"

    fs, audio = wav.read(file_path)
    audio_mono = audio[:, 1]

    midi_filer = MidiBuilder(1000, instrument)

    # get the window intervals to partition the audio
    note_segments = SDA.notesSegmentation(audio_mono, fs, SDA.HFC)

    # find the pitch of each segment. notes_fo[i] will be -1 if the segment is unvoiced
    pitches_fo = PDA.assign_pitch(audio_mono, fs, note_segments, PDA.autocorrelationAlgorithm)

    # Se genera el archivo midi correspondiente para corroborar que se detectaron las notas correctamente
    midi_filer.play_notes(note_segments, fs, pitches_fo, file_name)

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

create_midi()








