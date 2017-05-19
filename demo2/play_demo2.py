import pybinsim

if __name__ == "__main__":

    with pybinsim.BinSim('config/demo2.cfg') as binsim:
        binsim.stream_start()

