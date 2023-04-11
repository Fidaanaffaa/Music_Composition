
from CSP.CSP_Agent import *
import Parse
from QLearningAgent import chord
from QLearningAgent import musicGUI
import chordBuilder
NAME = 0
MINOR_INDICATOR = -1
DICT = {'$': 0, 'A': 1, 'b': 2, 'B': 3, 'C': 4, 'd': 5, 'D': 6, 'e': 7, 'E': 8, 'F': 9, 'g': 10, 'G': 11,
        'a': 12}
INVERTED_DICT = {0 : '$', 1: 'A', 2: 'b', 3: 'B', 4: 'C', 5: 'd', 6: 'D', 7: 'e', 8: 'E', 9: 'F', 10: 'g', 11: 'G',
        12: 'a'}
MINOR_THIRD = 3
MAJOR_THIRD = 4
FIFTH = 7

def makeOutputCsp(agent, filename):
    result = agent.getSolution()
    root_chords = agent.getChordInformation()

    f = open(filename, "w")
    if result is False:
        f.write("False")
        f.close()
        return

    bar_counter = 0
    for bar in result:
        bit_counter = 0
        for bit in bar:
            f.write(root_chords[bar_counter])
            f.write("/")
            f.write(bit)
            if bit_counter != 3:
                f.write(",")
            bit_counter += 1
        f.write("\n")
        bar_counter += 1
    f.close()


def check_input(input):
    check = input.split(',')
    if len(check) != 4:
        return False
    for chord in check:
        if len(chord) > 2:
            return False
        elif len(chord) == 2:
            if chord[-1] != 'm':
                return False
        elif len(chord) == 1:
            if chord[0] not in DICT.keys():
                return False
            if chord[0] == '$':
                return False
        elif len(chord) == 0:
            return False
    return True

def checkQLearningInput(epsilon, learning_rate, discount, subdivisions):
    if epsilon > 1 or epsilon < 0:
        return False
    if learning_rate > 1 or learning_rate < 0:
        return False
    if discount > 1 or discount < 0:
        return False
    if subdivisions > 4 or subdivisions < 1:
        return False
    return True

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Input Guidelines : For the chord progression, write only the root note of each chord, seperated by a comma,"
          " add an -m to each root note if it's a minor chord, for example:\n Bm,Am,C,G would be B-minor, A-minor,"
          "C-major and G-major\n")
    inputs = input("Type chord progression\n")
    if not check_input(inputs):
        print("Wrong input format, please follow guidelines")
        exit(-1)
    choice = input("Press C for CSP, Q for Q-learning\n")
    if choice == 'C':
        board = board(inputs)
        cspAgent = CspAgent(board)
        makeOutputCsp(cspAgent, 'CSP.txt')
        parser = Parse.parse_notes('CSP.txt')
        print("The music was generated, the name of the file is CSP.txt.wav")
        exit(0)
    if choice == 'Q':
        inputs = inputs.split(',')
        epsilon = float(input("Enter an epsilon value ( values 0 to 1)\n"))
        learning_rate = float(input("Enter a learning rate value (values 0 to 1)\n"))
        discount_factor = float(input("Choose discount factor (values 0 to 1)\n"))
        iterations = int(input("Choose number of training iterations (more than 10000 takes a very long runtime)\n"))
        subdivisions = int(input("Choose maximum number of notes per beat (up to 4), more notes per beat take longer"
                                 " to compute!\n 4 notes might take up to a minute or two depending on the number"
                                 " of training iterations!\n"))
        repetitions = int(input("Choose number of bars that you would like to be played (longer gives longer input)\n"))
        if not checkQLearningInput(epsilon, learning_rate, discount_factor, subdivisions):
            print("Invalid input, make sure the epsilon, learning rate and discount values are between 0 and 1, and "
                  "the number of notes per beat is between 1 and 4.")
            exit(-1)
        chord_progression_list = chordBuilder.ChordBuilder.build_chords(inputs)
        chord_progression = list()
        for ch in chord_progression_list:
            chord_progression.append(chord.Chord(ch[1], ch[2], ch[3], ch[0]))
        player = musicGUI.musicPlayer(chord_progression, learning_rate, epsilon, discount_factor, subdivisions,
                                      'Qlearning')
        player.runTraining(iterations)
        player.run(repetitions)
        Parse.parse_notes('QLearning')
        print("The music was generated, the name of the file is QLearning.wav")
        exit(0)
    print("Invalid choice")
    exit(1)

