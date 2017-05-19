# This file is part of the pyBinSim project.
#
# Copyright (c) 2017 A. Neidhardt, F. Klein, N. Knoop, T. Köllmer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import sys
import time
import msvcrt

from pythonosc import udp_client

from pybinsim.spark_fun import Spark9dof


def start_tracker():
    # Default values
    oscIdentifier = '/pyBinSim'
    ip = '127.0.0.1'
    port = 10000

    # please choose the correct COM-Port
    comPort = 'COM4'
    baudRate = 57600

    nSources = 1
    minAngleDifference = 5
    filterSet = 0

    # Value override by user
    if (len(sys.argv)) > 1:
        for i in range(len(sys.argv)):

            if (sys.argv[i] == '-comPort'):
                comPort = sys.argv[i + 1]

            if (sys.argv[i] == '-port'):
                port = int(sys.argv[i + 1])

            if (sys.argv[i] == '-ip'):
                ip = sys.argv[i + 1]

            if (sys.argv[i] == '-baudRate'):
                baudRate = int(sys.argv[i + 1])

    # Internal settings:
    positionVectorSubSampled = range(0, 360, minAngleDifference)

    print(['ComPort :', comPort])
    print(['Baudrate: ', baudRate])
    print(['IP: ', ip])
    print(['Using Port ', port])

    # Create OSC client
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=ip, help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=port, help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    try:
        spark9dof = Spark9dof(com_port=comPort, baudrate=baudRate)
    except RuntimeError as e:
        print(e)
        sys.exit(-1)

    while 1:

        # define current angles as "zero position"	when spacebar is hit
        if msvcrt.kbhit():
            char = msvcrt.getch()

            if ord(char) == 32:
                rollOffset = roll
                pitchOffset = pitch
                yawOffset = yaw

            # Key '1' actives 1st filter set
            if ord(char) == 49:
                filterSet = 0
            # Key '2' actives 2nd filter set
            if ord(char) == 50:
                filterSet = 1


            print(filterSet)

        rpy = spark9dof.get_sensor_data()

        if rpy:
            roll, pitch, yaw = rpy
            yaw += 180
        else:
            roll, pitch, yaw = 0, 0, 0



        # build OSC Message and send it
        for n in range(0, nSources):
            # channel valueOne valueTwo ValueThree valueFour valueFive ValueSix
            yaw = min(positionVectorSubSampled, key=lambda x: abs(x - yaw))
            binSimParameters = [n, int(round(yaw)), filterSet, 0, 0, 0, 0]
            print(['Source ', n, ' Yaw: ', round(yaw), '  Filterset: ', filterSet])
            client.send_message(oscIdentifier, binSimParameters)

        time.sleep(0.1)


if __name__ == "__main__":
    start_tracker()
