# pyBinSim Demo Repository
Different applications using pyBinSim 

## Demo3 - Translation with Vive
This is an example of an interactive listener translation towards a sound source, using the HTC Vive tracking. 
The provided binaural room impulse responses were created using MCRoomSim.


## Install pyBinSim
    $ conda create --name binsim35 python=3.5 numpy scipy
    $ source activate binsim35  # on windows: activate binsim35
    $ pip install pybinsim
        
## Start Demo3
    $ cd demo3/
    $ python play_demo.py
	
## Start Tracking in a separate thread
	$ python translationWithVive.py
	
