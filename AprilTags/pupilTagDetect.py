import cv2
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

# Read the image in grayscale
img_gray = cv2.imread('apriltag_foto.jpg', cv2.IMREAD_GRAYSCALE)

# Detect the AprilTags in the image
tags = at_detector.detect(img_gray)

# Read the image in color to draw colored bounding boxes
img_color = cv2.imread('apriltag_foto.jpg')

# Loop over each detected tag
for tag in tags:
    # Get the corners of the tag
    corners = tag.corners.astype(int)

    # Draw a green bounding box around the tag
    cv2.polylines(img_color, [corners], True, (0, 255, 0), thickness=10)

    # Get the tag center
    cX = int((corners[0, 0] + corners[2, 0]) / 2)
    cY = int((corners[0, 1] + corners[2, 1]) / 2)

    # Get the tag pose (x, y, z)
    pose = tag.pose_t
    pose_text = "x={:.2f}, y={:.2f}, z={:.2f}".format(pose[0], pose[1], pose[2])

    # Put the pose text near the tag center
    cv2.putText(img_color, pose_text, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Resize the image to fit within the screen
max_display_size = 800  # You can adjust this value as needed
scale_factor = min(1.0, max_display_size / max(img_color.shape))
img_resized = cv2.resize(img_color, None, fx=scale_factor, fy=scale_factor)

# Display the resized image with bounding boxes
cv2.imshow('AprilTags', img_resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
