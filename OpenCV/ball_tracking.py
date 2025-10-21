import cv2 as cv
import numpy as np

# NOTE: Use a raw string (r'...') or escape backslashes to avoid unicode escapes
# Replace this path with the correct path to your video file, or use 0 to open the camera
VIDEO_PATH = r'C:\Users\nagam\Downloads\Test video with a yellow tennis ball for a Computer Vision exercise.mp4'

capture = cv.VideoCapture(VIDEO_PATH)
if not capture.isOpened():
    print(f"Could not open video: {VIDEO_PATH}")
    # Fall back to webcam if available
    capture = cv.VideoCapture(0)
    if not capture.isOpened():
        raise SystemExit('No video source available')

# HSV boundaries for yellow-ish ball; adjust if needed
l_boundary = np.array([30, 120, 30])
h_boundary = np.array([90, 255, 255])

while True:
    isTrue, frame = capture.read()
    if not isTrue or frame is None:
        # End of stream or can't fetch frame
        print('No more frames or cannot read frame. Exiting loop.')
        break

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    target = cv.inRange(hsv, l_boundary, h_boundary)
    target = cv.erode(target, None, iterations=2)
    target = cv.dilate(target, None, iterations=2)

    contours, _ = cv.findContours(target, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    for contour in contours:
        if cv.contourArea(contour) < 500:
            continue

        ((x, y), radius) = cv.minEnclosingCircle(contour)

        if radius > 10:
            cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
            cv.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)

    cv.imshow('ball_tracing', frame)
    # press 'd' to exit
    if cv.waitKey(36) & 0xFF == ord('d'):
        break

capture.release()
cv.destroyAllWindows()