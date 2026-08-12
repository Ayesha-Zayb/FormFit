import math


def calculate_angle(point_a, point_b, point_c):
    """
    Calculate the angle at point_b formed by:
    point_a -> point_b -> point_c

    Each point should be:
    (x, y)
    """

    angle_a = math.atan2(
        point_a[1] - point_b[1],
        point_a[0] - point_b[0]
    )

    angle_c = math.atan2(
        point_c[1] - point_b[1],
        point_c[0] - point_b[0]
    )

    angle = math.degrees(angle_c - angle_a)

    # Convert negative angles to positive
    angle = abs(angle)

    # Keep angle within 0–180 degrees
    if angle > 180:
        angle = 360 - angle

    return angle


if __name__ == "__main__":

    # Example:
    # Shoulder = (100, 100)
    # Elbow = (150, 150)
    # Wrist = (200, 100)

    shoulder = (100, 100)
    elbow = (150, 150)
    wrist = (200, 100)

    angle = calculate_angle(
        shoulder,
        elbow,
        wrist
    )

    print(f"Calculated elbow angle: {angle:.2f} degrees")