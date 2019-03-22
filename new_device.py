import sys
import Queue as queue
import threading
import MySQLdb
import time
import os
import requests

#-----------Global Data Sturucture & Variable------------
uuid_list = []
#-----------Database connect-----------------------------
query_ = "SELECT * FROM uuid_list"


'''
try:
    db=MySQLdb.connect(host="13.125.170.17", user="root",passwd="7269",db="Capstone")
    print "Connected Database"
    
except:
    "Error Database Connect"
    sys.exit(1)
cur = db.cursor()
cur.execute(query_)
for row in cur.fetchall():
    uuid_list.append(row[0])
db.close()
'''
#----------Function-------------------------------------

#----------Main_func------------------------------------

if __name__=='__main__':
    

