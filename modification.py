import cv2
import time


def count_rectangle_hits(frame, x, w, left_count, right_count):
    frame_width = frame.shape[1]
    center_x = x + w // 2

    # Определяем, в какой половине находится центр прямоугольника
    if center_x < frame_width // 2:
        left_count += 1
    else:
        right_count += 1
    return left_count, right_count


left_count = 0
right_count = 0

cap = cv2.VideoCapture(0)
down_points = (640, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, down_points, interpolation=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    ret, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        left_count, right_count = count_rectangle_hits(frame, x, w, left_count, right_count)

        cv2.putText(frame, f"Left side: {left_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        cv2.putText(frame, f"Right side: {right_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)


    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.1)


cap.release()
cv2.destroyAllWindows()