import pybinsim

if __name__ == "__main__":

    with pybinsim.BinSim('config/demo1.cfg') as binsim:
        binsim.stream_start()

