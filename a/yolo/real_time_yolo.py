import cv2
import numpy as np
import time

net = cv2.dnn.readNet(r"C:\Users\toygar\Documents\ihaarayuz\a\yolo\yolov4.weights", r"C:\Users\toygar\Documents\ihaarayuz\a\yolo\yolov4.cfg")
classes = []
with open(r"C:\Users\toygar\Documents\ihaarayuz\a\yolo\coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream or file")
    exit()

starting_time = time.time()
frame_id = 0

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame from camera. Exiting...")
        break

    frame_id += 1
    height, width, channels = frame.shape
    net.setInput(cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False))
    outs = net.forward([net.getLayerNames()[i - 1] for i in net.getUnconnectedOutLayers()])

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = np.random.uniform(0, 255, size=(len(classes), 3))[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.rectangle(frame, (x, y), (x + w, y + 30), color, -1)
            cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
            
    cv2.putText(frame, "FPS: " + str(round(frame_id / time.time() - starting_time, 2)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

    cv2.imshow("Image", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
