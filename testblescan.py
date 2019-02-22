import blescan
import sys
import bluetooth._bluetooth as bluez
import Queue as queue
import threading
uuid_queue = queue.Queue()

uuid_list = [ '11111111111111111111111111111111', 'e2c56db5dffb48d2b060d0f5a71096e0']

comp_result = False

dev_id = 0

try:
	sock = bluez.hci_open_dev(dev_id)
	print "ble thread started"

except:
	print "error accessing bluetooth device..."
    	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

def distance_func(rssi_value, txPower):
	if rssi_value == 0:
		return -1.0
	if txPower == 0:
		return -1.0
	ratio = rssi_value*1.0/txPower
	
	if ratio < 1.0:
		return pow(ratio, 10)
	else:
		accuracy = (0.89976)*pow(ratio,7.7095) + 0.111
		return accuracy

def uuid_comp_func(target_uuid, uuid_list):
	for comp_uuid in uuid_list:
		if comp_uuid == target_uuid:
			print target_uuid
			print "\n"
			return True

def comp_result_func():
	global comp_result
	while True:
		if comp_result == True:
			print "Right"
			comp_result = False

def uuid_inqueue_func():
	while True:
		returnedList = blescan.parse_events(sock, 1)
		for beacon in returnedList:
			unfixed_payload = beacon.split(',')
			uuid = unfixed_payload[1]
			rssi = float(unfixed_payload[-1])
			txPower = float(unfixed_payload[-2])
			distance = distance_func(rssi, txPower)
			#print "UUID: {0} DISTANCE: {1}".format(uuid, distance)

			if distance < 0.0001 and distance > -1.0: #distane Value
				uuid_queue.put(uuid)
				print "Inqueued"
				print "UUID: {0} DISTANCE: {1}".format(uuid, distance)

def uuid_comp_set():
	global comp_result
	while True:	
		uuid = uuid_queue.get()
		comp_result = uuid_comp_func(uuid, uuid_list)

if __name__=='__main__':
	t1 = threading.Thread(target=uuid_inqueue_func) #Thread - UUID inqueue
	t2 = threading.Thread(target=uuid_comp_set) #Thread - dequeue & compare
	t3 = threading.Thread(target=comp_result_func) #Thread - compare result Output
	t1.start()
	t2.start()
	t3.start()
