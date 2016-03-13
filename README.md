# ReliableDataTransferProtocol
This is a UDP based reliable data transfer protocol which supports multi-homing. This protocol uses packets that consist of data divisions and its own header which contains the hash value of this packet and a sequence number of it. 

To supply reliability =>

In the reciever side of this protocol, it uses cumulative acking. Thanks to this, sender side can understand data loss by dublicate acks. When sender understands the data loss at a point, it sends just the lost data instead of sending all data inside the window. 

To use the advantage of multi-homing =>

As it is already mentioned, there are sequence numbers which is saved in the header of each packet. Because there are two channels to send the data, the data flow is devided into these two channels as odd numbered packets and even numberds. In other words, one link is the responsible of sending odd numbered packages while the other is sending the even ones. When one of these channels is done with sending its own half, it starts helping to send the other half with the other link. While two links are trying to send the samely numbered half, cumulative acking prevent a possible data sending repetition of these two channels.
