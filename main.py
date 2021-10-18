# Maybe a synthesizer? Music generator?
import math
from abc import ABC, abstractmethod
import numpy as np
from scipy.io import wavfile

# Dictionary of note frequencies in Hz. Letter is note, - denotes flat, + denotes sharp, number is octave
note_frequencies = {
    'a-0': 25.956547041363212,
    'a-1': 51.913094082726424,
    'a-2': 103.82618816545285,
    'a-3': 207.6523763309057,
    'a-4': 415.3047526618114,
    'a-5': 830.6095053236228,
    'a-6': 1661.2190106472456,
    'a-7': 3322.438021294491,
    'a0': 27.50000364732528,
    'a1': 55.00000729465056,
    'a2': 110.00001458930112,
    'a3': 220.00002917860223,
    'a4': 440.00005835720447,
    'a5': 880.0001167144089,
    'a6': 1760.0002334288179,
    'a7': 3520.0004668576357,
    'a+0': 29.135238959087147,
    'a+1': 58.270477918174294,
    'a+2': 116.54095583634859,
    'a+3': 233.08191167269717,
    'a+4': 466.16382334539435,
    'a+5': 932.3276466907887,
    'a+6': 1864.6552933815774,
    'a+7': 3729.310586763155,
    'b-0': 29.135238959087147,
    'b-1': 58.270477918174294,
    'b-2': 116.54095583634859,
    'b-3': 233.08191167269717,
    'b-4': 466.16382334539435,
    'b-5': 932.3276466907887,
    'b-6': 1864.6552933815774,
    'b-7': 3729.310586763155,
    'b0': 30.867710422491964,
    'b1': 61.73542084498393,
    'b2': 123.47084168996786,
    'b3': 246.9416833799357,
    'b4': 493.8833667598714,
    'b5': 987.7667335197428,
    'b6': 1975.5334670394857,
    'b7': 3951.0669340789714,
    'c0': 16.3516,
    'c1': 32.7032,
    'c2': 65.4064,
    'c3': 130.8128,
    'c4': 261.6256,
    'c5': 523.2512,
    'c6': 1046.5024,
    'c7': 2093.0048,
    'c8': 4186.0096,
    'c+0': 17.323916733725454,
    'c+1': 34.64783346745091,
    'c+2': 69.29566693490182,
    'c+3': 138.59133386980363,
    'c+4': 277.18266773960727,
    'c+5': 554.3653354792145,
    'c+6': 1108.730670958429,
    'c+7': 2217.461341916858,
    'd-0': 17.323916733725454,
    'd-1': 34.64783346745091,
    'd-2': 69.29566693490182,
    'd-3': 138.59133386980363,
    'd-4': 277.18266773960727,
    'd-5': 554.3653354792145,
    'd-6': 1108.730670958429,
    'd-7': 2217.461341916858,
    'd0': 18.354050429135544,
    'd1': 36.70810085827109,
    'd2': 73.41620171654218,
    'd3': 146.83240343308435,
    'd4': 293.6648068661687,
    'd5': 587.3296137323374,
    'd6': 1174.6592274646748,
    'd7': 2349.3184549293496,
    'd+0': 19.445439061678496,
    'd+1': 38.89087812335699,
    'd+2': 77.78175624671398,
    'd+3': 155.56351249342796,
    'd+4': 311.12702498685593,
    'd+5': 622.2540499737119,
    'd+6': 1244.5080999474237,
    'd+7': 2489.0161998948474,
    'e-0': 19.445439061678496,
    'e-1': 38.89087812335699,
    'e-2': 77.78175624671398,
    'e-3': 155.56351249342796,
    'e-4': 311.12702498685593,
    'e-5': 622.2540499737119,
    'e-6': 1244.5080999474237,
    'e-7': 2489.0161998948474,
    'e0': 20.60172503946101,
    'e1': 41.20345007892202,
    'e2': 82.40690015784403,
    'e3': 164.81380031568807,
    'e4': 329.62760063137614,
    'e5': 659.2552012627523,
    'e6': 1318.5104025255046,
    'e7': 2637.020805051009,
    'f0': 21.826767359446734,
    'f1': 43.65353471889347,
    'f2': 87.30706943778694,
    'f3': 174.61413887557387,
    'f4': 349.22827775114774,
    'f5': 698.4565555022955,
    'f6': 1396.913111004591,
    'f7': 2793.826222009182,
    'f+0': 23.124654486499903,
    'f+1': 46.249308972999806,
    'f+2': 92.49861794599961,
    'f+3': 184.99723589199922,
    'f+4': 369.99447178399845,
    'f+5': 739.9889435679969,
    'f+6': 1479.9778871359938,
    'f+7': 2959.9557742719876,
    'g-0': 23.124654486499903,
    'g-1': 46.249308972999806,
    'g-2': 92.49861794599961,
    'g-3': 184.99723589199922,
    'g-4': 369.99447178399845,
    'g-5': 739.9889435679969,
    'g-6': 1479.9778871359938,
    'g-7': 2959.9557742719876,
    'g0': 24.49971799825675,
    'g1': 48.9994359965135,
    'g2': 97.998871993027,
    'g3': 195.997743986054,
    'g4': 391.995487972108,
    'g5': 783.990975944216,
    'g6': 1567.981951888432,
    'g7': 3135.963903776864,
    'g+0': 25.956547041363212,
    'g+1': 51.913094082726424,
    'g+2': 103.82618816545285,
    'g+3': 207.6523763309057,
    'g+4': 415.3047526618114,
    'g+5': 830.6095053236228,
    'g+6': 1661.2190106472456,
    'g+7': 3322.438021294491,
}

