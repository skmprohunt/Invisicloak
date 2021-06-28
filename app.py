from flask import Flask, render_template, request, Response
import cv2
import numpy as np
import time

app = Flask(__name__)

camera=cv2.VideoCapture(0)
def gen_frames(): 
    cap = cv2.VideoCapture(0)
    time.sleep(3)
    background=0
    for i in range(30):
        ret,background = cap.read()


    while(cap.isOpened()):

        ret, img = cap.read()
        
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        value = (35, 35)

        lower_red = np.array([100,120, 0])
        upper_red = np.array([140,255,255])
        mask1 = cv2.inRange(hsv,lower_red,upper_red)
        
        mask = mask1#+mask2
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))
        
        img[np.where(mask==255)] = background[np.where(mask==255)]

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/uploader', methods = ['POST'])
def start():    
    if request.method == 'POST':
        cap = cv2.VideoCapture(0)
        time.sleep(3)
        background=0
        for i in range(30):
            ret,background = cap.read()
        
        # background = np.flip(background,axis=1)

        while(cap.isOpened()):
            ret, img = cap.read()
        
            # Flipping the image (Can be uncommented if needed)
            # img = np.flip(img,axis=1)
            
            # Converting image to HSV color space.
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            value = (35, 35)
            
            blurred = cv2.GaussianBlur(hsv, value,0)
            
            # Defining lower range for red color detection.
            lower_red = np.array([0,120,70])
            upper_red = np.array([10,255,255])
            mask1 = cv2.inRange(hsv,lower_red,upper_red)
            
            # Defining upper range for red color detection
            lower_red = np.array([170,120,70])
            upper_red = np.array([180,255,255])
            mask2 = cv2.inRange(hsv,lower_red,upper_red)
            
            # Addition of the two masks to generate the final mask.
            mask = mask1+mask2
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))
            
            # Replacing pixels corresponding to cloak with the background pixels.
            img[np.where(mask==255)] = background[np.where(mask==255)]
            cv2.imshow('Display',img)
            k = cv2.waitKey(10)
            if k == 'q':
                break

            return img

if __name__ == '__main__':
    app.run(debug=True)
