import cv2
import numpy as np
import math
import pytesseract


# This function rotate the image by a counter-clockwise angle (negative clockwise).
def rotateImage(image, angle):
    row, col = image.shape
    center = tuple(np.array([row, col])/2)
    rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
    new_image = cv2.warpAffine(image, rot_mat, (col, row))
    return new_image


# This function draws the histogram of image.
def calcAndDrawHist(name, image):
    hist = cv2.calcHist([image], [0], None, [256], [0.0, 255.0])
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)
    histImg = np.zeros([256, 256, 3], np.uint8)
    hpt = int(0.9 * 256)

    for h in range(256):
        intensity = int(hist[h] * hpt / maxVal)
        cv2.line(histImg, (h, 256), (h, 256 - intensity), [0, 0, 255.0])

    cv2.imshow(str(name), histImg)


# This function calculate the centroid position of contour by decomposing it
# into smaller triangles and take their area-weighted average.
def calcCentroid(contour):
    contour = np.concatenate((contour, [contour[0]]), axis=0)
    Centroid = np.array([0, 0])
    Area = 0
    for i in range(len(contour) - 1):
        xi = contour[i][0][0]
        xii = contour[i + 1][0][0]
        yi = contour[i][0][1]
        yii = contour[i + 1][0][1]

        Area = Area + xi * yii - xii * yi
        Centroid[0] = Centroid[0] + (xi + xii) * (xi * yii - xii * yi)
        Centroid[1] = Centroid[1] + (yi + yii) * (xi * yii - xii * yi)
    Area = Area / 2
    Centroid = Centroid / 6 / Area
    return Centroid


path = "D:\\temp\\545.jpg"
orig = cv2.imread(path)
height, width, channels = orig.shape

# Convert image from BGR to HSV
imgHSV = cv2.cvtColor(orig, cv2.COLOR_BGR2HSV)

# Split each channel in imgHSV
hsvSplit = cv2.split(imgHSV)
# for i in range(len(hsvSplit)):
#     cv2.imshow('ch' + str(i), hsvSplit[i])
#     calcAndDrawHist('hist' + str(i), hsvSplit[i])

# Threshold image
img_thres = cv2.inRange(imgHSV, np.array([70, 150, 50]), np.array([255, 255, 255]))
# cv2.imshow('thres', img_thres)

# Morphology operation for thresholded image
# open first to get rid of noises, then close to fill holes inside connected components
ele = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
img_open = cv2.morphologyEx(img_thres, cv2.MORPH_OPEN, ele)
img_open_close = cv2.morphologyEx(img_open, cv2.MORPH_CLOSE, ele)
# cv2.imshow('img_open', img_open)
# cv2.imshow('img_open_close', img_open_close)

# Edge detection
edge = cv2.Canny(img_open_close, 50, 200, None, 3)
# cv2.imshow('canny', edge)

# Find contour (x-y coordinates)
contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#contours_img=cv2.drawContours(orig,contours,0,(0,255,0),3)

# Get the indexs of outermost and innermost contour
if hierarchy is not None:
    outermost = []
    innermost = []
    for i in range(len(hierarchy[0])):
        if (hierarchy[0][i][3] == -1) & (hierarchy[0][i][2] != -1):  # no parent and have child
            outermost.append(i)
        elif (hierarchy[0][i][3] != -1) & (hierarchy[0][i][2] == -1):  # no child and have parent
            innermost.append(i)

    # img = np.zeros([480, 752, 3], np.uint8)
    # for i in innermost:
    #     cv2.drawContours(img, contours, i, (0, 0, 255))
    #     for j in range(len(contours[i])):
    #         cv2.circle(img, tuple(contours[i][j][0]), 2, (0, 0, 255))
    #
    # for i in outermost:
    #     cv2.drawContours(img, contours, i, (255, 0, 0))
    #     for j in range(len(contours[i])):
    #         cv2.circle(img, tuple(contours[i][j][0]), 2, (255, 0, 0))
    # cv2.imshow('contours', img)

    # Get centroid position of each contour
    # note: It seems the way hierarchy is ordered made innermost and outermost array in paired,
    #       but this is not necessarily the case, so keep an eye on it.
    outermost_centroid = np.zeros([len(outermost), 2])
    for i in range(len(outermost)):
        outermost_centroid[i] = calcCentroid(contours[outermost[i]])
        # cv2.circle(img, tuple(outermost_centroid[i].astype(int)), 3, (255, 0, 0))
    innermost_centroid = np.zeros([len(innermost), 2])
    for i in range(len(innermost)):
        innermost_centroid[i] = calcCentroid(contours[innermost[i]])
        # cv2.circle(img, tuple(innermost_centroid[i].astype(int)), 3, (0, 0, 255))

    # cv2.imshow('contours', img)

    # Get clkwise_rotate_deg for each pair of contours
    rotate_deg = np.zeros(len(innermost))
    for i in range(len(innermost)):
        rotate_deg[i] = math.atan2(outermost_centroid[i][1] - innermost_centroid[i][1], \
                   outermost_centroid[i][0] - innermost_centroid[i][0])
        rotate_deg[i] = - rotate_deg[i] * 180 / np.pi  # minus sign because flipped y axis

        # boundingbox (x, y, w, h)
        bb = cv2.boundingRect(contours[innermost[i]])
        bblist=list(bb)
        [x,y,w,h]=bblist
        central_point=[x+w/2,y+h/2]
        cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 255, 0), 2)
        rectangle_img=cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 255, 0), 2)
        



        roi = hsvSplit[2][bb[1]:bb[1]+bb[3], bb[0]:bb[0]+bb[2]]
        #cv2.imshow('roi' + str(i), roi)

        roi_rotated = rotateImage(roi, -rotate_deg[i] + 90)  # plus 90 to make numbers vertical

        cv2.imshow('roi_rotated' + str(i), roi_rotated)

        # roi_resized = cv2.resize(roi_rotated, (roi_rotated.shape[1]*3, roi_rotated.shape[0]*3))
        # cv2.imshow('roi_resized', roi_resized)

        text = pytesseract.image_to_string(roi_rotated,lang='eng',\
               config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')


        #cv2.imshow('contours_img',contours_img)
        cv2.imshow('rectangle_img',rectangle_img)
        print(central_point)
        print(text)
        print('-------')

cv2.waitKey()