# Intervals
# Unison / Diminished 2nd
P1 = d2 = 0
# Minor 2nd / Augmented 1st
m2 = A1 = 1
# Major 2nd / Diminished 3rd
M2 = d3 = 2
# Minor 3rd / Augmented 2nd
m3 = A2 = 3
# Major 3rd / Diminished 4th
M3 = d4 = 4
# Perfect 4th / Augmented 3rd
P4 = A3 = 5
# Augmented 4th / Diminished 5th
A4 = d5 = 6
# Perfect 5th / Diminished 6th
P5 = d6 = 7
# Minor 6th / Augmented 5th
m6 = A5 = 8
# Major 6th / Diminished 7th
M6 = d7 = 9
# Minor 7th / Augmented 6th
m7 = A6 = 10
# Majoe 7th / Diminished 8th
M7 = d8 = 11
# Octave / Augmented 7th
P8 = A7 = 12

# Scales
major_hept = [P1, M2, M3, P4, P5, M6, M7, P8]
nat_minor_hept = [P1, M2, m3, P4, P5, m6, m7, P8]
major_pent = [P1, M2, M3, P4, M6, P8]
minor_pent = [P1, m3, P4, P5, m7, P8]


# Functions to create modes of scales

def ionian(scale):
    return scale


def dorian(scale):
    scale[2] = scale[2] - 1
    scale[3] = scale[3] + 1
    scale[6] = scale[6] - 1
    scale[7] = scale[7] + 1
    return scale


def phrygian(scale):
    for i in range(0, 2):
        scale.insert(0, scale.pop())
    return scale


modes = {
    'ionian': ionian,
    'dorian': dorian,
    'phrygian': phrygian,
}


def set_mode(scale, mode):
    return modes[mode](scale)


print(set_mode(major_hept, 'dorian'))


def get_interval_frequency(root, interval):
    if interval == 0:
        return root
    if interval == 12:
        return root * 2
    else:
        return root * 2 ** (interval / 12.0)


