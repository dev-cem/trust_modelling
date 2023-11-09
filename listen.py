import scapy.all as scapy
import subprocess
import ifcfg
from time import sleep
from datetime import datetime
import sub_logic
import json

BASE_RATE = 0.5
INIT_TRUST = sub_logic.SubLog(False,{"a": BASE_RATE, "r": 1, "s":0})
LISTEN_FILE_PATH = "listen.py"
SEND_FILE_PATH = "send.py"
ASK_IP_MSG_FLAG = '10'
ASK_OPINION_MSG_FLAG = '1-'
OPINION_MSG_FLAG = "{"
IP_RECEIVED_FLAG = "10.0.0."
LOG_FILE = 'log.txt'

#This var capture one packet, the last one sended
capture = scapy.sniff(count=1, filter="tcp")

#Continue listening
subprocess.Popen(["python3", LISTEN_FILE_PATH, "&"])

#Get the ip of the node
ips = []
for name, interface in ifcfg.interfaces().items():
    for i in interface['inet4']:
        if(i != "127.0.0.1"):
            ips.append(i)
ip = ips[0]
sleep(int(ip[-1]))

#Tries to open the RAW data in the packet
try:
    d = str(capture[0][scapy.Raw].load.decode("utf-8"))
    #data = json.loads(d.replace("'", '"'))
    data = d

    #If packet is for me
    if(str(capture[0][scapy.IP].dst) == ip):
        g = sub_logic.Graph(ip)
        with open(LOG_FILE, 'a') as f:
            f.write(datetime.now().strftime("%H:%M:%S") + " : " + ip + ' received : ***' + str(data)  + '*** from ' + str(capture[0][scapy.IP].src)  +'\n')
            #I got the IP of a node, I should init an opinion on this node with INIT_TRUST
            if(str(data[:7]) == IP_RECEIVED_FLAG):
                g.add_direct_nodes(data, INIT_TRUST)
            #This flag indicates that a node is asking my opinion over another node , I will send my opinion
            elif(str(data[:2]) == ASK_OPINION_MSG_FLAG):
                opinion_on = data[-8:]
                o = g.get_my_opinion(opinion_on)
                cmd = ["python3", SEND_FILE_PATH, "-t", str(o.a), str(o.b), str(o.d), str(o.u), "-on", opinion_on, "-dst", str(capture[0][scapy.IP].src)]
                subprocess.Popen(cmd)
            #I received an opinion, I should store this opinion in my data
            elif(str(data[0]) == OPINION_MSG_FLAG):
                opinion = json.loads(str(data[:-9]).replace("'", '"'))
                o = sub_logic.SubLog(True, opinion)
                g.add_indirect_nodes(str(capture[0][scapy.IP].src), data[-8:], o)
            #I have nothing to do with other packets
            else:
                pass
                

    #If broadcast
    if(str(capture[0][scapy.IP].dst) == '10.0.0.255'):
        if(str(capture[0][scapy.IP].src) != ip):
            with open(LOG_FILE, 'a') as f:
                f.write(datetime.now().strftime("%H:%M:%S") + " : " + ip + ' received : ***' + str(data)  + '*** from broadcast (' + str(capture[0][scapy.IP].src) + ')\n')
                if(str(data) == ASK_IP_MSG_FLAG):
                    cmd = ["python3", SEND_FILE_PATH, "-dst", str(capture[0][scapy.IP].src), "-m", ip]
                    subprocess.Popen(cmd)
                    

#If it can't open it writes an error message in the log file
except:
    with open(LOG_FILE, 'a') as f:
        f.write(datetime.now().strftime("%H:%M:%S") + " : " + ip + ' says : error in received packet\n')

