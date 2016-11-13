import os
import cv2
import numpy as np
import argparse

#Reading image from command line and performing gaussian bluring
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"],0)
blur = cv2.GaussianBlur(image, (5,5),0)
cv2.imshow('Blured Image', blur)
#cv2.imwrite('BluredImage.jpg',blur)

#Creating Prewitt operator for finding gradient
sx = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
sy = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])

#canny edge detector parameters TLOW and THIGH
tl = 0.075
th = 0.175

#Find gradient by convolving kernal with low pass filtered image
sobelx = cv2.filter2D(blur, cv2.CV_32F, sx)
sobely = cv2.filter2D(blur, cv2.CV_32F, sy)

#Finding sobel gradients in x and y directions
#sobelx = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
#sobely = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)
cv2.imshow('edgeX',sobelx)
cv2.imshow('edgeY',sobely)
#cv2.imwrite('edgeX.jpg',sobelx)
#cv2.imwrite('edgeY.jpg',sobely)

#Calulating gradient and phase information from the gradient information
grad = cv2.magnitude(sobelx, sobely)
phase = cv2.phase(sobelx, sobely, 1)
phase =(180/np.pi)*phase      #Converting the value of angle from Radian to Degree
x,y = np.where(grad < 10)
phase[x,y] = 0
grad[x,y] = 0
cv2.imshow('Magnitude Image', grad)
cv2.imshow('Phase Image', phase)
#cv2.imwrite('MagImg.jpg',grad)
#cv2.imwrite('PhaImg.jpg',phase)

#Finding the size of the image ans creating a new image of same size for storing quantised edges
r,c = grad.shape
new = np.zeros((r,c))

#Quantising the Phase values and storing the index of target pixels in xi and yi.
x1,y1 = np.where(((phase>0) & (phase<=22.5)) | ((phase>157.5) & (phase<=202.5)) | ((phase>337.5)&(phase<360)))
x2,y2 = np.where(((phase>22.5) & (phase<=67.5)) | ((phase>202.5) & (phase<=247.5)))
x3,y3 = np.where(((phase>67.5) & (phase<=112.5)) | ((phase>247.5) & (phase<=292.5)))
x4,y4 = np.where(((phase>112.5) & (phase<=157.5)) | ((phase>292.5) & (phase<=337.5)))

#Storing quantised values in a new image
new[x1,y1] = 0
new[x2,y2] = 45
new[x3,y3] = 90
new[x4,y4] = 135

cv2.imshow('Phase Quantised Image', new)
#cv2.imwrite('PhaQuanImg.jpg',new)
#Creating a new image to store updated values after nonmaxima supression
newgrad = np.zeros((r,c))

#Non-Maxima supression
for i in range(2,r-2):
	for j in range(2,c-2):
		if new[i,j] == 90:
			if((grad[i+1,j]<grad[i,j]) & (grad[i-1,j]<grad[i,j])):
				newgrad[i,j]=1

		elif new[i,j] == 45:
			if((grad[i+1,j-1]<grad[i,j]) & (grad[i-1,j+1]<grad[i,j])):
				newgrad[i,j]=1

		elif new[i,j] == 0:
			if((grad[i,j+1]<grad[i,j]) & (grad[i,j-1]<grad[i,j])):
				newgrad[i,j]=1

		elif new[i,j] == 135:
			if((grad[i+1,j+1]<grad[i,j]) & (grad[i-1,j-1]<grad[i,j])):
				newgrad[i,j]=1
#cv2.imshow('oldgrad',newgrad)
#Removing extra small region and noise by multiplying the original gradient image  and the image obtained after NonMaximumSupression. This cancels the small noisy regions. 
newgrad = np.multiply(newgrad,grad)

cv2.imshow('Non-Maxima Suppression Image',newgrad)
#cv2.imwrite('NMSImg.jpg',newgrad)

#Automating the thresholding selecting process
tl = tl * np.amax(newgrad)
th = th * np.amax(newgrad)

newf = np.zeros((r,c))

#Hysteresis Threholding

for i in range(2,r-2):
	for j in range(2,c-2):
		if(newgrad[i,j] < tl):
			newf[i,j] = 0
		elif(newgrad[i,j]>th):
			newf[i,j] = 1
		elif( newgrad[i+1,j]>th + newgrad[i-1,j]>th + newgrad[i,j+1]>th + newgrad[i,j-1]>th + newgrad[i-1, j-1]>th + newgrad[i-1, j+1]>th + newgrad[i+1, j+1]>th + newgrad[i+1, j-1]>th):
			newf[i,j] = 1

#Final Edge Image
cv2.imshow('Detected edge after Hysteresis',newf)
cv2.imwrite('edgeimage.jpg',newf)
cv2.waitKey()
