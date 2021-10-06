import pprint


def get_frequencies(start, end):
    notes = ['c', 'c+/d-', 'd', 'd+/e-', 'e', 'f', 'f+/g-', 'g', 'g+/a-', 'a', 'a+/b-', 'b']
    current_frequency = start
    octave_count = 0
    frequency_dict = {}
    while current_frequency < end:
        # print(str(current_frequency) + f' {notes[0]}{octave_count}')
        frequency_dict[f'{notes[0]}{octave_count}'] = current_frequency
        for i in range(1, 12):
            # print(str(current_frequency * 2 ** (i / 12.0)) + f' {notes[i]}{octave_count}')
            frequency_dict[f'{notes[i]}{octave_count}'] = current_frequency * 2 ** (i / 12.0)
        current_frequency *= 2
        octave_count += 1
    # print(str(current_frequency) + f' {notes[0]}{octave_count}')
    frequency_dict[f'{notes[0]}{octave_count}'] = current_frequency
    return frequency_dict


pprint.pprint(get_frequencies(16.35160, 4186.009))
