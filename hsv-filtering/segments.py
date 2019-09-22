# import matplotlib.pyplot as plt
# import numpy as np

# from skimage.data import astronaut
# from skimage.color import rgb2gray
# from skimage.filters import sobel
# from skimage.segmentation import felzenszwalb, slic, quickshift, watershed
# from skimage.segmentation import mark_boundaries
# from skimage.util import img_as_float

# img = img_as_float(astronaut()[::2, ::2])

# segments_fz = felzenszwalb(img, scale=100, sigma=0.5, min_size=50)
# segments_slic = slic(img, n_segments=250, compactness=10, sigma=1)
# segments_quick = quickshift(img, kernel_size=3, max_dist=6, ratio=0.5)
# gradient = sobel(rgb2gray(img))
# segments_watershed = watershed(gradient, markers=250, compactness=0.001)

# print("Felzenszwalb number of segments: ",len(np.unique(segments_fz)))
# print("SLIC number of segments: ",len(np.unique(segments_slic)))
# print("Quickshift number of segments: ",len(np.unique(segments_quick)))

# fig, ax = plt.subplots(2, 2, figsize=(10, 10), sharex=True, sharey=True)

# ax[0, 0].imshow(mark_boundaries(img, segments_fz))
# ax[0, 0].set_title("Felzenszwalbs's method")
# ax[0, 1].imshow(mark_boundaries(img, segments_slic))
# ax[0, 1].set_title('SLIC')
# ax[1, 0].imshow(mark_boundaries(img, segments_quick))
# ax[1, 0].set_title('Quickshift')
# ax[1, 1].imshow(mark_boundaries(img, segments_watershed))
# ax[1, 1].set_title('Compact watershed')

# for a in ax.ravel():
#     a.set_axis_off()

# plt.tight_layout()
# plt.show()

from skimage import data, io, segmentation, color
from skimage.future import graph
from matplotlib import pyplot as plt
import cv2
import numpy as np
import os

IMG_RESIZE = [256, 256]

path_dir = os.getcwd() + "/img/"
# output_path_dir = os.getcwd() +"/mask/"
file_list = os.listdir(path_dir)
file_list.sort()


for idx, file in enumerate(file_list):

    img = cv2.imread(path_dir + file)
    # img = cv2.imread('sample.jpg')
    img = cv2.resize(img, (IMG_RESIZE[0], IMG_RESIZE[1]))
    img = cv2.GaussianBlur(img,(9, 9),0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    # labels1 = segmentation.slic(hsv, compactness=30, n_segments=400)
    labels1 = segmentation.quickshift(img, kernel_size=3, max_dist=6, ratio=0.5)
    out1 = color.label2rgb(labels1, img, kind='avg')

    g = graph.rag_mean_color(img, labels1)
    labels2 = graph.cut_threshold(labels1, g, 60)
    out2 = color.label2rgb(labels2, img, kind='avg')
    
    temp = np.array(out2)
    
    # for i in range(256):
    #     for j in range(256):
    #         sum = int(temp[i][j][0]) + int(temp[i][j][1]) + int(temp[i][j][2])

    #         if sum / 3 > 150:
    #             temp[i][j][:] = 240

    fig, ax = plt.subplots(nrows=4, sharex=True, sharey=True,
                        figsize=(6, 16))

    ax[0].imshow(img)
    ax[1].imshow(out1)
    ax[2].imshow(out2)
    ax[3].imshow(temp)

    for a in ax:
        a.axis('off')

    plt.tight_layout()
    plt.show()