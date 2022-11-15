import scipy.interpolate as intpo
import matplotlib.pyplot as plt
import numpy as np

time_interval = [0, 5, 7.5, 8.75, 10,  10.1, 10.2, 10.3, 10.4,  11.65, 12.5, 15.4, 20.4] # [0, 1, 1.5, 1.75, 2,  2.1, 2.2, 2.3, 2.4,  2.65, 2.9, 3.4, 4.4]

def get_motion_funs(time=time_interval):
    # servo3=[74.1,70.7, 73.9, 73.2,67.42,66.7,69,74.5,81.8,87.5, 85.9, 78,74.1]
    # servo2_old=[17.2,15.5, 17.1,16.7,13.6,24.2,29.6,26.9,18.9,19.26, 19.25,17.9,17.2]

    # diff2 = 17.2
    # diff3 = 74.1

    # servo2 = [2 * 17.2 - servo2_old[i] for i in range(len(servo2_old))]

    # print([round(servo2[i] - diff2, 1) for i in range(len(servo2))])
    # print([round(servo3[i] - diff3, 1) for i in range(len(servo3))])


    servo2angle = [0.0, 1.7, 0.1, 0.5, 3.6, -7.0, -12.4, -9.7, -1.7, -2.1, -2.1, -0.7, 0.0]
    servo3angle = [0.0, -3.4, -0.2, -0.9, -6.7, -7.4, -5.1, 0.4, 7.7, 13.4, 11.8, 3.9, 0.0]

    f2 = intpo.interp1d(time, servo2angle, "quadratic")
    f3 = intpo.interp1d(time, servo3angle, "quadratic")

    return [f2, f3]

if __name__ == "__main__":
    f2, f3 = get_motion_funs()

    print([f2, f3])