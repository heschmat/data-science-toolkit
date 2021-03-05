import math

import numpy as np
import matplotlib.pyplot as plt

class Gaussian:
    """ Gaussian distribution class for calculating and 
    visualizing a Gaussian distribution.
    
    Attributes:
        mean (float) the mean value of the distribution
        stddev (float) the standard deviation of the distribution
        data (list of floats) a list of floats extracted from the data file        
    """

    def __init__(self, mean= 0, sd= 1) -> None:
        self.mu = mean
        self.sd = sd
        self.data = []

    def calculate_mean(self) -> float:
        """ Calculate the mean of the dataset

        Returns:
        (float) mean of the dataset
        """
        self.mu = np.mean(self.data)
        return self.mu

    def calculate_stddev(self, is_sample: bool) -> float:
        """ Calculate the standard deviation of the data set.
        
        Args: 
            is_sample (bool): whether the data represents a sample or population
        
        Returns: 
            (float): standard deviation of the data set
        """
        n = len(self.data)
        mu = self.calculate_mean()
        diffs_squared = np.array([math.pow(x - mu, 2) for x in self.data])

        # If it's a sample, adjust the denominator (i.e., subtract one)
        if is_sample:
            n -= 1

        # Calculate the variance
        data_var = diffs_squared.sum() / n

        self.sd = np.sqrt(data_var)
        return self.sd

    def read_data(self, path_file, is_sample = True):
        """ Read in data from a text file.
        File format should be one number (float) per line.
        After reading the file, the mean and standard deviation are calculated.

        Args:
        path_file (str): the path to the file that holds the data
        """
        self.data = []
        with open(path_file, 'r') as f:
            line = f.readline()
            while line:
                self.data.append(float(line.strip()))
                line = f.readline()
        # Convert list to numpy array
        self.data = np.array(self.data)

        # Calculate the mean and the standard deviation
        self.mu = self.calculate_mean()
        self.sd = self.calculate_stddev(is_sample)


    def histogram(self):
        """Plot the histogram of instance variable `data`."""
        plt.hist(self.data)
        plt.title(self)

    def pdf(self, x):
        """"""
        m, s = self.mu, self.sd
        a = 1./ np.sqrt(2 * math.pi * s ** 2)
        return a * np.exp(-.5 * ((x - m) / s) ** 2)

    def plot_density(self):
        """"""
        res = zip(self.data, [self.pdf(x) for x in self.data])
        res = sorted(res, key= lambda point: point[0])

        x = [point[0] for point in res]
        y = [point[1] for point in res]

        plt.plot(x, y)
        plt.title(self)

    def __add__(self, other):
        """Add together two Gaussian distributions.
        
        Args:
        other (Gaussian): Gaussian instance
        
        Returns:
        (Gaussian)
        """
        res = Gaussian()
        res.mu = self.mu + other.mu
        res.sd = np.sqrt(self.sd ** 2 + other.sd ** 2)
        return res

    def __repr__(self) -> str:
        return (
            f'Normal Distribution: mean: {round(self.mu, 2)}, '
            f'sd: {round(self.sd, 2)}'
        )


if __name__ == '__main__':
    import unittest
    from test import TestGaussianClass
    tests = TestGaussianClass()
    tests_loaded = unittest.TestLoader().loadTestsFromModule(tests)
    unittest.TextTestRunner().run(tests_loaded)