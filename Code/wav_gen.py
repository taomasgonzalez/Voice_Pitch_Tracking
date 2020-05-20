import wave
import math
import struct


class WaveManagement:
    number_of_bytes_codification = 2        # number of bytes a frame has

    def __init__(self):
        self.opened_file = None

    # https://soledadpenades.com/posts/2009/fastest-way-to-generate-wav-files-in-python-using-the-wave-module/
    def generate_wav(self, finished: bool, data: list, n_channels: int = 1, sample_width=2, frame_rate=44100, file_name='NEW_WAV.wav'):
        """generate_wav generates a new .wav file based on the input data.
    #The amplitude of each data sample should be a float belonging to the interval [-2^15-1,2^15-1]"""
        if self.opened_file is None:
            self.opened_file = wave.open(file_name, 'wb')
            self.opened_file.setparams((n_channels, sample_width, frame_rate, len(data), 'NONE', 'not compressed'))
        translated_data = []

        # https://docs.python.org/2/library/struct.html#struct-format-strings
        # h : 2 bytes -> 2^15-1 =32767, maximum amplitude
        # i : 4 bytes
        for d in data:
            translated_data.append(struct.pack('h', int(d)))

        self.opened_file.writeframes(b''.join(translated_data))
        if finished:
            self.opened_file.close()
            self.opened_file = None

