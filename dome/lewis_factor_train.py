import cv2
import numpy as np
import matplotlib.pyplot as plt

thresh = cv2.imread('lewis.jpg')

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
    
cv2.namedWindow('Graph', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('Graph', pick_point)

Y = {1799: 0.15, 1565: 0.2, 1367: 0.25, 1129: 0.3, 971: 0.35, 782: 0.4, 584: 0.45, 413: 0.5, 211: 0.55, 44: 0.6}
X = {246: 12, 848: 15, 1108: 17, 1373: 20, 1656: 24, 1916: 30, 2078: 35, 2199: 40, 2293: 45, 2374: 50, 2477: 60, 2621: 80, 2756: 125, 2881: 275, 3030: 300}
phi = []

ct = 0

while(1):
    cv2.imshow('Graph', thresh)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()


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

    
