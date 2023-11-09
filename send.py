import scapy.all as scapy
import sub_logic
import argparse
import sub_logic
import ifcfg

BROADCAST_IP = '10.0.0.255'
ASK_IP_MSG = 10
ASK_OPINION = 1
BASE_RATE = 0.5

ips = []
for name, interface in ifcfg.interfaces().items():
    for i in interface['inet4']:
        if(i != "127.0.0.1"):
            ips.append(i)
my_ip = ips[0]


def send(ip, data):
    packet = scapy.IP(dst=ip)/scapy.TCP()/str(data)
    scapy.send(packet)

def ping(ip):
    packet = scapy.IP(dst=ip)/scapy.ICMP()
    s = scapy.sr1(packet, timeout=2, verbose=0)
    g = sub_logic.Graph(my_ip)
    if s is not None:
        o = sub_logic.SubLog(False, {
            "r": 1,
            "s": 0,
            "a": BASE_RATE
        })
        g.add_direct_nodes(ip, o)
    else:
        o = sub_logic.SubLog(False, {
            "r": 0,
            "s": 1,
            "a": BASE_RATE
        })
        g.add_direct_nodes(ip, o)
    path = "trust" + str(my_ip) + "/" + str(ip) + ".txt" 
    trust = g.compute_trust(ip)
    with open (path, "a") as f:
        f.write(str(trust))
        f.write(",")

def send_opinion(ip, opinion, on):
    raw_data = str(opinion.opinion_print_bdu()) + "-" + str(on)
    packet = scapy.IP(dst=ip)/scapy.TCP()/raw_data
    scapy.send(packet)


parser = argparse.ArgumentParser()

parser.add_argument('-dst', '--destination')

parser.add_argument('-i', '--init', action='store_true', help='You can send a broadcast message to obtain the IP adresses of your neighbours')
parser.add_argument('-o', '--opinion_ask', action='store_true', help='This sends a message to ask the opinion of somebody on an ip adresse')
parser.add_argument('-p', '--ping', action='store_true', help='This pings another node')
parser.add_argument('-m', '--message', help="You can send a message to another node using this flag")

parser.add_argument('-t', '--trust', nargs='+', type=float, help='You can send an opinion with this flag (format : -t value_a value_b value_d value_u)')
parser.add_argument('-on', '--opinion_on', help='When you send a trust value, you should precise the trust on who you are sending')

args = parser.parse_args()

#Handle the case the node want to asks for other nodes IP
if args.init:
    send(BROADCAST_IP, ASK_IP_MSG)
    exit()

#Pings another node
if args.ping:
    if args.destination:
        dst = args.destination
        ping(dst)
        exit()
    else:
        raise ValueError('You should presice with -dst to which node you want to ping')

#Send a string to another node
if args.message:
    if args.destination:
        dst = args.destination
        message = args.message
        send(dst, message)
        exit()
    else:
        raise ValueError('You should presice with -dst to which node you want to send the message')

#Ask the opinion on a node to another node
if args.opinion_ask:
    if args.destination:
        dst = args.destination
        if args.opinion_on:
            on = args.opinion_on
            send(dst, str(ASK_OPINION) + "-" + str(on))
            exit()
        else:
            raise ValueError('You should presice with -on the opinion of which node you want')
    else:
        raise ValueError('You should presice with -dst to which node you want to ask his opinion')

#Send a trust value to a node
if args.trust:
    a = args.trust[0]
    b = args.trust[1]
    d = args.trust[2]
    u = args.trust[3]
    if ((u + b + d) == 1):
        if args.destination:
            dst = args.destination
            if args.opinion_on:
                on = args.opinion_on
                opinion = sub_logic.SubLog(True, {
                            "a": a,
                            "b": b,
                            "d": d,
                            "u": u
                        })
                send_opinion(dst, opinion, on)
                exit()
            else:
                raise ValueError('You should presice with -on the opinion of which node you are sending')
        else:
            raise ValueError('You should presice with -dst to which node you want to ask your opinion')
    else:
        raise ValueError('Sum of b,d and u should be equal to 1')

raise ValueError('Use a flag to determine the data you want to send : ')

