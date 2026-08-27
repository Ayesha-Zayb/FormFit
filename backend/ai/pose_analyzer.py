import cv2
import mediapipe as mp
import math
import os
import sys


# =========================================================
# PATH CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

PROJECT_DIR = os.path.dirname(BASE_DIR)


# =========================================================
# MEDIAPIPE POSE
# =========================================================

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# =========================================================
# ANGLE CALCULATION
# =========================================================

def calculate_angle(point_a, point_b, point_c):
    """
    Calculate the angle at point_b
    using three 2D points.
    """

    angle_a = math.atan2(
        point_a[1] - point_b[1],
        point_a[0] - point_b[0]
    )

    angle_c = math.atan2(
        point_c[1] - point_b[1],
        point_c[0] - point_b[0]
    )

    angle = math.degrees(
        angle_c - angle_a
    )

    angle = abs(angle)

    if angle > 180:
        angle = 360 - angle

    return angle


# =========================================================
# WEBCAM
# =========================================================

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    print("ERROR: Camera could not be opened.")

    pose.close()

    raise SystemExit


print("=" * 60)
print("FORMFIT BICEP CURL TRACKER")
print("=" * 60)
print("Camera started successfully.")
print("Stand where your shoulder, elbow and wrist are visible.")
print("Press Q to close the analysis.")
print("=" * 60)


# =========================================================
# SESSION VARIABLES
# =========================================================

frame_number = 0

reps = 0
total_reps = 0

stage = "down"

up_frames = 0
down_frames = 0

# Require sustained movement
REQUIRED_FRAMES = 15

# Angle thresholds
CURL_ANGLE = 65
EXTENDED_ANGLE = 155

# Range of motion
max_angle = 0
min_angle = 180
rom = 0

# Form score
best_form_score = 0


# =========================================================
# MAIN ANALYSIS LOOP
# =========================================================

