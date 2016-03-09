import socket
import sys
import time
import hashlib
from threading import Thread,Condition,Lock

feedback = ['ACK','NACK']

output = [None] * 10452 
ordered_odd = 2
ordered_even = 1

done_lock = Lock()
odd_lock = Lock()
even_lock = Lock()
done = 0

def increment():
  global done
  done += 1

class recieve(Thread):
	def __init__(self,port,odd):
		self.port = port
		self.odd = odd
		Thread.__init__(self)

	def run (self):
		global ordered_odd
		global ordered_even
		sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		listen_addr = ('', self.port)
		sock.bind(listen_addr)
		print 'Starting up on local port %s' %listen_addr[1]

		if self.odd==0:
			ordered = 1
		else:
			ordered = 2		
		
		while 1:
			try:
				data,addr = sock.recvfrom(1000)
				sequence_number = int(data[:5])
				if sequence_number == ordered : 
					
					checksum = data[-10:]
					hash_value = (hashlib.sha1(data[:-10]).hexdigest())[:10]

					if checksum == hash_value:		

						output [ ordered-1 ]  = data[5:-10]
						ordered += 2 
						while output[ ordered-1] != None:
							ordered += 2 
				
				elif sequence_number > ordered:
					
					checksum = data[-10:]
					hash_value = (hashlib.sha1(data[:-10]).hexdigest())[:10]

					if checksum == hash_value:
						output [ sequence_number-1 ] = data[5:-10]

				if ordered == 10451 :
					odd_lock.release()
					ordered = ordered_odd
				elif ordered == 10450:
					even_lock.release()
					ordered = ordered_even
				else:
					if self.odd==1:
						ordered_odd = ordered
					else:
						ordered_even = ordered	

				print str(sequence_number)+" "+str(ordered)
				sock.sendto(feedback[0] + str(ordered),addr)
			except KeyboardInterrupt:
				print(time.time() - start_time)
				sock.close()
				break
				print "Connection is closed."
		sock.close()

if __name__ == "__main__":
	output_file = open("output.txt", "wb")
	start_time = time.time()
	
	reciever1 = recieve(10005,0)
	reciever2 = recieve(10006,1)
	reciever1.start()
	reciever2.start()

	odd_lock.acquire()
	even_lock.acquire()


	odd_lock.acquire()	
	even_lock.acquire()
	print "Done Babe"
	i =0
	for a in output:
		if a:				
			i+=1
			output_file.write(str(a))
		else:
			print a

	print time.time() - start_time

