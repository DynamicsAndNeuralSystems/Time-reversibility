#################################################################
#                                                               #
#   Author:   Teresa Dalle Nogare                               #
#   Date:     August 2024                                       #
#                                                               #
#   Summary:  Definition of the major class for time series     #
#             generation                                        #
#                                                               #
#################################################################

from abc import abstractmethod
import os
import pandas as pd

class TimeSeriesGenerator: # parent class
    """
    n: number of realizations of the random process
    length: temporal length of the time series (number of samples)
    samples: contain time series values
    reverse_samples: containe reversed time series values
    """
    def __init__(self, name, n, length): # attributes
        self.name=name
        self.n=n
        self.length=length
        self.samples=[]
        self.reverse_samples=[]
       
    
    @abstractmethod
    def generate_forward(self, **kwarg): # method implemented in subclass
        """ 
        Method for generation of forward trajectories that has to be implemented by subclasses 
        """
        pass

    def generate(self):
        """
        Generates forward trajectories
        """
        self.samples = [self.generate_forward() for k in range(self.n)]

    def discard_transient_forward(self):
        """
        Method to discard transient of forward trajectories implemented in subclasses
        """
        pass

    def discard_transient(self):
        """
        Discards transient of forward trajectories
        """
        self.samples = self.discard_transient_forward()
        self.reverse_samples = [reversed(x) for x in self.samples]

    def save(self, save_to='XXXX/'): # name of the folder to save the data
        """
        Saves sample of time series as csv
        Returns list of filepaths
        
        Forward filename: [NAME]_[NUM].txt
        Reverse filename: [NAME]_reverse_[NUM].txt
        """
        
        if not os.path.exists(save_to):
            os.mkdir(save_to)
        
        save_to = os.path.join(save_to, self.name)

        if os.path.exists(save_to):
            k = 1
            new_save_to = save_to + f"_{k}"
            while os.path.exists(new_save_to):
                k += 1
                new_save_to = save_to + '_' + str(k)
            
            save_to = new_save_to

        os.mkdir(save_to)

        forward_filepaths = []
        num_digits = len(str(self.n))
        for k, x in enumerate(self.samples):
            path = os.path.join(save_to, f'{self.name}_{str(k).zfill(num_digits)}.txt')
            df = pd.DataFrame({'v':x})
            df.to_csv(path, index=False, header=False)
            forward_filepaths.append(path)
            
        reverse_filepaths = []            
        for k, x in enumerate(self.reverse_samples):
            path = os.path.join(save_to, f'{self.name}_reverse_{str(k).zfill(num_digits)}.txt')
            df = pd.DataFrame({'v':x})
            df.to_csv(path, index=False, header=False)
            reverse_filepaths.append(path)            
            
        return forward_filepaths, reverse_filepaths
    
class WeierstrassTimeSeriesGenerator: # parent class
    """
    n: number of realizations of the random process
    length: temporal length of the time series (number of samples)
    samples: contain time series values
    reverse_samples: containe reversed time series values
    """
    def __init__(self, name, n, length): # attributes
        self.name=name
        self.n=n
        self.length=length
        self.samples=[]
        self.reverse_samples=[]
        self.used_H_values = set()  # Track previously used H values
       
    
    @abstractmethod
    def generate_forward(self, **kwarg): # method implemented in subclass
        """ 
        Method for generation of forward trajectories that has to be implemented by subclasses 
        """
        pass

    def generate(self):
        """
        Generates forward trajectories
        """
        self.samples= [self.generate_forward() for k in range(self.n)]

    def discard_transient_forward(self):
        """
        Method to discard transient of forward trajectories implemented in subclasses
        """
        pass

    def discard_transient(self):
        """
        Discards transient of forward trajectories
        """
        self.samples = self.discard_transient_forward()
        self.reverse_samples = [reversed(x) for x in self.samples]

    def save(self, save_to='XXXX/'): # name of the folder to save the data
        """
        Saves sample of time series as csv
        Returns list of filepaths
        
        Forward filename: [NAME]_[NUM].txt
        Reverse filename: [NAME]_reverse_[NUM].txt
        """
        
        if not os.path.exists(save_to):
            os.mkdir(save_to)
        
        save_to = os.path.join(save_to, self.name)

        if os.path.exists(save_to):
            k = 1
            new_save_to = save_to + f"_{k}"
            while os.path.exists(new_save_to):
                k += 1
                new_save_to = save_to + '_' + str(k)
            
            save_to = new_save_to

        os.mkdir(save_to)

        forward_filepaths = []
        num_digits = len(str(self.n))
        for k, x in enumerate(self.samples):
            path = os.path.join(save_to, f'{self.name}_{str(k).zfill(num_digits)}.txt')
            df = pd.DataFrame({'v':x})
            df.to_csv(path, index=False, header=False)
            forward_filepaths.append(path)
            
        reverse_filepaths = []            
        for k, x in enumerate(self.reverse_samples):
            path = os.path.join(save_to, f'{self.name}_reverse_{str(k).zfill(num_digits)}.txt')
            df = pd.DataFrame({'v':x})
            df.to_csv(path, index=False, header=False)
            reverse_filepaths.append(path)            
            
        # Save the used H values to a text file
        with open(os.path.join(save_to, 'used_H_values.txt'), 'w') as f:
            for h in self.used_H_values:
                f.write(f"{h}\n")
        return forward_filepaths, reverse_filepaths
    
