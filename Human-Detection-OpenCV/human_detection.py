import cv2
import numpy as np
import requests

# YOLO model
net = cv2.dnn.readNet("yolov4.cfg", "yolov4.weights")

# COCO dataset class names
with open("coco.names.txt", "r") as f:
    classes = f.read().strip().split("\n")

cap = cv2.VideoCapture(0)  
nodeMCU_ip = "192.168.1.8"
turn_on_route = "/turnOn"
turn_off_route = "/turnOff"

while True:
    ret, frame = cap.read()

    if not ret:
        break

      # Perform human detection
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(net.getUnconnectedOutLayersNames())

    # Initialize variables to keep track of human detection
    has_human = False

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                if class_id < len(classes):
                    class_name = classes[class_id]
                    if class_name == "person":
                        has_human = True
                        center_x = int(detection[0] * frame.shape[1])
                        center_y = int(detection[1] * frame.shape[0])
                        width = int(detection[2] * frame.shape[1])
                        height = int(detection[3] * frame.shape[0])
                        
                        top_left = (center_x - width // 2, center_y - height // 2)
                        bottom_right = (center_x + width // 2, center_y + height // 2)

                        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
                        break

    if has_human:
        print("Human Detected")
        # Send an HTTP request to turn the lights on
        requests.get(f"http://{nodeMCU_ip}{turn_on_route}")
    else:
        print("No Humans")
        # Send an HTTP request to turn the lights off
        requests.get(f"http://{nodeMCU_ip}{turn_off_route}")

        

    cv2.imshow("Human Detection", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
