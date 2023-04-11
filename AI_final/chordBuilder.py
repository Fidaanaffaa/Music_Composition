NAME = 0
MINOR_INDICATOR = -1
DICT = {'$': 0, 'A': 1, 'b': 2, 'B': 3, 'C': 4, 'd': 5, 'D': 6, 'e': 7, 'E': 8, 'F': 9, 'g': 10, 'G': 11,
        'a': 12}
INVERTED_DICT = {0 : '$', 1: 'A', 2: 'b', 3: 'B', 4: 'C', 5: 'd', 6: 'D', 7: 'e', 8: 'E', 9: 'F', 10: 'g', 11: 'G',
        12: 'a'}
MINOR_THIRD = 3
MAJOR_THIRD = 4
FIFTH = 7

class ChordBuilder:
    @staticmethod
    def build_chords(chord_progression):
        chord_list = list()
        for chord_name in chord_progression:
            if chord_name[MINOR_INDICATOR] == 'm':
                note = chord_name[NAME]
                root_ind = DICT[note]
                if DICT[note] < 3:
                    minor_key = (DICT[note] + 12 + MINOR_THIRD) % 12
                    fifth_key = (DICT[note] + 12 + FIFTH) % 12
                else:
                    minor_key = (DICT[note] + MINOR_THIRD) % 12
                    fifth_key = (DICT[note] + FIFTH) % 12
                chord_list.append([chord_name, INVERTED_DICT[root_ind], INVERTED_DICT[minor_key], INVERTED_DICT[fifth_key],
                                               '$'])
            else:
                note = chord_name[NAME]
                root_ind = DICT[note]
                if DICT[note] < 3:
                    major_key = (DICT[note] + 12 + MAJOR_THIRD) % 12
                    fifth_key = (DICT[note] + 12 + FIFTH) % 12
                else:
                    major_key = (DICT[note] + MAJOR_THIRD) % 12
                    fifth_key = (DICT[note] + FIFTH) % 12
                chord_list.append([chord_name, INVERTED_DICT[root_ind], INVERTED_DICT[major_key], INVERTED_DICT[fifth_key],
                                               '$'])
        return chord_list