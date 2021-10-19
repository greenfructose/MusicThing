# Maybe a synthesizer? Music generator?
import numpy as np
from scipy.io import wavfile
from oscillator import *
from frequencygen import *
from pygame import midi
from midiutil.MidiFile import MIDIFile
from io import BytesIO
from io import StringIO

memFile = BytesIO()
MyMIDI = MIDIFile(1)
track = 0
time = 0
channel = 0
pitch = 60
duration = 1
volume = 100
MyMIDI.addTrackName(track, time, "Sample Track")
MyMIDI.addTempo(track, time, 120)

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


chord_freq = get_chord_frequencies(note_frequencies['c5'], major_seventh)
chord_midi = []
for note in chord_freq:
    chord_midi.append(midi.frequency_to_midi(note))

for note in chord_midi:
    MyMIDI.addNote(track, channel, note, time, duration, volume)
    time += duration
MyMIDI.writeFile(memFile)
# with open('test.midi', 'wb') as output_file:
#     MyMIDI.writeFile(output_file)


# gen = WaveAdder(
#     SineOscillator(freq=chord[0]),
#     TriangleOscillator(freq=chord[1], amp=0.8),
#     SawtoothOscillator(freq=chord[2], amp=0.6),
#     SquareOscillator(freq=chord[3], amp=0.4),
# )
# iter(gen)
# wav = [next(gen) for _ in range(44100 * 4)]  # 4 Seconds
# wave_to_file(wav, fname="prelude_one.wav")
