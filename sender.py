import socket
import threading
import sys
import datetime
import time
import hashlib

def packetMaker(packet,i):
    hash_value = (hashlib.sha1(str(i).zfill(5) + packet).hexdigest())[:10]
    packet =  str(i).zfill(5) + packet + hash_value
    return packet

i = 1
input_file = open("input.txt", "rb") 
file_array = []
packet = input_file.read(957)   
while packet:
    packet = packetMaker(packet,i)
    file_array.append(packet)
    packet = input_file.read(957)
    i += 1

ACK_loss = 0
total_time = 0
window_size = 5
window_base = 1
packet_size = 954
success_table = [False]*10397

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.01)

#server_address = ('144.122.238.100', 10005)
server_address = ('144.122.238.100', 10005)

'''a
28 Byte for UDP+IP headers
10 Byte for first 10 digits of SHA1 hash
16 Byte for Ethernet connection(optional)
8 Byte sequence number

954 Byte for actual data

10396 packets must be transferred
'''

start_time = time.time()

while window_base < len(file_array):
    try:

        for j in range(window_size):
            if window_base+j - 1 < len(file_array):
                sock.sendto(file_array[window_base+j - 1],server_address)
        
        requested_packet = 0 
        for j in range(window_size):
            try : 
                feedback,addr = sock.recvfrom(50)
                if requested_packet == int(feedback[3:]):
                    break

                requested_packet = int(feedback[3:])
                print(requested_packet)
                window_base = requested_packet
                

            except socket.timeout:
                print "Timeout: Sent Again. Packet loss count: %d" %ACK_loss
                ACK_loss += 1

            
        elapsed_time = (time.time() - start_time)*1000
        
        total_time += elapsed_time 
    


    except KeyboardInterrupt:
        sock.close()
        

sock.close()