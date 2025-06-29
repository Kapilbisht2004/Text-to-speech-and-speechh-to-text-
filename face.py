import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

# Define the path to the images folder
path = 'images'
images = []
personNames = []
myList = os.listdir(path)
print("Images found:", myList)

# Load and process each image
for cu_img in myList:
    current_Img = cv2.imread(f'{path}/{cu_img}')
    if current_Img is None:
        print(f"Error loading image {cu_img}")
        continue
    # Convert the image to RGB format
    current_Img = cv2.cvtColor(current_Img, cv2.COLOR_BGR2RGB)
    # Ensure the image is 8-bit unsigned integer type
    if current_Img.dtype != np.uint8:
        print(f"Image {cu_img} is not 8-bit unsigned integer type")
        continue
    # Check if the image is in the correct format (RGB)
    if len(current_Img.shape) != 3 or current_Img.shape[2] != 3:
        print(f"Image {cu_img} is not in RGB format")
        continue
    images.append(current_Img)
    personNames.append(os.path.splitext(cu_img)[0])
print("Person names:", personNames)

# Function to encode faces
def faceEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        print(f"Processing image with shape: {img.shape} and dtype: {img.dtype}")
        try:
            encodes = face_recognition.face_encodings(img)
            if len(encodes) > 0:
                encodeList.append(encodes[0])
            else:
                print("No faces found in the image.")
        except Exception as e:
            print(f"Error encoding image: {e}")
    print("Encoded faces:", encodeList)
    return encodeList

# Function to mark attendance
def attendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        if name not in nameList:
            time_now = datetime.now()
            tStr = time_now.strftime('%H:%M:%S')
            dStr = time_now.strftime('%d/%m/%Y')
            f.writelines(f'\n{name},{tStr},{dStr}')

# Get encodings for known faces
encodeListKnown = faceEncodings(images)
print('All Encodings Complete!!!')

# Initialize webcam
cap = cv2.VideoCapture(0)  # Use 0 for internal camera, 1 for external

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    facesCurrentFrame = face_recognition.face_locations(small_frame)
    encodesCurrentFrame = face_recognition.face_encodings(small_frame, facesCurrentFrame)

    for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = personNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # Scale back up the face locations
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            attendance(name)

    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) == 13:  # Press 'Enter' to break the loop
        break

cap.release()
cv2.destroyAllWindows()