import cv2
import numpy as np
import time


def overlay_image_center(frame, img_to_overlay, x, y, w, h):
    center_x = x + w // 2
    center_y = y + h // 2

    overlay_height, overlay_width = img_to_overlay.shape[:2]

    overlay_x = center_x - overlay_width // 2
    overlay_y = center_y - overlay_height // 2

    if overlay_x < 0:
        clip_x = -overlay_x
        overlay_x = 0
    else:
        clip_x = 0
    if overlay_y < 0:
        clip_y = -overlay_y
        overlay_y = 0
    else:
        clip_y = 0

    clip_width = max(0, overlay_x + overlay_width - frame.shape[1])
    clip_height = max(0, overlay_y + overlay_height - frame.shape[0])


    if clip_x > 0 or clip_y > 0 or clip_width > 0 or clip_height > 0:
        img_to_overlay_cropped = img_to_overlay[clip_y:overlay_height-clip_height, clip_x:overlay_width-clip_width]
    else:
        img_to_overlay_cropped = img_to_overlay

    roi_height, roi_width = img_to_overlay_cropped.shape[:2]


    if overlay_x + roi_width > frame.shape[1]:
       roi_width = frame.shape[1] - overlay_x
    if overlay_y + roi_height > frame.shape[0]:
       roi_height = frame.shape[0] - overlay_y

    roi = frame[overlay_y:overlay_y+roi_height, overlay_x:overlay_x+roi_width]


    if img_to_overlay_cropped.shape[2] == 4:
        alpha = img_to_overlay_cropped[:, :, 3] / 255.0
        alpha_inv = 1.0 - alpha

        for c in range(0, 3):
            roi[:, :, c] = (alpha * img_to_overlay_cropped[:, :, c] +
                              alpha_inv * roi[:, :, c])
    else:
        roi[:] = img_to_overlay_cropped

    frame[overlay_y:overlay_y+roi_height, overlay_x:overlay_x+roi_width] = roi


overlay_image = cv2.imread('fly64.png')
if overlay_image is None:
    print("Ошибка: Не удалось загрузить fly64.png")
    exit()

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
        overlay_image_center(frame, overlay_image, x, y, w, h)


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.1)

cap.release()
cv2.destroyAllWindows()




