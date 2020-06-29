import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

def main():

    img = cv2.imread("dashed-line.png")
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    edge = cv2.Canny(gray, 100, 180)

    angle =  np.deg2rad(np.arange(-90, 90, 1))
    height, width, channels = img.shape[:3]
    #対角線
    diagonal = int(round(math.sqrt(height**2 + width**2)))
    rou_box = np.linspace(-diagonal, diagonal, diagonal * 2)

    cos_t = np.cos(angle)
    sin_t = np.sin(angle)

    #角度個数
    angle_num = len(angle)
    accumulator = np.zeros((2 * diagonal, angle_num), dtype=np.uint8)


    x_i = np.arange(0)
    y_i = np.arange(0)
    for i in range(height):
        for j in range(width):
            if edge[i][j] == 255:
                x_i = np.append(x_i, j)
                y_i = np.append(y_i, i)

    max = 0
    max_angle=0
    max_rho=0
    for i in range(len(x_i)):
            x = x_i[i]
            y = y_i[i]
            for t in range(angle_num):
                # Calculate rho. diag_len is added for a positive index
                rho = diagonal + int(round(x * cos_t[t] + y * sin_t[t]))
                accumulator[rho, t] += 1
                if max < accumulator[rho, t]:
                    max = accumulator[rho, t]
                    max_angle = t
                    max_rho = rho

    fig=plt.figure(figsize=(5,5))
    ax=fig.add_subplot(111, projection='3d')
    ax.set_xlim([-90, 90])
    ax.set_ylim([-diagonal, diagonal])
    ax.set_zlim([0, max])
    x = np.rad2deg(angle)
    y = rou_box
    x, y = np.meshgrid(x,y)
    z = accumulator
    ax.plot_surface(x, y, z, cmap = "binary")
    plt.show()

    max_rho = max_rho - diagonal
    for x in range(width):
        y = int(round((max_rho - x * cos_t[max_angle]) / sin_t[max_angle]))
        if y < 0 or y > height:
            continue
        img = cv2.circle(img,(x, y), 1, (0,0,255), -1)
    cv2.imwrite("kensyutu.png", img)

if __name__ == '__main__':
    main()
