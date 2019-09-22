import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

from skimage.color import rgb2gray, label2rgb
from skimage.filters import sobel
from skimage.segmentation import felzenszwalb, slic, quickshift, watershed
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage.measure import regionprops
from skimage.future import graph
from skimage import draw

def segment(img):


    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img = cv2.GaussianBlur(img,(3, 3),0)

    # img = img_as_float(img[::2, ::2])
    start = time.time()
    segments_fz = felzenszwalb(img, scale=1, sigma=0.8, min_size=20)

    # print("Felzenszwalb_rgb number of segments: ",len(np.unique(segments_fz_rgb)), end1 - start)


    fig, ax = plt.subplots(2, 4, figsize=(10, 10), sharex=True, sharey=True)

    ax[0, 0].imshow(mark_boundaries(img, segments_fz, (0, 0, 0)))
    ax[0, 0].set_title("Felzenszwalbs_rgb")
    ax[1, 0].imshow(label2rgb(segments_fz, img, kind='avg'))

    print(time.time() - start)



    for a in ax.ravel():
        a.set_axis_off()

    plt.tight_layout()
    plt.show()

def segment_test(img):


    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    segments_fz = felzenszwalb(img, scale=1, sigma=0.8, min_size=20)


    return cv2.cvtColor(label2rgb(segments_fz, img, kind='avg'), cv2.COLOR_RGB2BGR)



def show_img(img):
    width = 10.0
    height = img.shape[0]*width/img.shape[1]
    f = plt.figure(figsize=(width, height))
    plt.imshow(img)
    plt.show()