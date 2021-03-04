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
