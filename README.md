# pyBinSim Demo Repository
Different applications using pyBinSim 



## Install pyBinSim

    $ conda create --name binsim35 python=3.5 numpy scipy
    $ source activate binsim35  # on windows: activate binsim35
    $ pip install pybinsim
        
## Start Demo1 (simple playback)
    $ cd demo1/
    $ python play_demo.py

## Start Demo2 (Razor AHRS Compare Switch)
    $ cd demo2/

Please start the tracking script and the playdemo script seperately:

    $ python tracker.py
    $ python play_demo.py

