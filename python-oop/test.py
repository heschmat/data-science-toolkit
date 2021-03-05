import unittest

import numpy as np 

from Gaussian import Gaussian

class TestGaussianClass(unittest.TestCase):
    def setUp(self):
        self.gaussian = Gaussian(25, 2)

    def test_initialization(self): 
        self.assertEqual(self.gaussian.mu, 25, 'incorrect mean')
        self.assertEqual(self.gaussian.sd, 2, 'incorrect standard deviation')

    def test_pdf(self):
        self.assertEqual(round(self.gaussian.pdf(25), 5), 0.19947,
         'pdf function does not give expected result') 

    def test_meancalculation(self):
        self.gaussian.read_data('normal_population.txt', True)
        self.assertEqual(round(self.gaussian.calculate_mean(), 4),
         round(sum(self.gaussian.data) / float(len(self.gaussian.data)), 4),
             'calculated mean not as expected')

    def test_stdevcalculation(self):
        ndigits = 4
        self.gaussian.read_data('normal_sample.txt', True)
        n = len(self.gaussian.data)
        self.assertEqual(round(self.gaussian.sd, ndigits),
        round(np.std(self.gaussian.data) * np.sqrt(n / (n-1)), ndigits),
            'sample standard deviation incorrect')
        self.gaussian.read_data('normal_population.txt', False)
        self.assertEqual(round(self.gaussian.sd, ndigits),
        round(np.std(self.gaussian.data), ndigits),
            'population standard deviation incorrect')

    def test_add(self):
        gaussian_one = Gaussian(25, 3)
        gaussian_two = Gaussian(30, 4)
        gaussian_sum = gaussian_one + gaussian_two
        
        self.assertEqual(gaussian_sum.mu, 55)
        self.assertEqual(gaussian_sum.sd, 5)

    def test_repr(self):
        m, s = 25, 3
        gaussian_one = Gaussian(m, s)
        
        self.assertEqual(str(gaussian_one), f'Normal Distribution: mean: {m}, sd: {s}')
