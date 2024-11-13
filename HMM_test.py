import unittest
import HMM as hmm


class MyTestCase(unittest.TestCase):
    def test_load(self):
        hmm1 = hmm.HMM()
        hmm1.load('cat')

        self.assertEqual(hmm1.transitions,{
                '#': {'happy': 0.5, 'grumpy': 0.5, 'hungry': 0.0},
                'happy': {'happy': 0.5, 'grumpy': 0.1, 'hungry': 0.4},
                'grumpy': {'happy': 0.6, 'grumpy': 0.3, 'hungry': 0.1},
                'hungry': {'happy': 0.1, 'grumpy': 0.6, 'hungry': 0.3}
            })

        self.assertEqual(hmm1.emissions, {
            'happy': {'silent': 0.2, 'meow': 0.3, 'purr': 0.5},
            'grumpy': {'silent': 0.5, 'meow': 0.4, 'purr': 0.1},
            'hungry': {'silent': 0.2, 'meow': 0.6, 'purr': 0.2}
        })



if __name__ == '__main__':
    unittest.main()
