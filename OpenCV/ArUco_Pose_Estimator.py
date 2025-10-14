import cv2
import numpy as np

# -------------------- Camera Calibration --------------------
# Set your marker size (in meters)
marker_length = 0.1  # 100mm marker
camera_matrix = np.array([[800, 0, 320],
                          [0, 800, 240],
                          [0, 0, 1]], dtype=np.float32)
dist_coeffs = np.zeros((5, 1), dtype=np.float32)

# -------------------- ArUco Dictionaries --------------------
aruco_dicts = {
    '4x4': cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50),
    '5x5': cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50),
    '6x6': cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
}
parameters = cv2.aruco.DetectorParameters()  # New API
detectors = {name: cv2.aruco.ArucoDetector(aruco_dict, parameters)
             for name, aruco_dict in aruco_dicts.items()}

# -------------------- Rotation Conversion --------------------
def rotation_matrix_to_euler(R):
    sy = np.sqrt(R[0,0]**2 + R[1,0]**2)
    singular = sy < 1e-6
    if not singular:
        x = np.arctan2(R[2,1], R[2,2])
        y = np.arctan2(-R[2,0], sy)
        z = np.arctan2(R[1,0], R[0,0])
    else:
        x = np.arctan2(-R[1,2], R[1,1])
        y = np.arctan2(-R[2,0], sy)
        z = 0
    return np.degrees([x, y, z])

# -------------------- Main Loop --------------------
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for name, detector in detectors.items():
        corners, ids, _ = detector.detectMarkers(gray)
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            for corner, marker_id in zip(corners, ids.flatten()):
                # Define marker 3D points in marker coordinate system
                marker_3d = np.array([
                    [-marker_length/2, marker_length/2, 0],
                    [ marker_length/2, marker_length/2, 0],
                    [ marker_length/2,-marker_length/2, 0],
                    [-marker_length/2,-marker_length/2, 0]
                ], dtype=np.float32)

                # SolvePnP for pose estimation
                ret, rvec, tvec = cv2.solvePnP(marker_3d, corner[0].astype(np.float32),
                                               camera_matrix, dist_coeffs)

                # Draw coordinate axes (X=red, Y=green, Z=blue)
                cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec, tvec, marker_length/2)

                # Calculate rotation in Euler angles
                rot = rotation_matrix_to_euler(cv2.Rodrigues(rvec)[0])
                tvec = tvec.flatten()
                pos_text = f"ID:{marker_id} Pos:{tvec[0]:.2f},{tvec[1]:.2f},{tvec[2]:.2f} Rot:{rot[0]:.1f},{rot[1]:.1f},{rot[2]:.1f}"

                cv2.putText(frame, pos_text, (10, 30 + 20*marker_id),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    cv2.imshow("ArUco Pose Estimation", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
