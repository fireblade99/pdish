import serial
import math
import time
import urllib2
import urllib

"""
We use a web server to display the results. 
Post_to_server is simply doing a HTTP POST 
request to the url provided with the values 
given to it.
"""
def post_to_server(url, values):
	if values['opacity'] != None and values['number'] != None:
		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)

# get user input on automatic or manual mode
def get_mode():
	mode = raw_input("Which mode do you want? 0 = manual, 1 = automatic: ")
	return mode
	
# get user input on # of dishes loaded
def get_dishes():
	no_dishes = raw_input("How many dishes are loaded? ")
	return no_duishes

# send over serial to ardunio
def send_data(ser, data, end_char):
	ser.write(data)
	ser.write(end_char)

########## ACTUAL CODE #################
	
ser = serial.Serial('/dev/ttyACM0', 9600) # open serial port
send_data(get_dishes(), 'n')
send_data(get_mode(), 'z')

i = 1
while i <= no_dishes:		# loop this all dishes are completed
	if int(mode) == 0:		# if manual, get user input
		a = raw_input("press enter to read opacity of dish #" + str(i))
		ser.write('y');
	values = {}			# temp hash to store data
	while (len(values) <2):		# until all data is recevied
		input1 = ser.readline()
		#print input1
		if  len(input1) > 1	:			# null checker
			# gets the digits from serial read
			b = [int(s) for s in input1.split() if s.isdigit()]	
			if "number" in input1: # receiving number of dish
				values['number'] = b[0]
			elif "light" in input1:	# receiving light data
				#print "light data is : " + str(b)
				values['opacity'] = float(b[0])/1023 * 100;	# converting light data to opacity
	print 'values are :               '
	print values
	if len(values) == 2:	
		post_to_server('http://pdish.herokuapp.com/data', values)	# post to server
		i+=1
