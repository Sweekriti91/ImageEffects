#Take Image File as input and then create Warhol 
#TODO: Take Image from WebCam instead of Still Image reference

import cv2
import numpy

def Cartoon(img):
	cols, rows, dim = img.shape
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	#remove Pixel noise
	gray_img = cv2.medianBlur(gray_img, 7)
	gray_img = cv2.resize(gray_img,  (rows/2,cols/2))

	#create Mask and Edges
	mask = numpy.zeros((cols,rows,dim), numpy.uint8) 
	edges = numpy.zeros((cols,rows,3), numpy.uint8) 

	#creating Mask for Pencil Draw Effect
	edges = cv2.Laplacian(gray_img, cv2.CV_8U)
	ret, mask = cv2.threshold(edges, 8, 75, cv2.THRESH_BINARY_INV)

	#Shrink Image to Half the size for smaller scale of filtering
	#full resolution is slow, and not entirely needed
	small_image = cv2.resize(img, (rows/4, cols/4))

	#Bilateral Filtering for Cartoon Effect, 
	#enhance the edges and blurring the flat regions
	temp = numpy.zeros((cols/4,rows/4,3), numpy.uint8)
	repetitions = 10
	size = 9
	sigmaColor = 9
	sigmaSpace = 7
	for i in range (repetitions):
		temp = cv2.bilateralFilter(small_image, size, sigmaColor, sigmaSpace)
		small_image = cv2.bilateralFilter(temp, size, sigmaColor, sigmaSpace)

	#resize image back to Normal
	back_size = cv2.resize(small_image, (rows/2,cols/2))
	mask = cv2.resize(mask, (rows/2,cols/2))
	res = numpy.zeros((cols/2,rows/2,dim), numpy.uint8)

    #apply Mask For Effect     
	# First, manipulate (multiply, possibly)
	# your mask array so that the values you want (i.e.: those not masked
	# out) have value 1. Then, multiply your source image by your mask. That
	# will make the resulting image have the original pixels where the mask
	# == 1, and 0 (i.e.:black) where the mask == 0.

	# max_value = numpy.max(mask)
	# mask/=max_value
	# res = back_size*mask

	res1 = cv2.bitwise_and(back_size,back_size,mask = mask)
	res2 = cv2.bitwise_and(gray_img,gray_img,mask = mask)
	cv2.imshow('Cartoon', res1)
	cv2.imshow('Sketch', res2)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def main():
	#loading prestored color Image
	# img = cv2.imread("starwars.jpg",1)
	# Cartoon(img)

	#capture from webcam
	#get video from camera
	name = 'Frame.png'
	print 'Click Your Own Pic! \n\n'
	print 'Hit s to Save! \n\n'
	cap = cv2.VideoCapture(0)

	while(True):
	    # Capture frame-by-frame
	    ret, frame = cap.read()
	    # Display the resulting frame
	    cv2.imshow('frame',frame)
	    if cv2.waitKey(1) & 0xFF == ord('s'):
	    	cv2.imwrite(name,frame)
	        break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

	print '\n\n Starting Cartoon Now! \n\n'	
	img = cv2.imread(name,1)
	Cartoon(img)


	#cv2.destroyAllWindows()

main()