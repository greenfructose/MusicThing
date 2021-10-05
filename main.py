# Maybe a synthesizer? Music generator?
import math
from abc import ABC, abstractmethod
import numpy as np
from scipy.io import wavfile

tone = {
    0: 1.0,
    1: 2.0 ** (1.0 / 12.0),
    2: 2.0 ** (2.0 / 12.0),
    3: 2.0 ** (3.0 / 12.0),
    4: 2.0 ** (4.0 / 12.0),
    5: 2.0 ** (5.0 / 12.0),
    6: 2.0 ** (6.0 / 12.0),
    7: 2.0 ** (7.0 / 12.0),
    8: 2.0 ** (8.0 / 12.0),
    9: 2.0 ** (9.0 / 12.0),
    10: 2.0 ** (10.0 / 12.0),
    11: 2.0 ** (11.0 / 12.0),
    12: 2.0
}

P1 = d2 = tone[0]
m2 = A1 = tone[1]
M2 = d3 = tone[2]
m3 = A2 = tone[3]
M3 = d4 = tone[4]
P4 = A3 = tone[5]
A4 = d5 = tone[6]
P5 = d6 = tone[7]
m6 = A5 = tone[8]
M6 = d7 = tone[9]
m7 = A6 = tone[10]
M7 = d8 = tone[11]
P8 = A7 = tone[12]

major_hept = [0, 2, 4, 5, 7, 9, 11, 12]
nat_minor_hept = [0, 2, 3, 5, 7, 8, 10, 12]
major_pent = [0, 2, 4, 5, 9, 12]
minor_pent = [0, 3, 5, 7, 10, 12]


class Oscillator(ABC):
    def __init__(self, freq=440.0, phase=0, amp=1.0, sample_rate=44_100, wave_range=(-1, 1)):
        self._freq = freq
        self._amp = amp
        self._phase = phase
        self._sample_rate = sample_rate
        self._wave_range = wave_range

        # Properties that will be changed
        self._f = freq
        self._a = amp
        self._p = phase

    @property
    def init_freq(self):
        return self._freq

    @property
    def init_amp(self):
        return self._amp

    @property
    def init_phase(self):
        return self._phase

    @property
    def freq(self):
        return self._f

    @freq.setter
    def freq(self, value):
        self._f = value
        self._post_freq_set()

    @property
    def amp(self):
        return self._a

    @amp.setter
    def amp(self, value):
        self._a = value
        self._post_amp_set()

    @property
    def phase(self):
        return self._p

    @phase.setter
    def phase(self, value):
        self._p = value
        self._post_phase_set()

    def _post_freq_set(self):
        pass

    def _post_amp_set(self):
        pass

    def _post_phase_set(self):
        pass

    @abstractmethod
    def _initialize_osc(self):
        pass

    @staticmethod
    def squish_val(val, min_val=0, max_val=1):
        return (((val + 1) / 2) * (max_val - min_val)) + min_val

    @abstractmethod
    def __next__(self):
        return None

    def __iter__(self):
        self.freq = self._freq
        self.phase = self._phase
        self.amp = self._amp
        self._initialize_osc()
        return self


class SineOscillator(Oscillator):
    def _post_freq_set(self):
        self._step = (2 * math.pi * self._f) / self._sample_rate

    def _post_phase_set(self):
        self._p = (self._p / 360) * 2 * math.pi

    def _initialize_osc(self):
        self._i = 0

    def __next__(self):
        val = math.sin(self._i + self._p)
        self._i = self._i + self._step
        if self._wave_range is not (-1, 1):
            val = self.squish_val(val, *self._wave_range)
        return val * self._a


class SquareOscillator(SineOscillator):
    def __init__(self, freq=440, phase=0, amp=1, sample_rate=44_100, wave_range=(-1, 1), threshold=0):
        super().__init__(freq, phase, amp, sample_rate, wave_range)
        self.threshold = threshold

    def __next__(self):
        val = math.sin(self._i + self._p)
        self._i = self._i + self._step
        if val < self.threshold:
            val = self._wave_range[0]
        else:
            val = self._wave_range[1]
        return val * self._a


class SawtoothOscillator(Oscillator):
    def _post_freq_set(self):
        self._period = self._sample_rate / self._f
        self._post_phase_set

    def _post_phase_set(self):
        self._p = ((self._p + 90) / 360) * self._period

    def _initialize_osc(self):
        self._i = 0

    def __next__(self):
        div = (self._i + self._p) / self._period
        val = 2 * (div - math.floor(0.5 + div))
        self._i = self._i + 1
        if self._wave_range is not (-1, 1):
            val = self.squish_val(val, *self._wave_range)
        return val * self._a


class TriangleOscillator(SawtoothOscillator):
    def __next__(self):
        div = (self._i + self._p) / self._period
        val = 2 * (div - math.floor(0.5 + div))
        val = (abs(val) - 0.5) * 2
        self._i = self._i + 1
        if self._wave_range is not (-1, 1):
            val = self.squish_val(val, *self._wave_range)
        return val * self._a


class WaveAdder:
    def __init__(self, *oscillators):
        self.oscillators = oscillators
        self.n = len(oscillators)

    def __iter__(self):
        [iter(osc) for osc in self.oscillators]
        return self

    def __next__(self):
        return sum(next(osc) for osc in self.oscillators) / self.n


def wave_to_file(wav, wav2=None, fname="temp.wav", amp=0.1, sample_rate=44100):
    wav = np.array(wav)
    wav = np.int16(wav * amp * (2 ** 15 - 1))

    if wav2 is not None:
        wav2 = np.array(wav2)
        wav2 = np.int16(wav2 * amp * (2 ** 15 - 1))
        wav = np.stack([wav, wav2]).T

    wavfile.write(fname, sample_rate, wav)


gen = WaveAdder(
    SineOscillator(freq=note_frequencies['c3']),
    TriangleOscillator(freq=note_frequencies['e3'], amp=0.8),
    SawtoothOscillator(freq=note_frequencies['g3'], amp=0.6),
    SquareOscillator(freq=note_frequencies['c2'], amp=0.4),
)
iter(gen)
wav = [next(gen) for _ in range(44100 * 4)]  # 4 Seconds
wave_to_file(wav, fname="prelude_one.wav")
