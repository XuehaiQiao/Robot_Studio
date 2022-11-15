from math import sin, cos
from pylx16a.lx16a import *
import time
from Robot import *

LX16A.initialize("/dev/ttyUSB0", 0.1)

servo_count = 6
try:
    servos = [LX16A(i) for i in range(1, servo_count+1)]
    for servo in servos:
        servo.set_timeout(0.2)
        servo.set_angle_limits(0, 240)
        servo.enable_torque()
    
    # servos[0].disable_torque()
    # servos[3].disable_torque()

        
except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()


robot = Robot(servos)

#robot.main()
# robot.pos_init()
# robot.to_pos(robot.stand_angle)
# robot.pos_init()

# robot.get_angle_change()
# robot.get_angles()
# # robot.pos_init()
# # robot.to_pos([118.56, 86.16, 105.6, 112.56, 138.72, 122.4])
# print(robot.init_angle)

robot.main()