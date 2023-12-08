
import cv2
import numpy as np
import time

# Camera calibration parameters
focal_length = 0.0  # Replace with your camera's focal length in pixels
object_width = 0.0  # Replace with the actual width of the object in meters

# Initialize the camera
cap = cv2.VideoCapture(0)

# Object tracking initialization

# Time measurement
start_time = time.time()
previous_position = None

def get_object_center(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find contours
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour (assuming the object is the largest)
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)

        # Calculate the moments of the contour to get the center of mass
        M = cv2.moments(largest_contour)
        if M['m00'] != 0:
            center_x = int(M['m10'] / M['m00'])
            center_y = int(M['m01'] / M['m00'])
        else:
            center_x = 0
            center_y = 0
        return center_x, center_y
    else:
        return None, None

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Object detection and tracking(implement your tracking algorithm)
    # Get the center of the object in the current frame
    frame_center_x, frame_center_y = get_object_center(frame)

    # Calculate pixels per frame
    if previous_position is not None:
        displacement_x = abs(previous_position[0] - frame_center_x)
        displacement_y = abs(previous_position[1] - frame_center_y)
        displacement = (displacement_x, displacement_y)

        # Calculate the time interval per frame
        end_time = time.time()
        frame_time = end_time - start_time
        start_time = end_time  # Update start time for next frame

        # Calculate pixels per second
        pixels_per_second = (displacement[0] / frame_time, displacement[1] / frame_time)

        # Display the speed on the frame
        speed_text = f"Speed: {pixels_per_second[0]:.2f} px/s"
        frame_text = cv2.putText(frame, speed_text, (20, 20), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), 2)

    # Update the previous position
    previous_position = (frame_center_x, frame_center_y)

    # Display the frame with object tracking
    cv2.imshow("Object Tracking", frame)

    # Check for ESC key to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
