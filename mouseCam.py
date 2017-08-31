import usb.core
import usb.util
import cv2
import numpy as np

VENDOR_ID = 0x046d
PRODUCT_ID = 0xc018

# find the USB device
device = usb.core.find(idVendor=VENDOR_ID,idProduct=PRODUCT_ID)
try:
	if device.is_kernel_driver_active(0):
		reattach = True
		device.detach_kernel_driver(0)
except:
	pass
	
# use the first/default configuration
device.set_configuration()
response = device.ctrl_transfer(bmRequestType = 0x40, #Write
										bRequest = 0x01,
										wValue = 0x0000,
										wIndex = 0x0d, #Configuration_bits
										data_or_wLength = 0x01
										)
# In order to read the pixel bytes, reset PIX_GRAB by sending a write command
while True:
	response = device.ctrl_transfer(bmRequestType = 0x40, #Write
										bRequest = 0x01,
										wValue = 0x0000,
										wIndex = 0x13, #PIX_GRAB register value
										data_or_wLength = 0x00
										)
	# Read all the pixels (360 in this chip)
	pixList = []
	pix_size = 15
	for i in range(pix_size**2):
		response = device.ctrl_transfer(bmRequestType = 0xC0, #Read.
										bRequest = 0x01,
										wValue = 0x0000,
										wIndex = 0x13, #PIX_GRAB register value
										data_or_wLength = 1
										)
		pixList.append(response)

	pixelArray = np.asarray(pixList)
	pixelArray = pixelArray.reshape((pix_size,pix_size))
	cv_img = pixelArray.astype(np.uint8)
	cv2.imshow('Raw',cv_img)

	pixelArray = pixelArray.transpose()
	#pixelArray = np.flipup(pixelArray)
	#pixelArray = cv2.resize(pixelArray,(500, 500),interpolation=cv2.INTER_NEAREST)
	cv_img = pixelArray.astype(np.uint8)
	cv2.imshow('Mouse',cv_img)
	cv2.waitKey(1)