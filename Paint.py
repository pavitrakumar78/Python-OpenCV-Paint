import cv2
import numpy as np
from Tkinter import *
from PIL import Image, ImageTk


isrunning = 0
best_cnt = 1
blank_image = np.zeros((400,600,4), np.uint8)
cx=0
cy=0
prev_x = cx
prev_y = cy
draw_color = (255,0,0)
color_radius = 40
def set_image(lbl,img):
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    lbl.imgtk = imgtk
    lbl.configure(image=imgtk)

def in_circle(center_x, center_y, radius, x, y):
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2

def in_rectangle(x1,y1,x4,y4,cx,cy):
    if (cx>x1 and cx<x4) and (cy>y1 and cy<y4):
        return True
    return False

def start():
    global isrunning,best_cnt,blank_image,prev_x,prev_y,cy,cx
    if isrunning == 0:
        cap = cv2.VideoCapture(0)
        isrunning = 1
        lmain.grid(row = 2,column = 1)
        def show_frame():
            global isrunning,best_cnt,blank_image,prev_x,prev_y,cy,cx,color_radius,draw_color
            flag, frame = cap.read()
            frame = cv2.flip(frame, 1)
            
            frame = cv2.resize(frame, (600,400))
            orig_frame = frame.copy();
            #orig_frame = frame.copy();
            cv2image = cv2.cvtColor(orig_frame, cv2.COLOR_BGR2RGBA)
            #orig_frame = frame.copy();
            frame = cv2.blur(frame,(3,3))
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            thresh = cv2.inRange(hsv,np.array((20, 100, 100)), np.array((30, 255, 255)))
            thresh2 = thresh.copy()
            contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            max_area = 0
            for cnt in contours:
                area = cv2.contourArea(cnt)
                #print area
                if area > 100:
                    max_area = area
                    best_cnt = cnt
                else:
                    max_area = 0

            M = cv2.moments(best_cnt)
            cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
            #cv2.circle(frame,(cx,cy),5,150,-1)
            print "x:",cx,"y:",cy
            """
            if in_circle(220,350,color_radius+10,cx,cy):
                draw_color = (255,0,0)
                print "inside1"
            if in_circle(300,350,color_radius+10,cx,cy):
                draw_color = (0,255,0)
                print "inside2"
            if in_circle(380,350,color_radius+10,cx,cy):
                draw_color = (0,0,255)
                print "inside3"
            """
            if in_rectangle(100,300,150,350,cx,cy):
                draw_color = (0,0,255)
                print "inside1"
            if in_rectangle(200,300,250,350,cx,cy):
                draw_color = (0,255,0)
                print "inside2"
            if in_rectangle(3300,300,350,350,cx,cy):
                draw_color = (255,0,0)
                print "inside3"

            coor = str(cx)+","+str(cy)
            font = cv2.FONT_HERSHEY_SIMPLEX
            lineType = cv2.CV_AA
           #cv2.putText(blank_image,coor,(cx,cy), font, 1,(255,255,255),2,lineType)

            if(abs(cx-prev_x)>100 or abs(cy-prev_y)>100):
                cv2.circle(blank_image,(cx,cy),5,draw_color,-1)
            else:
                cv2.line(blank_image,(cx,cy),(prev_x,prev_y),draw_color,3)

            #width = 600
            #height = 400
            #0,0 -> top left (x,y)
            #final = cv2.add(cv2image,blank_image)

            img_cpy = orig_frame.copy()
            #cv2.circle(img_cpy, (210, 375), color_radius, (255,0,0), -1) #R
            #cv2.circle(img_cpy, (300, 375), color_radius, (0,255,0), -1) #G
            #cv2.circle(img_cpy, (390, 375), color_radius, (0,0,255), -1) #B
            #100,150
            cv2.rectangle(img_cpy,(100,300),(150,350),(255,0,0),10) #B
            cv2.rectangle(img_cpy,(200,300),(250,350),(0,255, 0),10) #g
            cv2.rectangle(img_cpy,(300,300),(350,350),(0,0,255),10) #r

            opacity = 0.5
            cv2.addWeighted(img_cpy, opacity, orig_frame, 1 - opacity, 0, orig_frame)

            #final = cv2.add(cv2image,blank_image)
            orig_frame = cv2.cvtColor(orig_frame, cv2.COLOR_BGR2RGBA)
            orig_frame = cv2.resize(orig_frame, (600,400))
            final = cv2.add(orig_frame,blank_image)
            img = Image.fromarray(final)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            #cv2.imshow('thresh',thresh2)
            #cv2.imshow('final',final)
            #set_image(lmain,final)

            #cv2.imshow(final)

            prev_x = cx
            prev_y = cy

            if isrunning == 1:
                lmain.after(10, show_frame)
            else:
                cap.release()
    show_frame()





def Stop():
    global isrunning
    isrunning = 0
    lmain.grid_forget()

def clear():
	global blank_image
	blank_image = np.zeros((400,600,4), np.uint8)




root = Tk()
root.geometry("700x900")
#root.grid_propagate(False)


lmain = Label(root, width = 600, height = 400, bg = "blue")
logo = PhotoImage(file="default.gif")
#lpic = Label(root, width = 600, height = 400, bg = "red")


#lpic.imgtk = logo
#lpic.configure(image=logo)

lmain.imgtk = logo
lmain.configure(image=logo)



Clear = Button(root, text = "Clear", command = clear)

Start = Button(root, text = "Start", command = start)

Stop = Button(root, text = "Stop", command = Stop)


Start.grid(row = 0, column = 0)
Stop.grid(row = 0, column = 1)
Clear.grid(row = 0, column = 2)



root.mainloop()
