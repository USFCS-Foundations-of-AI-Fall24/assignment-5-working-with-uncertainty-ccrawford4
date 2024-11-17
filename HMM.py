import math
import random
import argparse
import codecs
import os
import sys

import numpy
from plotly.validators.histogram import cumulative


# Sequence - represents a sequence of hidden states and corresponding
# output variables.

class Sequence:
    def __init__(self, stateseq, outputseq):
        self.stateseq  = stateseq   # sequence of states
        self.outputseq = outputseq  # sequence of outputs
    def __str__(self):
        return ' '.join(self.stateseq)+'\n'+' '.join(self.outputseq)+'\n'
    def __repr__(self):
        return self.__str__()
    def __len__(self):
        return len(self.outputseq)

# HMM model
class HMM:
    def __init__(self, transitions={}, emissions={}):
        """creates a model from transition and emission probabilities
        e.g. {'happy': {'silent': '0.2', 'meow': '0.3', 'purr': '0.5'},
              'grumpy': {'silent': '0.5', 'meow': '0.4', 'purr': '0.1'},
              'hungry': {'silent': '0.2', 'meow': '0.6', 'purr': '0.2'}}"""



        self.transitions = transitions
        self.emissions = emissions

    ## part 1 - you do this.
    def load(self, basename):
        emit_file = open(f'{basename}.emit', 'r')
        transmission_file = open(f'{basename}.trans', 'r')

        emit_lines = emit_file.readlines()
        for line in emit_lines :
            parts = line.split()
            key, child, score = parts[0], parts[1], float(parts[2])
            if key not in self.emissions :
                self.emissions[key] = {}
            self.emissions[key][child] = score

        # Load Transmission
        trans_lines = transmission_file.readlines()
        for line in trans_lines :
            parts = line.split()
            key, child, score = parts[0], parts[1], float(parts[2])
            if key not in self.transitions:
                self.transitions[key] = {}
            self.transitions[key][child] = score

   ## you do this.
    def generate(self, n):
        result = ""

        def build_total(map) :
            cumulative = []
            total = 0
            for state, score in map.items() :
                total += score
                cumulative.append({'state': state, 'score': score})

            return cumulative

        def get_best_atribute(cumulative) :
            random.shuffle(cumulative)
            r = random.random()
            for j, threshold in enumerate(cumulative):
                if r <= threshold['score']:
                    return threshold['state']

            return cumulative[0]['state']

        states = self.transitions['#']
        # Your loop, but simplified
        for i in range(n):
            # Keep track of total
            cumulative = build_total(states)
            best_transmission = get_best_atribute(cumulative)

            emissions = self.emissions[best_transmission]
            emissions_cumulative = build_total(emissions)
            best_emission = get_best_atribute(emissions_cumulative)

            result += best_transmission + " " + best_emission + "\n"
            states = self.transitions[best_transmission]
        return result

    def forward(self, sequence):
        # summing all the probablities
        # transition probablity * emission probablity?
        O = list(set(sequence.outputseq))
        t = len(O)
        M = {time: {state: 0 for state in sequence.stateseq} for time in range(1, t + 1)}

        for s in sequence.stateseq:
            M[1][s] = (self.transitions[sequence.stateseq[0]][s] if s in self.transitions[sequence.stateseq[0]] else 0.0) * (self.emissions[s][O[0]] if O[0] in self.emissions[s] else 0.0)

        for i in range(2, t + 1):
            for s in sequence.stateseq:
                M[i][s] = sum(
                    M[i - 1][s2] * (self.transitions[s2][s] if s in self.transitions[s2] else 0.0) * (self.emissions[s][O[i - 1]] if O[i - 1] in self.emissions[s] else 0.0)
                    for s2 in sequence.stateseq
                )
        return M

    ## you do this: Implement the Viterbi algorithm. Given a Sequence with a list of emissions,
    ## determine the most likely sequence of states.
    def viterbi(self, sequence):
        pass
    ## You do this. Given a sequence with a list of emissions, fill in the most likely
    ## hidden states using the Viterbi algorithm.


def main() :
    file, flag, amount = sys.argv[1], sys.argv[2], sys.argv[3]
    hmm = HMM()
    hmm.load(file)


    if flag == '--generate' :
        print(hmm.generate(int(amount)))
    elif flag == '--forward':
        dest_file_name = sys.argv[3]
        dest_file = open(f'{dest_file_name}', 'w')
        dest_file.write(hmm.generate(20))
        dest_file.close()
        with open(dest_file_name, 'r') as f:
            lines = f.readlines()

        states = []
        outputs = []
        for line in lines:
            state, output = line.strip().split()
            states.append(state)
            outputs.append(output)

        seq = Sequence(states, outputs)
        print(hmm.forward(seq))

if __name__ == '__main__':
    main()