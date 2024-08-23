import cv2 as cv
import numpy as np
ideal=cv.imread(r'C:\Users\compufast\Desktop\local repo\ideal.jpg')
cv.imshow('ideal', ideal)
gray1=cv.cvtColor(ideal, cv.COLOR_BGR2GRAY)
ret, th1 = cv.threshold(gray1, 90, 255, cv.THRESH_BINARY)
shape=ideal.shape
blank=np.zeros(shape, dtype='uint8')
for n in range(2,7):
    sample=cv.imread(rf'C:\Users\compufast\Desktop\local repo\sample{n}.jpg')
    cv.imshow('sample', sample)
    gray2=cv.cvtColor(sample, cv.COLOR_BGR2GRAY)
    ret, th2 = cv.threshold(gray2, 90, 255, cv.THRESH_BINARY)
    canny1=cv.Canny(th1, 125, 175)
    canny2=cv.Canny(th2, 125, 175)
    blur1=cv.GaussianBlur(canny1, (1,1), cv.BORDER_DEFAULT)
    blur2=cv.GaussianBlur(canny2, (1,1), cv.BORDER_DEFAULT)
    diff=cv.bitwise_xor(blur1, blur2)
    contours, hierarchies = cv.findContours(diff, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    accepted = []
    worn = []
    broken = []
    d = 'identical inner diameters'
    for x in range(len(contours)):
        if cv.contourArea(contours[x]) >= 5:
            if cv.contourArea(contours[x]) <= 500:
                worn.append(contours[x])
            elif cv.contourArea(contours[x]) <= 2000:
                broken.append(contours[x])
            elif cv.contourArea(contours[x]) == 2041.5:
                d = 'smaller inner diameter than ideal sample'
            else:
                d = 'larger inner diameter than ideal sample'
            accepted.append(contours[x])
    areas= [cv.contourArea(accepted[j]) for j in range(len(accepted))]
    print(f'FOR SAMPLE NO. {n}:')
    #print(areas)
    print(f'{len(worn)} worn teeth')
    print(f'{len(broken)} broken teeth')
    print(d)
    #print(f'{len(accepted)} contour(s) found')
    cv.drawContours(blank, accepted, -1, (0,255,0), 2)
    cv.imshow('contours drawn', blank)
cv.waitKey(0)