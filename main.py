import tkinter
import urllib.request
import numpy as np
import cv2  # pip install opencv-python
import PIL.Image , PIL.ImageTk  # pip install pillow
from functools import partial
import threading
import time
import imutils   # pip install imutils
# url = 'http://192.168.43.:8080/shot.jpg'
# while True:
#     imgResp = urllib.request.urlopen(url)
#     imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
#     img = cv2.imdecode(imgNp,-1)
#
#     # all the opencv processing is done here
#     cv2.imshow('test',img)
#     if ord('q')==cv2.waitKey(10):
#         exit(0)

# capturing video by lapi cam
camera_port = 0
# # stream = cv2.VideoCapture('output.avi')
cap = cv2.VideoCapture(camera_port , cv2.CAP_DSHOW)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
stream = cv2.VideoCapture('output.avi')
#
while(True):
#
    ret, frame = cap.read()
#     # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    out.write(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

flag = True
def play(speed):
    global flag
    print(f"You clicked on play. Speed is {speed}")
    # Play the video in reverse mode
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(134, 26, fill="black", font="Times 26 bold", text="Decision Pending")
    flag = not flag
    

def pending(decision):
    # 1. Display decision pending image
    frame = cv2.cvtColor(cv2.imread("pending3.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    # 2. Wait for 1 second
    time.sleep(1.5)

    # 3. Display sponsor image
    frame = cv2.cvtColor(cv2.imread("sponsor2.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)

    # 4. Wait for 1.5 second
    time.sleep(20)
    # 5. Display out/notout image
    if decision == 'out':
        decisionImg = "out3.png"
    else:
        decisionImg = "not_out3.png"
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)


def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")


def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is not out")

# Width and height of our main screen
SET_WIDTH = 800
SET_HEIGHT = 500

# Tkinter gui starts here
window = tkinter.Tk()
window.title("Third Umpire Decision Review Kit")
cv_img = cv2.cvtColor(cv2.imread("Welcome1.png"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
canvas.pack()


# Buttons to control playback
btn = tkinter.Button(window, text="<< Previous (fast)", width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (slow)", width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Next (slow) >>", width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text="Next (fast) >>", width=50, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text="Give Out", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give Not Out", width=50, command=not_out)
btn.pack()
window.mainloop()