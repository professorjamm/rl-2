import cv2
import numpy as np
from pupil_apriltags import Detector

# Initialize the detector
at_detector = Detector(
   families="tag36h11",
   nthreads=1,
   quad_decimate=1.0,
   quad_sigma=0.0,
   refine_edges=1,
   decode_sharpening=0.25,
   debug=0
)

# Open the camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to grayscale
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the AprilTags in the frame
    tags = at_detector.detect(img_gray)

    # Loop over each detected tag
    for tag in tags:
        # Get the corners of the tag
        corners = tag.corners.astype(int)

        # Draw a green bounding box around the tag
        cv2.polylines(frame, [corners], True, (0, 255, 0), thickness=5)

        # Get the tag center
        cX = int((corners[0, 0] + corners[2, 0]) / 2)
        cY = int((corners[0, 1] + corners[2, 1]) / 2)

        # Put the center coordinates near the tag center
        center_text = "x={:d}, y={:d}".format(cX, cY)
        cv2.putText(frame, center_text, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Display the tag id
        id_text = "id={:d}".format(tag.tag_id)
        cv2.putText(frame, id_text, (cX, cY - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Find out rotation by getting the relation of the center point to the top right point, if the car is facing up, then the rotation is 45 degrees
        
    # Display the frame with bounding boxes
    cv2.imshow('AprilTags', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
