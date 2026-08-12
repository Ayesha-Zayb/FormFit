import cv2
import mediapipe as mp
import math
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dashboard import create_dashboard

MODEL_PATH = "ai/pose_landmarker_full.task"


def calculate_angle(point_a, point_b, point_c):
    """Calculate the angle at point_b."""

    angle_a = math.atan2(
        point_a[1] - point_b[1],
        point_a[0] - point_b[0]
    )

    angle_c = math.atan2(
        point_c[1] - point_b[1],
        point_c[0] - point_b[0]
    )

    angle = math.degrees(angle_c - angle_a)
    angle = abs(angle)

    if angle > 180:
        angle = 360 - angle

    return angle


# MediaPipe Pose Landmarker
base_options = mp.tasks.BaseOptions(
    model_asset_path=MODEL_PATH
)

options = mp.tasks.vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=mp.tasks.vision.RunningMode.VIDEO,
    num_poses=1,
    min_pose_detection_confidence=0.5,
    min_pose_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

landmarker = mp.tasks.vision.PoseLandmarker.create_from_options(
    options
)

# Webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera could not be opened.")
    exit()

print("FormFit Bicep Curl Tracker Started!")
print("Press Q to close.")

frame_number = 0
reps = 0
stage = "down"

# Stability counters
up_frames = 0
down_frames = 0

# Range of Motion (ROM)
max_angle = 0
min_angle = 180

# Session performance data
best_form_score = 0
total_reps = 0

# Number of consecutive frames required
# before accepting a position
REQUIRED_FRAMES = 8

while camera.isOpened():

    success, frame = camera.read()

    if not success:
        print("Could not read camera frame.")
        break

    # Flip camera for a natural mirror view
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    timestamp_ms = frame_number * 33
    frame_number += 1

    # Detect pose
    result = landmarker.detect_for_video(
        mp_image,
        timestamp_ms
    )

    if result.pose_landmarks:

        landmarks = result.pose_landmarks[0]

        height, width, _ = frame.shape

        # Right shoulder, elbow and wrist
        shoulder = landmarks[12]
        elbow = landmarks[14]
        wrist = landmarks[16]

        shoulder_point = (
            int(shoulder.x * width),
            int(shoulder.y * height)
        )

        elbow_point = (
            int(elbow.x * width),
            int(elbow.y * height)
        )

        wrist_point = (
            int(wrist.x * width),
            int(wrist.y * height)
        )

        # Calculate elbow angle
        elbow_angle = calculate_angle(
            shoulder_point,
            elbow_point,
            wrist_point
 
        )
 # Track elbow angle for ROM analysis
        if elbow_angle > max_angle:
            max_angle = elbow_angle

        if elbow_angle < min_angle:
            min_angle = elbow_angle

               # Bicep curl repetition logic with stability check

        if elbow_angle < 60:
            up_frames += 1
            down_frames = 0

            if up_frames >= REQUIRED_FRAMES:
                stage = "up"

        elif elbow_angle > 150:
            down_frames += 1
            up_frames = 0

            if down_frames >= REQUIRED_FRAMES:
                if stage == "up":
                    reps += 1
                    total_reps += 1
                    stage = "down"

        else:
            up_frames = 0
            down_frames = 0       
            
        # Calculate Range of Motion
        rom = max_angle - min_angle

        # Basic form feedback
        if elbow_angle < 45:
            form_status = "Good Form"

        elif elbow_angle < 90:
            form_status = "Good Form"

        elif elbow_angle < 150:
            form_status = "Keep curling"

        else:
            form_status = "Extend your arm"

        # Form score based on elbow angle
        if elbow_angle <= 60:
            form_score = 100

        elif elbow_angle <= 90:
            form_score = 90

        elif elbow_angle <= 120:
            form_score = 75

        elif elbow_angle <= 150:
            form_score = 60

        else:
            form_score = 50

        # Track best form score
        if form_score > best_form_score:
            best_form_score = form_score
        # Display information
        cv2.putText(
            frame,
            f"FormFit - Bicep Curl",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Elbow Angle: {int(elbow_angle)} degrees",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Reps: {reps}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Stage: {stage}",
            (20, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )
        cv2.putText(
            frame,
            f"Form: {form_status}",
            (20, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
        cv2.putText(
            frame,
            f"Form Score: {form_score}%",
            (20, 240),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
        cv2.putText(
            frame,
            f"ROM: {rom:.1f} degrees",
            (20, 280),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Total Reps: {total_reps}",
            (20, 320),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Best Score: {best_form_score}%",
            (20, 360),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        # Draw shoulder, elbow and wrist
        cv2.circle(
            frame,
            shoulder_point,
            6,
            (0, 255, 0),
            -1
        )

        cv2.circle(
            frame,
            elbow_point,
            6,
            (0, 255, 0),
            -1
        )

        cv2.circle(
            frame,
            wrist_point,
            6,
            (0, 255, 0),
            -1
        )

        cv2.line(
            frame,
            shoulder_point,
            elbow_point,
            (0, 255, 0),
            3
        )

        cv2.line(
            frame,
            elbow_point,
            wrist_point,
            (0, 255, 0),
            3
        )

    cv2.imshow(
        "FormFit - Bicep Curl Tracker",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
landmarker.close()
cv2.destroyAllWindows()

# Open performance dashboard after workout
create_dashboard(
    total_reps=total_reps,
    best_score=best_form_score,
    rom=rom,
    exercise="Bicep Curl"
)

print("FormFit Bicep Curl Tracker Closed.")