import blescan
import sys
import bluetooth._bluetooth as bluez
import Queue as queue
import threading

#-------------------Global Data Structure & Variable--------
uuid_queue = queue.Queue()
uuid_list = ['11111111111111111111111111111111',\
					 	 'e2c56db5dffb48d2b060d0f5a71096e0']
output_flag = False

#-------------------Socket----------------------------------
dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print "Start Bluetooth Scan"

except:
	print "Error Bluetooth Device"
	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)


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
	for comp_uuid in uuid_list:
		if target_uuid == comp_uuid:
			return True

def parser_func():
	payload_nonfix = blescan.parse_events(sock, 1)
	for payload_list in payload_nonfix:
		payload = payload_list.split(',')
		return payload

def rssi_check_func(distance):
	if distance < 0.01 and distance > -1.0: #distance_func Error value is -1.0
		return True
	else:
		return False

def rssi_origin_check_func(rssi):
	if rssi > -30:
		return True
	else:
		return False

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
		#print "UUID: {0} distance: {1} RSSI: {2}".format(uuid, distance, rssi)
		
		#if rssi_check_func(distance) == True:
		if rssi_origin_check_func(rssi) == True:
			if compare_func(uuid_list, uuid) == True:
				print "\nOk\nThat's Right\nGet in, Bro!\n"
				print "UUID: {0} distance: {1} RSSI: {2}".format(uuid, distance, rssi)
		
#----------------Main_func---------------------------------------

if __name__=='__main__':

	#Thread - UUID inqueue
	t_inqueue = threading.Thread(target=inqueue_func)
	#Thread - dequeue & compare
	t_deq_comp = threading.Thread(target=dequeue_func)
	#Thread - compared result Output
	#t_res_output = threading.Thread(target=output_func)
	
	t_inqueue.start()
	t_deq_comp.start()
	#t_res_output.start()
