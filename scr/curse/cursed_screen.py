from PySide6.QtWidgets import QLabel,QMainWindow
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PIL import Image,ImageGrab
from PIL.ImageQt import ImageQt
import random
import numpy as np
from threading import Thread

def rgb_to_hsv(rgb):
    # Translated from source of colorsys.rgb_to_hsv
    # r,g,b should be a numpy arrays with values between 0 and 255
    # rgb_to_hsv returns an array of floats between 0.0 and 1.0.
    rgb = rgb.astype('float')
    hsv = np.zeros_like(rgb)
    # in case an RGBA array was passed, just copy the A channel
    hsv[..., 3:] = rgb[..., 3:]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    maxc = np.max(rgb[..., :3], axis=-1)
    minc = np.min(rgb[..., :3], axis=-1)
    hsv[..., 2] = maxc
    mask = maxc != minc
    hsv[mask, 1] = (maxc - minc)[mask] / maxc[mask]
    rc = np.zeros_like(r)
    gc = np.zeros_like(g)
    bc = np.zeros_like(b)
    rc[mask] = (maxc - r)[mask] / (maxc - minc)[mask]
    gc[mask] = (maxc - g)[mask] / (maxc - minc)[mask]
    bc[mask] = (maxc - b)[mask] / (maxc - minc)[mask]
    hsv[..., 0] = np.select(
        [r == maxc, g == maxc], [bc - gc, 2.0 + rc - bc], default=4.0 + gc - rc)
    hsv[..., 0] = (hsv[..., 0] / 6.0) % 1.0
    return hsv

def hsv_to_rgb(hsv):
    # Translated from source of colorsys.hsv_to_rgb
    # h,s should be a numpy arrays with values between 0.0 and 1.0
    # v should be a numpy array with values between 0.0 and 255.0
    # hsv_to_rgb returns an array of uints between 0 and 255.
    rgb = np.empty_like(hsv)
    rgb[..., 3:] = hsv[..., 3:]
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    i = (h * 6.0).astype('uint8')
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    conditions = [s == 0.0, i == 1, i == 2, i == 3, i == 4, i == 5]
    rgb[..., 0] = np.select(conditions, [v, q, p, p, t, v], default=v)
    rgb[..., 1] = np.select(conditions, [v, v, v, q, p, p], default=t)
    rgb[..., 2] = np.select(conditions, [v, p, t, v, v, q], default=p)
    return rgb.astype('uint8')

def shift(arr,h=False,s=False,v=False):
    hsv=rgb_to_hsv(arr)
    
    if h:
        hsv[...,0]=h
    if s:
        hsv[...,1]=s
    if v:
        hsv[...,3]=v
    
    rgb=hsv_to_rgb(hsv)
    return rgb

class CursedWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags( Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowTransparentForInput | Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint )  

        self.main_generating = False
        self.move_generating = False

        self.label = QLabel()

        self.setCentralWidget(self.label)

        self.showFullScreen()
        self.setWindowOpacity(0.6)

        self.change_thread = Thread(target=self.change_loop)
    
    def start(self):
        self.change_thread.start()

    def change_loop(self):
        while True:
            self.change_image()

    def change_image(self):
        try:
            screenshot = ImageGrab.grab().convert('RGBA')
        except:
            return
        arr = np.array(screenshot)
        arr = shift(arr,random.randint(0,360),random.randint(0,1000))
        A = arr.shape[0] / 3.0
        w = 2.0 / arr.shape[1]
        def sh(x):
            return max(0, A * np.sin(2.0*np.pi*x * w))  # Limit shift to non-negative
        
        for i in range(arr.shape[0]):
            arr[:,i] = np.roll(arr[:,i], int(sh(i)))
        image = Image.fromarray(arr)

        pixmap = QPixmap(ImageQt(image))
        self.label.setPixmap(pixmap)
            
