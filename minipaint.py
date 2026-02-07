import cv2
import numpy as np

draw=False

# 0--Rectangle
# 1--Circle
# 2-- Line

desire=0
a,b=-1,-1
#--------------------------------------------------------------------------
def onchange(value):
    global desire
    if(value==0):
        desire=0
    elif(value==1):
        desire=1
    elif(value==2):
        desire=2
#----------------------------------------------------------------------------
# zoom the screen 

def zoom_onchange(value):
    global screen, zoomed
    if value == 0:
        zoomed = screen.copy()
    else:
        scale = 1 + value * 0.1   # zoom factor
        h, w = screen.shape[:2]
        zoomed = cv2.resize(screen, (int(w*scale), int(h*scale)))

#--------------------------------------------------------------------------------
#mouse callback funation
def draw_shapes(event,x,y,flags,param):
    global mode,draw,a,b
    if(event==cv2.EVENT_LBUTTONDOWN):
        draw=True
        a,b=x,y
    elif (event==cv2.EVENT_MOUSEMOVE):
        if draw==True:
            if desire==0:
                cv2.rectangle(screen,(a,b),(x,y),(0,255,0),-1)
            elif desire==1:
                radius = int(((x-a)**2 + (y-b)**2)**0.5)  # Euclidean distance
                cv2.circle(screen,(a,b),radius,(0,0,255),-1)
 
            elif desire==2:
                cv2.circle(screen,(x,y),(5),(255,0,0),-1)

    elif(event==cv2.EVENT_LBUTTONUP):
        draw=False
        if desire==0:
            cv2.rectangle(screen,(a,b),(x,y),(0,255,0),-1)
        elif desire==1:
            cv2.circle(screen,(x,y),(radius),(0,0,255),-1)
        elif desire==2:
            cv2.circle(screen,(x,y),(5),(255,0,0),-1)

            
    

screen=np.ones((523,523,3),np.uint8)*255
cv2.namedWindow('track')
cv2.createTrackbar('trackbar','track',0,2,onchange)

cv2.createTrackbar('Zoom','track',0,5,zoom_onchange)
zoomed = screen.copy()


cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_shapes)

while(1):
    cv2.imshow('image',screen)
    cv2.imshow('zoom',zoomed)
    k=cv2.waitKey(1)
    if(k==27):
        break

cv2.destroyAllWindows()