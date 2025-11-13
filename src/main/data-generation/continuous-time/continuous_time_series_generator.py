#################################################################
#                                                               #
#   Author:   Teresa Dalle Nogare                               #
#   Date:     August 2024                                       #
#                                                               #
#   Summary:  Definition of the major class for continuous      #
#             time series generation                            #
#                                                               #   
#################################################################

from abc import abstractmethod
import os
import pandas as pd
import numpy as np

cwd = os.getcwd()

class ContinuousTimeSeriesGenerator: # parent class
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
        self.dsf = None # downsampling factor

    @abstractmethod
    def generate_forward(self, **kwarg): # method implemented in subclass
        """ 
        Method for generation of forward trajectories implemented in subclasses 
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

    def downsample_forward(self, **kwarg):  
        """
        Method to downsample forward trajectories implemented in subclasses
        """
        pass

    def downsample(self, **kwarg):
        """
        Downsample forward and reverse trajectories
        """
        self.samples, self.dsf = self.downsample_forward(**kwarg)
        

    def cut_trajectory_forward(self):
        """
        Method to cut trajectory to "cut" samples implemented in subclasses. "cut" is specified in the function
        """
        pass

    def cut_trajectory(self):
        """
        Cuts trajectory to "cut" samples
        """
        self.samples = self.cut_trajectory_forward()
        self.reverse_samples = [reversed(x) for x in self.samples]


    def save(self, save_to=os.path.join(cwd, 'data-tr/time-series/data-cnt/')): 
        """
        Saves sample of time series as csv
        Returns list of filepaths
        
        Forward filename: [NAME]_[NUM].txt
        Reverse filename: [NAME]_reverse_[NUM].txt
        """
        
        if not os.path.exists(save_to):
            os.mkdir(save_to)
        
        save_to_name = os.path.join(save_to, self.name)
        save_to_dsf = os.path.join(save_to, 'DSF') # folder for downsampling factor

        if os.path.exists(save_to_name):
            k = 1
            new_save_to = save_to_name + f"_{k}"
            while os.path.exists(new_save_to):
                k += 1
                new_save_to = save_to_name + '_' + str(k)
            
            save_to_name = new_save_to

        os.mkdir(save_to_name)

        # create folder DSF in DAta if it does not exist
        if not os.path.exists(save_to_dsf):
            os.mkdir(save_to_dsf)
        
        # Save downsampling factor
        np.savetxt(os.path.join(save_to_dsf, f'{self.name}_DSF.txt'), self.dsf, fmt='%d')


        forward_filepaths = []
        num_digits = len(str(self.n))
        for k, x in enumerate(self.samples):
            path = os.path.join(save_to_name, f'{self.name}_{str(k).zfill(num_digits)}.txt')
            df = pd.DataFrame({'v':x})
            df.to_csv(path, index=False, header=False)
            forward_filepaths.append(path)
            
        reverse_filepaths = []            
        for k, x in enumerate(self.reverse_samples):
            path = os.path.join(save_to_name, f'{self.name}_reverse_{str(k).zfill(num_digits)}.txt')
            df = pd.DataFrame({'v':x})
            df.to_csv(path, index=False, header=False)
            reverse_filepaths.append(path)            
            
        return forward_filepaths, reverse_filepaths
    

class ThreeDimContinuousTimeSeriesGenerator: # parent class
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
        self.samples_x=[]
        self.samples_y=[]
        self.samples_z=[]
        self.samples_sum=[]
        self.reverse_samples_x=[]
        self.reverse_samples_y=[]
        self.reverse_samples_z=[]
        self.reverse_samples_sum=[]
        self.dsf = None # downsampling factor

    @abstractmethod
    def generate_forward(self, **kwarg): # method implemented in subclass
        """ 
        Method for generation of forward trajectories implemented in subclasses 
        """
        pass

    def generate(self):
        """
        Generates forward trajectories
        """
        self.samples_x, self.samples_y, self.samples_z = zip(*[self.generate_forward() for k in range(self.n)])
        self.samples_x = list(self.samples_x)
        self.samples_y = list(self.samples_y)
        self.samples_z = list(self.samples_z)
        self.samples_sum = [x+y+z for x,y,z in zip(self.samples_x, self.samples_y, self.samples_z)]


    def discard_transient_forward(self):
        """
        Method to discard transient of forward trajectories implemented in subclasses
        """
        pass

    def discard_transient(self):
        """
        Discards transient of forward trajectories
        """
        self.samples_x, self.samples_y, self.samples_z, self.samples_sum = self.discard_transient_forward()

    def downsample_forward(self, **kwarg):  
        """
        Method to downsample forward trajectories implemented in subclasses
        """
        pass

    def downsample(self, **kwarg):
        """
        Downsample forward and reverse trajectories
        """
        self.samples_x, self.samples_y, self.samples_z, self.samples_sum, self.dsf = self.downsample_forward(**kwarg)

    def cut_trajectory_forward(self):
        """
        Method to cut trajectory to "cut" samples implemented in subclasses. "cut" is specified in the function
        """
        pass

    def cut_trajectory(self):
        """
        Cuts trajectory to "cut" samples
        """
        self.samples_x, self.samples_y, self.samples_z, self.samples_sum= self.cut_trajectory_forward()
        self.reverse_samples_x = [reversed(x) for x in self.samples_x]
        self.reverse_samples_y = [reversed(y) for y in self.samples_y]
        self.reverse_samples_z = [reversed(z) for z in self.samples_z]
        self.reverse_samples_sum = [reversed(s) for s in self.samples_sum]
        
        

    def save(self, save_to=os.path.join(cwd, 'data-tr/time-series/data-cnt/')):
        """
        Saves sample of time series in three csv files, one for x, y, z
        Returns list of filepaths
        
        Forward filename: [NAME]_[NUM].txt
        Reverse filename: [NAME]_reverse_[NUM].txt
        """
        
        if not os.path.exists(save_to):
            os.mkdir(save_to)
        
        save_to_x = os.path.join(save_to, self.name+'_X')
        save_to_y = os.path.join(save_to, self.name+'_Y')
        save_to_z = os.path.join(save_to, self.name+'_Z')
        save_to_sum = os.path.join(save_to, self.name+'_SUM')
        save_to_dsf = os.path.join(save_to, 'DSF') # folder for downsampling factor

        if os.path.exists(save_to_x):
            k = 1
            new_save_to = save_to_x + f"_{k}"
            while os.path.exists(new_save_to):
                k += 1
                new_save_to = save_to_x + '_' + str(k)
            
            save_to_x = new_save_to

        os.mkdir(save_to_x)

        if os.path.exists(save_to_y):
            k = 1
            new_save_to = save_to_y + f"_{k}"
            while os.path.exists(new_save_to):
                k += 1
                new_save_to = save_to_y + '_' + str(k)
            
            save_to_y = new_save_to

        os.mkdir(save_to_y)

        if os.path.exists(save_to_z):
            k = 1
            new_save_to = save_to_z + f"_{k}"
            while os.path.exists(new_save_to):
                k += 1
                new_save_to = save_to_z + '_' + str(k)
            
            save_to_z = new_save_to

        os.mkdir(save_to_z)

        if os.path.exists(save_to_sum):
            k = 1
            new_save_to = save_to_sum + f"_{k}"
            while os.path.exists(new_save_to):
                k += 1
                new_save_to = save_to_sum + '_' + str(k)
            
            save_to_sum = new_save_to

        os.mkdir(save_to_sum)

        # create folder DSF in DAta if it does not exist
        if not os.path.exists(save_to_dsf):
            os.mkdir(save_to_dsf)
        
        # Save downsampling factor
        # Save downsampling factor
        np.savetxt(os.path.join(save_to_dsf, f'{self.name}_DSF.txt'), self.dsf, fmt='%d')
  

        forward_filepaths_x = []
        forward_filepaths_y = []
        forward_filepaths_z = []
        forward_filepaths_sum = []
        num_digits = len(str(self.n))

        for k, x in enumerate(self.samples_x):
            path = os.path.join(save_to_x, f'{self.name}_X_{str(k).zfill(num_digits)}.txt')
            df = pd.DataFrame({'x':x})
            df.to_csv(path, index=False, header=False)
            forward_filepaths_x.append(path)

        for k, y in enumerate(self.samples_y):
            path = os.path.join(save_to_y, f'{self.name}_Y_{str(k).zfill(num_digits)}.txt')
            df = pd.DataFrame({'y':y})
            df.to_csv(path, index=False, header=False)
            forward_filepaths_y.append(path)

        for k, z in enumerate(self.samples_z):
            path = os.path.join(save_to_z, f'{self.name}_Z_{str(k).zfill(num_digits)}.txt')
            df = pd.DataFrame({'z':z})
            df.to_csv(path, index=False, header=False)
            forward_filepaths_z.append(path)

        for k, s in enumerate(self.samples_sum):
            path = os.path.join(save_to_sum, f'{self.name}_SUM_{str(k).zfill(num_digits)}.txt')
            df = pd.DataFrame({'sum':s})
            df.to_csv(path, index=False, header=False)
            forward_filepaths_sum.append(path)

        reverse_filepaths_x = []    
        reverse_filepaths_y = []  
        reverse_filepaths_z = []      
        reverse_filepaths_sum = []    
        for k, x in enumerate(self.reverse_samples_x):
            path = os.path.join(save_to_x, f'{self.name}_X_reverse_{str(k).zfill(num_digits)}.txt')
            df = pd.DataFrame({'x':x})
            df.to_csv(path, index=False, header=False)
            reverse_filepaths_x.append(path)  

        for k, y in enumerate(self.reverse_samples_y):
            path = os.path.join(save_to_y, f'{self.name}_Y_reverse_{str(k).zfill(num_digits)}.txt')
            df = pd.DataFrame({'y':y})
            df.to_csv(path, index=False, header=False)
            reverse_filepaths_y.append(path)

        for k, z in enumerate(self.reverse_samples_z):
            path = os.path.join(save_to_z, f'{self.name}_Z_reverse_{str(k).zfill(num_digits)}.txt')
            df = pd.DataFrame({'z':z})
            df.to_csv(path, index=False, header=False)
            reverse_filepaths_z.append(path)
            
        for k, s in enumerate(self.reverse_samples_sum):
            path = os.path.join(save_to_sum, f'{self.name}_SUM_reverse_{str(k).zfill(num_digits)}.txt')
            df = pd.DataFrame({'sum':s})
            df.to_csv(path, index=False, header=False)
            reverse_filepaths_sum.append(path)
        
            
        return forward_filepaths_x, forward_filepaths_y, forward_filepaths_z, forward_filepaths_sum, reverse_filepaths_x, reverse_filepaths_y, reverse_filepaths_z, reverse_filepaths_sum
    

