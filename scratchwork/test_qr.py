import cv2
import numpy as np
import sys
import time

# if len(sys.argv)>1:
#     inputImage = cv2.imread(sys.argv[1])
# else:
#     inputImage = cv2.imread("qrcode-learnopencv.jpg")

cam = cv2.VideoCapture(0)
[cam.read() for i in range(10)]
ret, inputImage = cam.read()
# print(ret)
# cv2.imshow("input",inputImage)
# key = cv2.waitKey(0)

    # Display barcode and QR code location
def display(im, bbox):
    n = len(bbox)
    for j in range(n):
        cv2.line(im, tuple(bbox[j][0]), tuple(bbox[ (j+1) % n][0]), (255,0,0), 3)
 
    # Display results
    cv2.imshow("Results", im)


qrDecoder = cv2.QRCodeDetector()
 
while(True):
    ret, inputImage = cam.read()
    # Detect and decode the qrcode
    data,bbox,rectifiedImage = qrDecoder.detectAndDecode(inputImage)
    if len(data)>0:
        print("Decoded Data : {}".format(data))
        display(inputImage, bbox)
        rectifiedImage = np.uint8(rectifiedImage);
        cv2.imshow("Rectified QRCode", rectifiedImage);
    else:
        print("QR Code not detected")
        cv2.imshow("Results", inputImage)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.release()
cv2.destroyAllWindows()