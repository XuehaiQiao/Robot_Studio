import scipy.interpolate as intpo
import matplotlib.pyplot as plt
import numpy as np

time_interval = [0, 5, 7.5, 9, 10, 10.1, 10.2, 10.3, 10.4, 11.5, 15, 20] # [0, 1, 1.5, 1.8, 2, 2.1, 2.2, 2.3, 2.4, 2.7, 3.4, 4.4]

def get_motion_funs(time=time_interval):
    # servo2_old = [17.5,14.1,18.4,20.9,21.5,20.7,17.5]
    # servo2 = [2 * 17.5 - servo2_old[i] for i in range(len(servo2_old))]
    # servo3 = [63.4,59.4,60.4,62.3,65,68.1,63.4]

    # print([round(servo2[i] - diff2, 1) for i in range(len(servo2))])
    # print([round(servo3[i] - diff3, 1) for i in range(len(servo3))])

    # time=[0,1, 1.5,1.8,   2,2.1,2.2,2.3,2.4,  2.7,    3.4,4.4]
    # servo3=[70.6, 65.9, 63, 62, 61.7, 61.9, 66, 72.9, 82.3, 85, 76.4, 70.6]
    # servo2_old=[13.9, 10.5, 8,6.2, 5.9, 17.6, 24.4, 23.6, 17.5, 16, 15.8, 13.9]
    # servo2 = [2 * 13.9 - servo2_old[i] for i in range(len(servo2_old))]

    # diff2 = 13.9
    # diff3 = 70.6

    # print([round(servo2[i] - diff2, 1) for i in range(len(servo2))])
    # print([round(servo3[i] - diff3, 1) for i in range(len(servo3))])

    servo2angle = [0.0, 3.4, 5.9, 7.7, 8.0, -3.7, -10.5, -9.7, -3.6, -2.1, -1.9, 0.0]
    servo3angle = [0.0, -4.7, -7.6, -8.6, -8.9, -8.7, -4.6, 2.3, 11.7, 14.4, 5.8, 0.0]

    f2 = intpo.interp1d(time, servo2angle, "quadratic")
    f3 = intpo.interp1d(time, servo3angle, "quadratic")

    return [f2, f3]

if __name__ == "__main__":
    f2, f3 = get_motion_funs()

    print([f2, f3])