# class Oscillator(ABC):
#     def __init__(self, freq=440.0, phase=0, amp=1.0, sample_rate=44_100, wave_range=(-1, 1)):
#         self._freq = freq
#         self._amp = amp
#         self._phase = phase
#         self._sample_rate = sample_rate
#         self._wave_range = wave_range
#
#         # Properties that will be changed
#         self._f = freq
#         self._a = amp
#         self._p = phase
#
#     @property
#     def init_freq(self):
#         return self._freq
#
#     @property
#     def init_amp(self):
#         return self._amp
#
#     @property
#     def init_phase(self):
#         return self._phase
#
#     @property
#     def freq(self):
#         return self._f
#
#     @freq.setter
#     def freq(self, value):
#         self._f = value
#         self._post_freq_set()
#
#     @property
#     def amp(self):
#         return self._a
#
#     @amp.setter
#     def amp(self, value):
#         self._a = value
#         self._post_amp_set()
#
#     @property
#     def phase(self):
#         return self._p
#
#     @phase.setter
#     def phase(self, value):
#         self._p = value
#         self._post_phase_set()
#
#     def _post_freq_set(self):
#         pass
#
#     def _post_amp_set(self):
#         pass
#
#     def _post_phase_set(self):
#         pass
#
#     @abstractmethod
#     def _initialize_osc(self):
#         pass
#
#     @staticmethod
#     def squish_val(val, min_val=0, max_val=1):
#         return (((val + 1) / 2) * (max_val - min_val)) + min_val
#
#     @abstractmethod
#     def __next__(self):
#         return None
#
#     def __iter__(self):
#         self.freq = self._freq
#         self.phase = self._phase
#         self.amp = self._amp
#         self._initialize_osc()
#         return self
#
#
# class SineOscillator(Oscillator):
#     def _post_freq_set(self):
#         self._step = (2 * math.pi * self._f) / self._sample_rate
#
#     def _post_phase_set(self):
#         self._p = (self._p / 360) * 2 * math.pi
#
#     def _initialize_osc(self):
#         self._i = 0
#
#     def __next__(self):
#         val = math.sin(self._i + self._p)
#         self._i = self._i + self._step
#         if self._wave_range is not (-1, 1):
#             val = self.squish_val(val, *self._wave_range)
#         return val * self._a
#
#
# class SquareOscillator(SineOscillator):
#     def __init__(self, freq=440, phase=0, amp=1, sample_rate=44_100, wave_range=(-1, 1), threshold=0):
#         super().__init__(freq, phase, amp, sample_rate, wave_range)
#         self.threshold = threshold
#
#     def __next__(self):
#         val = math.sin(self._i + self._p)
#         self._i = self._i + self._step
#         if val < self.threshold:
#             val = self._wave_range[0]
#         else:
#             val = self._wave_range[1]
#         return val * self._a
#
#
# class SawtoothOscillator(Oscillator):
#     def _post_freq_set(self):
#         self._period = self._sample_rate / self._f
#         self._post_phase_set
#
#     def _post_phase_set(self):
#         self._p = ((self._p + 90) / 360) * self._period
#
#     def _initialize_osc(self):
#         self._i = 0
#
#     def __next__(self):
#         div = (self._i + self._p) / self._period
#         val = 2 * (div - math.floor(0.5 + div))
#         self._i = self._i + 1
#         if self._wave_range is not (-1, 1):
#             val = self.squish_val(val, *self._wave_range)
#         return val * self._a
#
#
# class TriangleOscillator(SawtoothOscillator):
#     def __next__(self):
#         div = (self._i + self._p) / self._period
#         val = 2 * (div - math.floor(0.5 + div))
#         val = (abs(val) - 0.5) * 2
#         self._i = self._i + 1
#         if self._wave_range is not (-1, 1):
#             val = self.squish_val(val, *self._wave_range)
#         return val * self._a
#
#
# class WaveAdder:
#     def __init__(self, *oscillators):
#         self.oscillators = oscillators
#         self.n = len(oscillators)
#
#     def __iter__(self):
#         [iter(osc) for osc in self.oscillators]
#         return self
#
#     def __next__(self):
#         return sum(next(osc) for osc in self.oscillators) / self.n
#
#
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

#
# gen = WaveAdder(
#     SineOscillator(freq=note_frequencies['c3']),
#     TriangleOscillator(freq=note_frequencies['e3'], amp=0.8),
#     SawtoothOscillator(freq=note_frequencies['g3'], amp=0.6),
#     SquareOscillator(freq=note_frequencies['c2'], amp=0.4),
# )
# iter(gen)
# wav = [next(gen) for _ in range(44100 * 4)]  # 4 Seconds
# wave_to_file(wav, fname="prelude_one.wav")
