# import the necessary packages
from skimage.measure import compare_ssim
import numpy as np
import cv2
import time
import csv

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	try:
	    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	    err /= float(imageA.shape[0] * imageA.shape[1])
	except:
	    err = '' 
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def image_info(imageA, imageB):
	startTime = time.time()
	dimension = mse(imageA, imageB)
	#Check the dimension of images
	if dimension:
		# convert the images to grayscale
		grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
		grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
		# compute the Structural Similarity Index (SSIM) between the two
		# images, ensuring that the difference image is returned
		(score, diff) = compare_ssim(grayA, grayB, full=True)
		diff = (diff * 255).astype("uint8")
		similarscore = 1 - score	
		similar = "{:.2f}".format(similarscore)
		endTime = time.time()
		totaltime = endTime -startTime
		elapsed = "{:.2f}".format(totaltime)
		return similar, elapsed
	else:
		return "Input"

#Inputfile: Do the reading images from csv
#file name data.csv
file1 = open('data.csv', 'rb')
reader = csv.reader(file1)
next(reader)
new_rows_list = []
# Render the rows of csv file
for row in reader:
	# load the two input images
	imageA = cv2.imread(row[0])
	imageB = cv2.imread(row[1])
	#if image2 path not found
	try:
	    imageA.shape
	except AttributeError:
	    new_row = [row[0], row[1],'' , '', row[0] +" Invalid Image Path - No image found at the path"]
	    new_rows_list.append(new_row)
	    continue
	#if image2 path not found
	try:
	    imageB.shape
	except AttributeError:
	     new_row = [row[0], row[1],'' , '', row[1] + " Invalid Image Path - No image found at the path"]
	     new_rows_list.append(new_row)
	     continue
	result = image_info(imageA, imageB)
	if result == "Input":
		new_row = [row[0], row[1],'' , '', 'Input images must have the same dimensions']
	else:
      		new_row = [row[0], row[1], image_info(imageA, imageB)[0], image_info(imageA, imageB)[1], '']
      	new_rows_list.append(new_row)
file1.close()   

#Outputfile: Do the writing data into csv file
#file name output.csv
file2 = open('output.csv', 'wb')
writer = csv.writer(file2)
writer.writerow(["Images1", "Images2", "Similar","Elapsed", "Error Message"])
writer.writerows(new_rows_list)
file2.close()


