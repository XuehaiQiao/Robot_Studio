from math import *
import importlib
from pylx16a.lx16a import *
import robot_parameters
import time
import servo_motion_funs_v1 as servo_motion_funs

class Robot:
    def __init__(self, servos):
        #Parameters
        
        self.servos = servos
        self.servo_count = len(servos)
        self.timeout = 30000

        self.init_angle = robot_parameters.init_angle
        self.stand_angle = robot_parameters.stand_angle
        self.init_time_usage = robot_parameters.moving_time
        self.f2, self.f3 = servo_motion_funs.get_motion_funs()

        # Variables
        self.angle_output = [0] * self.servo_count
        self.t = 0

        time.sleep(1)
    
    def main(self):
        try:
            self.check_vin()
            self.check_temp()
            
            self.pos_init()
            self.walk_test(300, [self.check_temp, self.check_vin])
            self.pos_init()
        except:
            print("Exception occured in robot.main()")
            return


    
    def pos_init(self):
        self.to_pos(self.init_angle, "Position init finished")
        time.sleep(1)

    def update_physical_angle(self):
        try:
            for i, servo in enumerate(self.servos):
                self.angle_output[i] = servo.get_physical_angle()
        except ServoTimeoutError as e:
            print(f"Servo {e.id_} error when getting output. Exiting...")
            quit()

    def walk(self, t_limit=100000):
        
        t_offset = self.t
        while self.t - t_offset < t_limit:
            # self.servos[0].move(sin(self.t - t_offset) * 10 + self.init_angle[0])
            self.servos[1].move(cos(self.t - t_offset) * 10 - 10 + self.init_angle[1])
            self.servos[2].move(cos(self.t - t_offset) * 10 - 10 + self.init_angle[2])
            # self.servos[3].move(sin(self.t - t_offset) * 10 + self.init_angle[3])
            self.servos[4].move(cos(self.t - t_offset) * 10 - 10 + self.init_angle[4])
            self.servos[5].move(cos(self.t - t_offset) * 10 - 10 + self.init_angle[5])

            if self.t % 2 < 0.05:
                print(self.angle_output)
                self.update_physical_angle()

            time.sleep(0.05)
            self.t += 0.1

    def check_vin(self):
        for i in range(self.servo_count):
            vin = 0
            try:
                vin = self.servos[i].get_vin()
                vin_limit = self.servos[i].get_vin_limits()
            except ServoTimeoutError as e:
                print(f"Servo {e.id_} is not responding to get_vin(). Exiting...")
            
            if vin < vin_limit[0]:
                raise Exception( "servo {} voltage too low.".format(i+1))
            elif vin > vin_limit[1]:
                raise Exception("servo {} voltage too high.".format(i+1))
        
        print("Voltage check finished, votage in limit range.")
    
    def check_temp(self):
        for i in range(self.servo_count):
            temp = 0
            try:
                temp = self.servos[i].get_temp()
                temp_limit = self.servos[i].get_temp_limit()
            except ServoTimeoutError as e:
                print(f"Servo {e.id_} is not responding to get_temp(). Exiting...")
            
            if temp > temp_limit:
                raise Exception("servo {} temperature too high.".format(i+1))
        
        print("Temperature check finished, votage in limit range.")
    
    def get_angle_change(self):
        self.update_physical_angle()
        
        return [round(self.angle_output[i] - self.init_angle[i], 2) for i in range(self.servo_count)]
    
    def get_angles(self):
        self.update_physical_angle()
        return self.angle_output

    def to_pos(self, aim_pos, output=None):
        self.update_physical_angle()
        time.sleep(1)

        init_physical_angle = self.angle_output
        angle_diff = [aim_pos[i] - init_physical_angle[i] for i in range(self.servo_count)]
        start_t, end_t = self.t, self.t + self.init_time_usage
        while self.t < end_t:
            for i in range(self.servo_count):
                self.servos[i].move(angle_diff[i] / 2 * (1 - cos((self.t - start_t) * pi / self.init_time_usage)) + init_physical_angle[i])
            
            time.sleep(0.05)
            self.t += 0.1
        
        if output:
            print(output)
    
    def walk_test(self, timeout=robot_parameters.timeout_time, check_funs=[]):
        time.sleep(1)
        step_time_len = servo_motion_funs.time_interval[-1]

        t_offset = self.t

        while self.t < robot_parameters.timeout_time and self.t - t_offset < timeout:
            t = self.t - t_offset

            self.servos[1].move(self.init_angle[1] + self.f2(t % step_time_len))
            self.servos[2].move(self.init_angle[2] + self.f3(t % step_time_len))

            if t >= step_time_len / 2:
                self.servos[4].move(self.init_angle[4] - self.f2((t + step_time_len / 2) % step_time_len))
                self.servos[5].move(self.init_angle[5] - self.f3((t + step_time_len / 2) % step_time_len))


            if t % 100 < 0.1:
                try:
                    for fun in check_funs:
                        fun()
                except:
                    print("Exception occured in walk test")
                    return

            time.sleep(0.01)
            self.t += 0.15
        
        print("walk test finished")