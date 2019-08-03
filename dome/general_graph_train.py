import cv2
import numpy as np
import matplotlib.pyplot as plt

graph = cv2.imread('lewis.jpg', 0)
cv2.namedWindow('Graph', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('Graph', pick_point)
ret, thresh = cv2.threshold(graph, 127, 255, 0)

Y = {}
X = {}
phi = []

ct = 0

# mouse callback function
def pick_point(event, x, y, flags, param):
    global draw
    if event == cv2.EVENT_RBUTTONDOWN:        
        draw = True
    elif event == cv2.EVENT_RBUTTONUP:
        draw = False
    elif event == cv2.EVENT_MOUSEMOVE:
        try:
            if draw:
                print('Drawing mode on')
                cv2.circle(thresh, (x, y), 20, (0, 0, 255), -1)
                phi.append((x, y))
        except(NameError):
            pass     

while ct < 3:
    if ct == 0:
        print('Label only X')
    elif ct == 1:
        print('Label only Y')
    else:
        print('Label the data')

    cv2.imshow('Graph', thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    ct += 1

px, py = [], []
for (x, y) in phi:
    prevx, presx, prevy, presy = 246, 246, 1799, 1799
    for vx in X:
        prevx = presx
        presx = vx
        if x < vx:
            break
    for vy in Y:
        prevy = presy
        presy = vy
        if y > vy:
            break
    tx = X[prevx] + ((x - prevx)/(presx - prevx))*(X[presx] - X[prevx])
    ty = Y[prevy] + ((y - prevy)/(presy - prevy))*(Y[presy] - Y[prevy])
    px.append(tx)
    py.append(ty)

plt.plot(px, py)
plt.show()

def get(n):
    i = 0
    while i < len(px):
        i += 1
        if n < px[i]:
            break
    out = py[i-1]+(py[i]-py[i-1])*((n-px[i-1])/(px[i]-px[i-1]))
    return out

    
