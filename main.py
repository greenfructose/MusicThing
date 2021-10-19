# Maybe a synthesizer? Music generator?
import numpy as np
from scipy.io import wavfile
from oscillator import *
from frequencygen import *
from pygame import midi
from midiutil.MidiFile import MIDIFile
from io import BytesIO
from io import StringIO
import pygame
import pygame.mixer
from time import sleep
import random

memFile = BytesIO()
MyMIDI = MIDIFile(1)
track = 0
time = 0.0
channel = 0
pitch = 60
duration = 1
volume = 100
MyMIDI.addTrackName(track, time, "Sample Track")
MyMIDI.addTempo(track, time, 220)


# def wave_to_file(wav, wav2=None, fname="temp.wav", amp=0.1, sample_rate=44100):
#     wav = np.array(wav)
#     wav = np.int16(wav * amp * (2 ** 15 - 1))
#
#     if wav2 is not None:
#         wav2 = np.array(wav2)
#         wav2 = np.int16(wav2 * amp * (2 ** 15 - 1))
#         wav = np.stack([wav, wav2]).T
#
#     wavfile.write(fname, sample_rate, wav)

def freq_list_to_midi_list(freq_list):
    midi_list = []
    for note in freq_list:
        midi_list.append(midi.frequency_to_midi(note))
    return midi_list


chord_freq = get_chord_frequencies(note_frequencies['c4'], dominant_thirteen)
scale_freq = get_scale_frequencies(note_frequencies['d3'], 'mixolydian')
chord_midi = freq_list_to_midi_list(chord_freq)
scale_midi = freq_list_to_midi_list(scale_freq)
# while i < 4:
#     duration = random.randint(1, 2)
#     MyMIDI.addNote(track, channel, chord_midi[i], time, duration, volume)
#     time += duration
#     i += 1
# i = 0
# Groups of 4 ascending
j = 0
for note in scale_midi[:5]:
    # duration = random.randint(1, 2)
    i = 0
    while i < 4:
        MyMIDI.addNote(track, channel, scale_midi[i + j], time, 1, volume)
        time += duration
        i += 1
    j += 1

# Groups of 4 descending
j = len(scale_midi) - 1
for note in scale_midi[3:]:
    i = 0
    while i < 4:
        MyMIDI.addNote(track, channel, scale_midi[j - i], time, 1, volume)
        time += duration
        i += 1
    j -= 1
MyMIDI.writeFile(memFile)
with open('test.midi', 'wb') as output_file:
    MyMIDI.writeFile(output_file)

pygame.init()
pygame.mixer.init()
memFile.seek(0)  # THIS IS CRITICAL, OTHERWISE YOU GET THAT ERROR!
pygame.mixer.music.load(memFile)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    sleep(1)
print("Done!")

# gen = WaveAdder(
#     SineOscillator(freq=chord[0]),
#     TriangleOscillator(freq=chord[1], amp=0.8),
#     SawtoothOscillator(freq=chord[2], amp=0.6),
#     SquareOscillator(freq=chord[3], amp=0.4),
# )
# iter(gen)
# wav = [next(gen) for _ in range(44100 * 4)]  # 4 Seconds
# wave_to_file(wav, fname="prelude_one.wav")
