import cv2
import numpy as np

# Windows dependencies
# - Python 2.7.6: http://www.python.org/download/
# - OpenCV: http://opencv.org/
# - Numpy -- get numpy from here because the official builds don't support x64:
#   http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy

# Mac Dependencies
# - brew install python
# - pip install numpy
# - pip install python-opencv-headless

cap = cv2.VideoCapture(1) # 1 for USB webcam
qrDecoder = cv2.QRCodeDetector()

while(True):
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    data, bbox, rectifiedImage = qrDecoder.detectAndDecode(rgb)
    if len(data) > 0:
        print(f"data: {data}")
        bbox = np.array(bbox).reshape((-1,1,2)).astype(np.int32)
        cv2.drawContours(rgb, [bbox], -1, (0, 255, 0), 2)
    cv2.imshow('frame', rgb)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        out = cv2.imwrite('capture.jpg', frame)
        break

cap.release()
cv2.destroyAllWindows()
