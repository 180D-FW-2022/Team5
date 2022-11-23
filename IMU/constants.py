#Kalman filter variables
Q_angle = 0.02
Q_gyro = 0.0015
R_angle = 0.005

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846

ACC_MEDIANTABLESIZE = 15         # Median filter table size for accelerometer. Higher = smoother but a longer delay
MAG_MEDIANTABLESIZE = 9         # Median filter table size for magnetometer. Higher = smoother but a longer delay
