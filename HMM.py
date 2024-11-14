import math
import random
import argparse
import codecs
import os
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

            result += best_transmission + " " + best_emission + " "
            states = self.transitions[best_transmission]


        return result

    def forward(self, sequence):
        # summing all the probablities
        # transition probablity * emission probablity?

        pass
    ## you do this: Implement the Viterbi algorithm. Given a Sequence with a list of emissions,
    ## determine the most likely sequence of states.






    def viterbi(self, sequence):
        pass
    ## You do this. Given a sequence with a list of emissions, fill in the most likely
    ## hidden states using the Viterbi algorithm.


def main() :
    # Do work to
    arg = 'cat'
    n = 20

    hmm = HMM()
    hmm.load(arg)
    print(hmm.generate(n))




if __name__ == '__main__':
    main()