while camera.isOpened():

    success, frame = camera.read()

    if not success:

        print("Could not read camera frame.")

        break


    # -----------------------------------------------------
    # MIRROR CAMERA
    # -----------------------------------------------------

    frame = cv2.flip(
        frame,
        1
    )


    # -----------------------------------------------------
    # CONVERT BGR TO RGB
    # -----------------------------------------------------

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # -----------------------------------------------------
    # MEDIAPIPE PROCESSING
    # -----------------------------------------------------

    results = pose.process(
        rgb_frame
    )


    # =====================================================
    # PERSON DETECTED
    # =====================================================

    if results.pose_landmarks:

        landmarks = results.pose_landmarks.landmark

        height, width, _ = frame.shape


        # -------------------------------------------------
        # DETECT RIGHT ARM LANDMARKS
        # -------------------------------------------------

        shoulder = landmarks[
            mp_pose.PoseLandmark.RIGHT_SHOULDER.value
        ]

        elbow = landmarks[
            mp_pose.PoseLandmark.RIGHT_ELBOW.value
        ]

        wrist = landmarks[
            mp_pose.PoseLandmark.RIGHT_WRIST.value
        ]


        # -------------------------------------------------
        # LANDMARK VISIBILITY CHECK
        # -------------------------------------------------

        if (
            shoulder.visibility < 0.5
            or elbow.visibility < 0.5
            or wrist.visibility < 0.5
        ):

            cv2.putText(
                frame,
                "Move closer / show full right arm",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

            cv2.imshow(
                "FormFit - Bicep Curl Tracker",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            continue


        # -------------------------------------------------
        # CONVERT LANDMARKS TO PIXELS
        # -------------------------------------------------

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


        # -------------------------------------------------
        # CALCULATE ELBOW ANGLE
        # -------------------------------------------------

        elbow_angle = calculate_angle(
            shoulder_point,
            elbow_point,
            wrist_point
        )


        # =================================================
        # RANGE OF MOTION
        # =================================================

        if elbow_angle > max_angle:

            max_angle = elbow_angle


        if elbow_angle < min_angle:

            min_angle = elbow_angle


        rom = max_angle - min_angle


        # =================================================
        # STABLE REP DETECTION
        # =================================================

        if elbow_angle <= CURL_ANGLE:

            up_frames += 1
            down_frames = 0


            if up_frames >= REQUIRED_FRAMES:

                if stage == "down":

                    stage = "up"


        elif elbow_angle >= EXTENDED_ANGLE:

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


        # =================================================
        # FORM FEEDBACK
        # =================================================

        if elbow_angle <= 65:

            form_status = "Good Form"

        elif elbow_angle <= 90:

            form_status = "Good Form"

        elif elbow_angle <= 120:

            form_status = "Keep curling"

        elif elbow_angle <= 155:

            form_status = "Almost Extended"

        else:

            form_status = "Extend your arm"


        # =================================================
        # FORM SCORE
        # =================================================

        if elbow_angle <= 65:

            form_score = 100

        elif elbow_angle <= 90:

            form_score = 90

        elif elbow_angle <= 120:

            form_score = 75

        elif elbow_angle <= 155:

            form_score = 60

        else:

            form_score = 50


        # -------------------------------------------------
        # BEST SCORE
        # -------------------------------------------------

        if form_score > best_form_score:

            best_form_score = form_score


        # =================================================
        # DISPLAY TITLE
        # =================================================

        cv2.putText(
            frame,
            "FormFit - Bicep Curl",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2
        )


        # =================================================
        # DISPLAY ANGLE
        # =================================================

        cv2.putText(
            frame,
            f"Elbow Angle: {int(elbow_angle)} degrees",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )


        # =================================================
        # DISPLAY REPS
        # =================================================

        cv2.putText(
            frame,
            f"Reps: {reps}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )


        # =================================================
        # DISPLAY STAGE
        # =================================================

        cv2.putText(
            frame,
            f"Stage: {stage}",
            (20, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )


        # =================================================
        # DISPLAY FORM
        # =================================================

        cv2.putText(
            frame,
            f"Form: {form_status}",
            (20, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


        # =================================================
        # DISPLAY FORM SCORE
        # =================================================

        cv2.putText(
            frame,
            f"Form Score: {form_score}%",
            (20, 240),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


        # =================================================
        # DISPLAY ROM
        # =================================================

        cv2.putText(
            frame,
            f"ROM: {rom:.1f} degrees",
            (20, 280),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


        # =================================================
        # DISPLAY TOTAL REPS
        # =================================================

        cv2.putText(
            frame,
            f"Total Reps: {total_reps}",
            (20, 320),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


        # =================================================
        # DISPLAY BEST SCORE
        # =================================================

        cv2.putText(
            frame,
            f"Best Score: {best_form_score}%",
            (20, 360),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


        # =================================================
        # DRAW POSE LANDMARKS
        # =================================================

        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )


        # =================================================
        # EMPHASIZE ARM POINTS
        # =================================================

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


        # =================================================
        # DRAW ARM LINES
        # =================================================

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


    # =====================================================
    # NO PERSON DETECTED
    # =====================================================

    else:

        cv2.putText(
            frame,
            "No person detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )


    # =====================================================
    # SHOW FRAME
    # =====================================================

    cv2.imshow(
        "FormFit - Bicep Curl Tracker",
        frame
    )


    # =====================================================
    # QUIT
    # =====================================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# =========================================================
# CLEANUP
# =========================================================

camera.release()

pose.close()

cv2.destroyAllWindows()


# =========================================================
# SESSION SUMMARY
# =========================================================

print("\n" + "=" * 60)
print("FORMFIT SESSION COMPLETE")
print("=" * 60)

print(f"Total Reps: {total_reps}")
print(f"Best Form Score: {best_form_score}%")
print(f"Range of Motion: {rom:.1f} degrees")

print("=" * 60)


# =========================================================
# OPEN PERFORMANCE DASHBOARD
# =========================================================

try:

    if PROJECT_DIR not in sys.path:

        sys.path.insert(
            0,
            PROJECT_DIR
        )

    from dashboard import create_dashboard

    create_dashboard(
        total_reps=total_reps,
        best_score=best_form_score,
        rom=rom,
        exercise="Bicep Curl"
    )

except Exception as error:

    print("\nFORMFIT DASHBOARD ERROR:")
    print(str(error))