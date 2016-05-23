import bpy
import math
from math import degrees
import serial
import time

port = "/dev/cu.wchusbserialfd120"

ser = serial.Serial(port)

def turnServo(board_id, servo_nr, pos):
	#assert(board_id in [i for i in xrange(16)]), "board_id has to be in [0,..,15]"
	#assert(servo_nr in [i for i in xrange(16)]), "servo_nr has to be in [0,..,15]"
	#assert(pos>=0 and pos<=180), "position between 0 and 180 degree"
	servo = board_id<<4 | servo_nr
	ser.write(('S'+chr(servo)+chr(int(pos))).encode('latin_1'))
	
time.sleep(1)

def my_handler(scene): 
  """Handler that get's the Euler X rotation from two cubes and passes this to servos 9 and 10 though the serial port.""" 

  # Get the Euler x rotation in degrees.  The rotation for "Cube" will be applied to servo on pin 9
  servoAngle = degrees(bpy.data.objects['Cube'].rotation_euler.x)
 
  turnServo(0,0,servoAngle)  

# Register the handler to be called once the frame has changed.
bpy.app.handlers.frame_change_post.append(my_handler)

print("Servo ready")