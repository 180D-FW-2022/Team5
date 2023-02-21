import numpy as np
# capture source number select the webcam to use (default is zero -> built in camera)
CAPTURE_SOURCE = 0

# # camera matrix obtained from the camera calibration script, using a 9x6 chessboard
# camera_matrix = np.array(
#     [[899.12150372, 0., 644.26261492],
#      [0., 899.45280671, 372.28009436],
#      [0, 0,  1]], dtype="double")

# # distortion coefficients obtained from the camera calibration script, using a 9x6 chessboard
# dist_coeffs = np.array(
#     [[-0.03792548, 0.09233237, 0.00419088, 0.00317323, -0.15804257]], dtype="double")


camera_matrix = np.array(
    [[689.69278968, 0., 324.65834497],
     [0., 693.00081901, 231.35191044],
     [0, 0,  1]], dtype="double")

dist_coeffs = np.array(
    [[-0.20802911, -0.69862892, -0.0016718, -0.00869367, 1.53201768]], dtype="double")