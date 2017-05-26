# pyBinSim Demo Repository
Different applications using pyBinSim 

## Demo4 - Use tracking data from Oculus Rift
This example shows, how to use the tracking data of the Oculus Rift. Please check, whether the ovr1130.py is already a python3-version, otherwise replace it with 
https://github.com/cmbruns/pyovr/blob/c49d98474761539b4cbc8b825de98f56d547bfc2/ovr/_ovr1130.py


## Install pyBinSim
    $ conda create --name binsim35 python=3.5 numpy scipy
    $ source activate binsim35  # on windows: activate binsim35
    $ pip install pybinsim
        
## Start Demo4
    $ cd demo4/
    $ python play_demo4.py
	
## Start Tracking in a separate thread
	$ python oculus2pybinsim.py
	
