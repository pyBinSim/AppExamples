from pythonosc import osc_message_builder
from pythonosc import udp_client
import numpy as np
import sys
import time
import ovr
import math



def start_tracker_app():

	oscIdentifier = '/pyBinSim'
	ip = '127.0.0.1'
	port = 10000
	nSources = 1
	minAngleDifference=5

	if (len(sys.argv))>1:
		for i in range(len(sys.argv)):

			if( sys.argv[i] == '-port' ):
				port = int(sys.argv[i+1])
				
			if( sys.argv[i] == '-ip' ):
				ip = sys.argv[i+1]
				
			if( sys.argv[i] == '-nSources' ):
				nSources = int(sys.argv[i+1])
				
			if( sys.argv[i] == '-angleStep' ):
				minAngleDifference = int(sys.argv[i+1])
				
	# Internal settings:
	positionVector=np.arange(360)
	positionVectorSubSampled=xrange(0,360,minAngleDifference)
				
	# Create OSC client 
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", default=ip,help="The ip of the OSC server")
	parser.add_argument("--port", type=int, default=port, help="The port the OSC server is listening on")
	args = parser.parse_args()

	client = udp_client.SimpleUDPClient(args.ip, args.port)

				
	# Create OVR session			
	ovr.initialize(None)
	session, luid = ovr.create()
	hmdDesc = ovr.getHmdDesc(session)
	print hmdDesc.ProductName
	

	try :
		while 1:
					# Query the HMD for the current tracking state.
					ts  = ovr.getTrackingState(session, ovr.getTimeInSeconds(), True)
			
					if ts.StatusFlags & (ovr.Status_OrientationTracked | ovr.Status_PositionTracked):
							pose = ts.HeadPose.ThePose
																			
							yawRad, pitchRad, rollRad=pose.Orientation.getEulerAngles(axis1=1, axis2=0, axis3=2, rotate_direction=1, handedness=1)
							
							yaw=int(round(np.rad2deg(yawRad)))
							pitch=int(round(np.rad2deg(pitchRad)))
							roll=int(round(np.rad2deg(rollRad)))
										
							   
							# Adjustment to desired global origin
							yaw=360-yaw
							
							if yaw>360:     
								yaw=yaw-360
						   
							print(['YAW: ',yaw,' PITCH: ',pitch,'ROLL: ',roll])
							
							for n in range(0,nSources):
								# round yaw to angle stepsize
								yaw=min(positionVectorSubSampled, key=lambda x: abs(x - yaw))
								#channel valueOne valueTwo ValueThree valueFour valueFive ValueSix
								binSimParameters=[n,yaw,n,0,0,0,0]
								print([' Yaw: ', yaw])
								client.send_message(oscIdentifier, binSimParameters)


							#print pose
							sys.stdout.flush()
				
					time.sleep(0.020)
					
			
	except KeyboardInterrupt:	# Break if ctrl+c is pressed
		
			ovr.destroy(session)
			ovr.shutdown()
			
			print('Done')
			

if __name__ == "__main__":
	start_tracker_app()