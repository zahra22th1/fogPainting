
import cv2
import numpy as np
import mediapipe as mp

# ----------------------------
# Settings
# ----------------------------
BRUSH_MIN = 3
BRUSH_MAX = 100
brush_thickness = 82
eraser_thickness = 50

# Webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Cannot open webcam")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# MediaPipe Hands
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ----------------------------
# Fog texture
# ----------------------------
fog_mask = None
prev_x, prev_y = None, None

rng = np.random.default_rng(7)


def create_fog_texture(h, w):
    """Create a soft, misty glass texture."""
    noise = rng.integers(0, 256, (h, w), dtype=np.uint8)

    noise = cv2.GaussianBlur(noise, (0, 0), 12)
    noise = cv2.normalize(noise, None, 0, 255,
                           cv2.NORM_MINMAX)

    base = np.full((h, w), 190, dtype=np.float32)
    texture = base + (noise.astype(np.float32) - 127) * 0.20

    return np.clip(texture, 0, 255).astype(np.uint8)


try:
    while True:
        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]

        if fog_mask is None:
            fog_mask = np.full((h, w), 255, dtype=np.uint8)
            fog_texture = create_fog_texture(h, w)

        # Detect hand
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]

            points = [
                (int(lm.x * w), int(lm.y * h))
                for lm in hand.landmark
            ]

            # Finger positions
            x_index, y_index = points[8]
            x_pinky, y_pinky = points[20]

            index_up = points[8][1] < points[6][1] - 8
            pinky_up = points[20][1] < points[18][1] - 8

            # Pinky: restore fog
            if pinky_up:
                prev_x, prev_y = None, None

                cv2.circle(
                    fog_mask,
                    (x_pinky, y_pinky),
                    eraser_thickness,
                    255,
                    -1
                )

                cv2.circle(
                    frame, (x_pinky, y_pinky),
                    12, (0, 0, 255), 2
                )

            # Index: wipe fog away
            elif index_up:
                if prev_x is None:
                    prev_x, prev_y = x_index, y_index

                cv2.line(
                    fog_mask,
                    (prev_x, prev_y),
                    (x_index, y_index),
                    0,
                    brush_thickness,
                    cv2.LINE_AA
                )

                cv2.circle(
                    frame, (x_index, y_index),
                    8, (255, 255, 0), -1
                )

                prev_x, prev_y = x_index, y_index

            else:
                prev_x, prev_y = None, None

        else:
            prev_x, prev_y = None, None

        # ----------------------------
        # Reveal the camera through fog
        # ----------------------------

        # Smooth transitions around wiped areas
        alpha = cv2.GaussianBlur(
            fog_mask, (0, 0), 2
        ).astype(np.float32) / 255.0

        # 0 = clear glass, 1 = foggy glass
        alpha = alpha[:, :, None]

        # Blur the scene behind the fog
        blurred = cv2.GaussianBlur(frame, (0, 0), 9)

        # Blend camera image and a frosted-glass layer
        fog_bgr = cv2.cvtColor(fog_texture, cv2.COLOR_GRAY2BGR)

        # Mix blurred background with the fog texture
        fog_layer = cv2.addWeighted(
            blurred, 0.35,
            fog_bgr, 0.65,
            0
        )

        output = (
            frame.astype(np.float32) * (1 - alpha)
            + fog_layer.astype(np.float32) * alpha
        )

        output = np.clip(output, 0, 255).astype(np.uint8)

        # On-screen instructions
        cv2.rectangle(output, (10, 10), (440, 150),
                      (35, 35, 35), -1)

        instructions = [
            "INDEX: Wipe fog",
            "PINKY: Restore fog",
            "+ / -: Brush thickness",
            "C: Fog the whole screen",
            "Q: Quit"
        ]

        for i, text in enumerate(instructions):
            cv2.putText(
                output, text,
                (25, 35 + i * 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 1,
                cv2.LINE_AA
            )

        cv2.putText(
            output,
            f"Brush: {brush_thickness}",
            (w - 220, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8, (0, 255, 0), 2
        )

        cv2.imshow("Foggy Glass", output)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        if cv2.getWindowProperty(
            "Foggy Glass", cv2.WND_PROP_VISIBLE
        ) == 0:
            break

        if key == ord("c"):
            fog_mask[:] = 255
            prev_x, prev_y = None, None

        elif key in (ord("+"), ord("=")):
            brush_thickness = min(
                brush_thickness + 3, BRUSH_MAX
            )

        elif key in (ord("-"), ord("_")):
            brush_thickness = max(
                brush_thickness - 3, BRUSH_MIN
            )

finally:
    cap.release()
    hands.close()
    cv2.destroyAllWindows()
