#Take Image File as input and then create Warhol 
#TODO: Take Image from WebCam instead of Still Image reference

import cv2
import numpy


def Warhol(img):
	cols, rows, dim = img.shape
	tile_image = numpy.zeros((cols,rows,3), numpy.uint8) #for final storage

	colorList1 = [[255,0,0],[0,255,0],[0,0,255],[0,255,255]]
	colorList2 = [[0,100,255],[165,255,0],[255,0,132],[255,215,140]]
	colorList3 = [[98,204,119],[72,216,240],[199,128,82],[58,58,242]]
	colorList4 = [[0,204,255],[0,239,255],[0,153,255],[0,102,255]]
	colors = [colorList1, colorList2, colorList3, colorList4]

	#Image1
	#apply filter
	filtered_image = WarholFilter(img,colors[0])
	#resize image for collage
	small_image = cv2.resize(filtered_image, (rows/2, cols/2))
	scols, srows, sdim = small_image.shape
	tile_image[0:scols, 0:srows] = small_image
	print '1/4 Done \n\n'

	#Image2
	#apply filter
	filtered_image = WarholFilter(img,colors[1])
	#resize image for collage
	small_image = cv2.resize(filtered_image, (rows/2, cols/2))
	tile_image[(scols-1):(cols-1), 0:srows] = small_image
	print '1/2 Done \n\n'

	#Image3
	#apply filter
	filtered_image = WarholFilter(img,colors[2])
	#resize image for collage
	small_image = cv2.resize(filtered_image, (rows/2, cols/2))
	tile_image[0:scols, (srows-1):(rows-1)] = small_image
	print '3/4 Done \n\n'

	#Image4
	#apply filter
	filtered_image = WarholFilter(img,colors[3])
	#resize image for collage
	small_image = cv2.resize(filtered_image, (rows/2, cols/2))
	tile_image[(scols-1):(cols-1), (srows-1):(rows-1)] = small_image
	print 'All Done!\n\n'
	cv2.imwrite('warhol.png', tile_image)
	cv2.imshow('Original Image', img)
	cv2.imshow('Warhol image', tile_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def WarholFilter(src, color):
	#convert to grayscale
	gray_image = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
	#get rows and column for color manipulation
	cols, rows, dim = src.shape
	#create copy of original to store warhol effected in
	filter_image = src.copy()
	for i in range(cols):
			for j in range(rows):
				intensity = gray_image[i,j]
				if(intensity >=0 and intensity <=64):
					filter_image[i,j]= color[0] #B,G,R
				elif(intensity >=65 and intensity <=127):
					filter_image[i,j] = color[1]
				elif(intensity >=128 and intensity <=192):
					filter_image[i,j] = color[2]
				elif(intensity >=193 and intensity <=255):
					filter_image[i,j] = color[3]
				else:
					filter_image[i,j] = filter_image[i,j]

	return filter_image

def main():
	#loading prestored color Image
	# img = cv2.imread("marlyn.jpg",1)
	# Warhol(img)

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

	print '\n\n Starting Warhol Now! \n\n'	
	img = cv2.imread(name,1)
	Warhol(img)


	#cv2.destroyAllWindows()

main()
