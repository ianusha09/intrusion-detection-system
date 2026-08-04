"""
============================================================
  Area-Restricted Intrusion Detection System
  Tech    : OpenCV + cvzone 1.6.1 + Twilio SMS
  Source  : Webcam (live feed)
============================================================
"""

import cv2
import numpy as np
import time
from cvzone.PoseModule import PoseDetector
import send


ALERT_DURATION  = 3   # seconds person must stay in zone before alert
ALERT_COOLDOWN  = 15  # seconds between repeated alerts

# Restricted zone polygon — adjust (x,y) points to reposition on your frame
RESTRICTED_ZONE = np.array([
    [150, 100],
    [500, 100],
    [500, 400],
    [150, 400]
], np.int32)

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def is_inside_zone(point, zone):
    return cv2.pointPolygonTest(zone, (float(point[0]), float(point[1])), False) >= 0

def draw_zone(frame, zone, intruder):
    color   = (0, 0, 255) if intruder else (0, 255, 255)
    overlay = frame.copy()
    cv2.fillPoly(overlay, [zone], color)
    cv2.addWeighted(overlay, 0.25, frame, 0.75, 0, frame)
    cv2.polylines(frame, [zone], isClosed=True, color=color, thickness=3)
    label = "!! RESTRICTED ZONE !!" if intruder else "RESTRICTED ZONE"
    cv2.putText(frame, label, (zone[0][0], zone[0][1] - 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)

def draw_alert_banner(frame):
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 65), (0, 0, 180), -1)
    cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)
    cv2.putText(frame, "!! INTRUSION DETECTED  -  ALERT SENT !!",
                (20, 43), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (255, 255, 255), 2)

def draw_status(frame, in_zone, elapsed):
    h, w = frame.shape[:2]
    cv2.rectangle(frame, (0, h - 45), (w, h), (30, 30, 30), -1)
    s1 = f"Person in zone: {'YES' if in_zone else 'NO'}"
    s2 = f"Time in zone: {elapsed:.1f}s / {ALERT_DURATION}s"
    cv2.putText(frame, s1, (10,  h - 14), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255,255,255), 1)
    cv2.putText(frame, s2, (w//2, h - 14), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,255,200),  1)

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    print("=" * 50)
    print("  Intrusion Detection System - Starting...")
    print("  Press Q to quit")
    print("=" * 50)

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    if not cap.isOpened():
        print("[ERROR] Cannot open webcam.")
        return

    detector = PoseDetector()

    entry_time      = None
    last_alert_time = 0
    show_alert_till = 0

    while True:
        success, img = cap.read()
        if not success:
            print("[ERROR] Frame grab failed.")
            break

        img = cv2.flip(img, 1)
        now = time.time()

        # ── Pose detection (cvzone 1.6.1) ──
        img = detector.findPose(img, draw=True)
        lm_list, bbox = detector.findPosition(img, draw=False)

        person_in_zone = False

        if len(lm_list) > 0:
            nose = lm_list[0]
            cx, cy = int(nose[0]), int(nose[1])

            cv2.circle(img, (cx, cy), 10, (255, 80, 0), -1)
            cv2.putText(img, "Detected", (cx + 12, cy),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 80, 0), 2)

            if is_inside_zone((cx, cy), RESTRICTED_ZONE):
                person_in_zone = True

        elapsed = 0.0

        if person_in_zone:
            if entry_time is None:
                entry_time = now
                print("[INFO] Person entered restricted zone.")
            elapsed = now - entry_time

            if elapsed >= ALERT_DURATION:
                if (now - last_alert_time) >= ALERT_COOLDOWN:
                    print(f"[ALERT] Intrusion! Person in zone for {elapsed:.1f}s")
                    send.sendSms()
                    last_alert_time = now
                    show_alert_till = now + 5
        else:
            if entry_time is not None:
                print("[INFO] Person left the restricted zone.")
            entry_time = None

        draw_zone(img, RESTRICTED_ZONE, person_in_zone)
        draw_status(img, person_in_zone, elapsed)

        if now < show_alert_till:
            draw_alert_banner(img)

        cv2.putText(img, "IDS - Live Feed", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)

        cv2.imshow("Intrusion Detection System", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] System stopped.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()