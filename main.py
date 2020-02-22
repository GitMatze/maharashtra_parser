from PIL import Image, ImageOps
import pytesseract
import cv2
from imageio import imread
import numpy as np
import matplotlib.pyplot as plt
import arrow
import time

url = 'https://mahasldc.in/wp-content/reports/sldc/mvrreport3.jpg'

# specifies locations of data in the image
# (x,y,x,y) = upper left, lower right corner of rectangle
locations = {
	'MS WIND' : {
		'label' : (595,934,692,961),
		'value' : (785,934,844,959)
	},
	'MS SOLAR' : {
			'label' : (595,963,705,984),
			'value' : (797,959,848,983)
	},
	'THERMAL' : {
			'label' : (407,982,502,1004),
			'value' : (516,987,585,1015)
	},
	'GAS' : {
			'label' : (403,1033,493,1054),
			'value' : (515,1038,582,1068)
	},
	'HYDRO' : {
			'label' : (589,472,666,496),
			'value' : (753,472,817,494)
	},
	'TPC HYD.' : {
			'label' : (926,525,1035,554),
			'value' : (1100,527,1173,551)
	},
	'TPC THM.' : {
			'label' : (924,578,1030,604),
			'value' : (1088,581,1173,605)
	},
	'GHATGR PUMP' : {
			'label' : (594,671,735,697),
			'value' : (789,675,828,700)
	},
	'COGEN' : {
			'label' : (594,989,670,1011),
			'value' : (789,982,844,1007)
	},
	'OTHR+SMHYD' : {
			'label' : (594,1009,730,1031),
			'value' : (789,1004,846,1032)
	},
	'AEML GEN.' : {
			'label' : (922,687,1041,716),
			'value' : (1081,692,1175,717)
	},
	'CS GEN. TTL.' : {
			'label' : (1341,998,1492,1029),
			'value' : (1549,1001,1616,1023)
	}
}


#converts image into a black and white image
def RGBtoBW(pil_image):
	image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2GRAY)
	image = cv2.threshold(image, 0, 255,
						 cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	return Image.fromarray(image)

#performs text recognition on given location and source image
def recognize(location, source, lang):
	img = source.crop(location)
	img = RGBtoBW(img)
	img = ImageOps.invert(img)
	text = pytesseract.image_to_string(img, lang=lang, config='--psm 7')

	return text, img


if __name__ == '__main__':

	file = open('logfile_ext.txt', 'a')
	
	#read image and save to a logfile
	while (True):

		image = imread(url)
		image = Image.fromarray(image)  # create PIL image
		#image = Image.open('error_2020-02-22T19 31.png')

		line = ''
		labels = []
		values=[]

		localtime = arrow.utcnow().shift(hours=5, minutes=30)
		localtime = localtime.format('YYYY-MM-DDTHH:mm')
		save_time = localtime.replace(':', ' ')

		plt_num = 1
		fig = plt.figure(figsize=(3,13))
		plt.subplots_adjust(top=0.8, wspace=0.2, hspace=0.3)
		rows = len(locations)
		cols = 2

		#recognize label and value for all items in locations-dict
		for type, locs in locations.items():
			label, l_img = recognize(locs['label'], image, 'eng')
			value, v_img = recognize(locs['value'], image, 'digits_comma')
			labels.append(label)
			values.append(value)

			axes = fig.add_subplot(rows, cols, plt_num)
			axes.get_xaxis().set_visible(False)
			axes.get_yaxis().set_visible(False)
			plt.imshow(l_img)
			plt.title(label)
			plt_num = plt_num + 1

			axes = fig.add_subplot(rows, cols, plt_num)
			axes.get_xaxis().set_visible(False)
			axes.get_yaxis().set_visible(False)
			plt.imshow(v_img)
			plt.title(value)
			plt_num = plt_num + 1

		#create line for log.txt
		#compare recognized label with name in locations dict to detect errors
		for i, key in enumerate(locations.keys()):
			if labels[i] == key:
				line = line+values[i]+ ' '
			else:
				line = line + 'NaN '
				image.save('error_'+save_time+'.png')
				print('Error: ' + labels[i] + ', ' +key)

		#read daytime from image
		rec_time, img = recognize( (355,110,524,150), image, 'eng')
		#plt.imshow(img)
		#plt.title(rec_time)
		rec_time = rec_time.replace(' ', 'T')


		line = line + localtime +' '
		line = line + rec_time
		file.write(line+'\n')
		print(line)
		plt.savefig('figures/' + save_time + '.png')
		#plt.show()
		time.sleep(60*10)
		plt.close()

	file.close()
