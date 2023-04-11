from QLearningAgent import musicEnvironment
from QLearningAgent import qlearningAgents
from QLearningAgent import chord
import writer
import Parse

ROOT = 0
CHORD = 0
class musicPlayer:
    def __init__(self, chord_progression, alpha, epsilon, gamma, subdivisions, fileName):
        self.scales = [['G','A','B','C','D','E','g', '$', 'b', 'F', 'd', 'e', 'a']]
        self.musicEnvironment = musicEnvironment.MusicEnvironment(self.scales, chord_progression, subdivisions)
        actionFn = lambda state: \
            self.musicEnvironment.getPossibleActions(state)
        self.learner = qlearningAgents.QLearningAgent(actionFn=actionFn)
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.learner.setEpsilon(self.epsilon)
        self.learner.setLearningRate(self.alpha)
        self.learner.setDiscount(self.gamma)
        self.stepCount = 0
        self.fileWriter = writer.Writer(fileName)
        self.actions_in_bar = []

    def step(self, is_training):
        self.stepCount += 1
        state = self.musicEnvironment.getCurrentState()

        actions = self.musicEnvironment.getPossibleActions(state)
        if len(actions) == 0.0:
            self.musicEnvironment.reset()
            state = self.musicEnvironment.getCurrentState()
            actions = self.musicEnvironment.getPossibleActions(state)
            print('Reset!')
        action = self.learner.getAction(state)
        self.actions_in_bar.append(action)
        if not is_training:
            if self.stepCount % 4 == 0:
                self.fileWriter.writeBar(state[CHORD].get_name(), self.actions_in_bar)
                self.actions_in_bar = []
        if action == None:
            raise Exception('None action returned: Code Not Complete')
        nextState, reward = self.musicEnvironment.doAction(action)

        self.learner.update(state, action, nextState, reward)

    def runTraining(self, bars):
        reps = bars * 4
        for i in range(reps):
            self.step(True)
            if self.learner.epsilon > 0:
                self.learner.epsilon -= 1/reps

    def run(self, bars):
        self.fileWriter.openFile()
        reps = bars * 4
        self.actions_in_bar = []
        for i in range(reps):
            self.step(False)
        self.fileWriter.closeFile()

