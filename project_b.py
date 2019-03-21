import blescan
import sys
import bluetooth._bluetooth as bluez
import Queue as queue
import threading
import MySQLdb
import time
import os
#-------------------System Command Line--------------------
os.system('sudo echo -e "power on \nscan on \nquit" | bluetoothctl')
time.sleep(3)
#-------------------Global Data Structure & Variable--------
uuid_queue = queue.Queue()
uuid_list = []
output_flag = False
used_list = []
del_time = 10 #time of init
non_list = []
#-------------------Database connect-----------------------
try:
	db=MySQLdb.connect(host="mariadb.c4lfqmkfhrw8.ap-northeast-2.rds.amazonaws.com",\
									 	 user="admin",passwd="1q2w3e4r",db="mariadb")
	print "Connected DataBase"

except:
	print "Error Database Connect"
	sys.exit(1)

cur = db.cursor()
cur.execute("SELECT * FROM uuid_list")
for row in cur.fetchall():
	uuid_list.append(row[0])
db.close()

#-------------------Socket(or Network)----------------------
dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print "Start Bluetooth Scan"

except:
	print "Error Bluetooth Device"
	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

'''
test_payload = blescan.parse_events(sock, 1)
if test_payload is None:
	os.system('echo -e "" | sudo python /home/pi/iBeacon-Scanner-/project_b.py')
	sys.exit(1)
else:
	print test_payload
'''
#------------------Function---------------------------------
def distance_func(rssi_value, txPower):
	if rssi_value == 0:
		return -1.0
	if txPower == 0:
		return -1.0
	
	ratio = rssi_value*1.0/txPower
	
	if ratio < 1.0:
		return (pow(ratio, 10)*100)
	else:
		accuracy = (0.89976)*pow(ratio, 7.7095) + 0.111
		return (accuracy*100)

def compare_func(uuid_list, target_uuid):
	if target_uuid in uuid_list:
		return True
	else:
		return False

def parser_func():
	payload_nonfix = blescan.parse_events(sock, 1)
	for payload_list in payload_nonfix:
		payload = payload_list.split(',')
		return payload

def rssi_check_func(distance):
	if distance > -1.0: #distance_func Error value is -1.0
		return True
	else:
		return False

def rssi_origin_check_func(rssi):
	if rssi > -30:
		return True
	else:
		return False

def used_check_func(used_list, target_uuid):
	if target_uuid in used_list:
 		return False
	else:
		return True

#===========## Thread_func ##=================

def inqueue_func():
	while True:
		payload = parser_func()
		uuid_queue.put(payload)
		#print payload

'''
def output_func():
	while True:	
		global output_flag
		if output_flag == True:
			print "Right UUID, Get in!"
			output_flag = False
'''

def dequeue_func():
	#payload - Mac_addr[0], UUID[1], Major[2], Minor[3], txPower[4], RSSI[5]
	while True:
		#global output_flag
		payload = uuid_queue.get()
		uuid = payload[1]
		txPower = float(payload[-2])
		rssi = float(payload[-1])
		distance = distance_func(rssi, txPower)
		print "UUID: {0} distance: {1} RSSI: {2}".format(uuid, distance, rssi)
		
		if rssi_check_func(distance) == True:
		#if rssi_origin_check_func(rssi) == True:
			if compare_func(uuid_list, uuid) == True:
				if used_check_func(used_list, uuid) == True:
					print "\nOk\nThat's Right\nGet in, Bro!\n"
					used_list.append(uuid)
					print "UUID: {0} distance: {1} RSSI: {2}".format(uuid, distance, rssi)

def init_list():
	while True:
		time.sleep(del_time)
		del used_list[:]
		print "init uuid_list\n\n"

#----------------Main_func---------------------------------------
if __name__=='__main__':
	'''
	if test_payload == None:
		os.system('echo -e "" | sudo python /home/pi/iBeacon-Scanner-/project_b.py')
		sys.exit(1)
	else:
		print test_payload
	'''
	#Thread - init used_list
	t_init_list = threading.Thread(target=init_list)
	#Thread - UUID inqueue
	t_inqueue = threading.Thread(target=inqueue_func)
	#Thread - dequeue & compare
	t_deq_comp = threading.Thread(target=dequeue_func)
	#Thread - compared result Output
	t_init_list.start()
	t_inqueue.start()
	t_deq_comp.start()
