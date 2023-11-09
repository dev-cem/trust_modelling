from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
import os
from datetime import datetime
from time import sleep
import argparse
import random

RANGE = "35"
LISTEN_FILE_PATH = "listen.py"
GRAPH_FILE_PATH = "graph.py"
GRAPH_INIT_FILE_PATH = "send.py -i"
PING_FILE_PATH = "send.py -p"
ASK_OPINION_FILE = "send.py -o"
DATA_HANDLE_FILE = "data_handle.py"
NUMBER_OF_ITERATION = 1000

def topology():
    #Create a network
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    #Add the range of each nodes LAN
    kwargs = {}
    kwargs['range'] = RANGE

    info("*** Adding nodes\n")
    car1 = net.addStation('car1', ip='10.0.0.1', ip6='fe80::1',
                          position='40,10,0', **kwargs)
    car2 = net.addStation('car2', ip='10.0.0.2', ip6='fe80::2',
                          position='50,20,0', **kwargs)
    car3 = net.addStation('car3', ip='10.0.0.3', ip6='fe80::3',
                          position='50,0,0', **kwargs)
    car4 = net.addStation('car4', ip='10.0.0.4', ip6='fe80::4',
                          position='60,10,0', **kwargs)
    cars = [car1, car2, car3, car4]

    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Adding links\n")
    net.addLink(car1, cls=adhoc, intf='car1-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                **kwargs)
    net.addLink(car2, cls=adhoc, intf='car2-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                **kwargs)
    net.addLink(car3, cls=adhoc, intf='car3-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                **kwargs)
    net.addLink(car4, cls=adhoc, intf='car4-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                **kwargs)
    
    '''info("*** Displaying graph\n")
    net.plotGraph(max_x=100, max_y=100)'''

    info("*** Starting network\n")
    net.build()

    '''info('\n*** Testing connections\n')
    net.pingAll()'''

    info("\n\n*** Initializing Subjective Logic")
    for i in cars:
        i.cmd("python3 " + GRAPH_FILE_PATH + " &")

    info("\n*** Nodes starts listening")
    for i in cars:
        i.cmd("python3 " + LISTEN_FILE_PATH + " &")

    info("\n*** Graph is initialized")
    for idx, i in enumerate(cars):
        sleep(7)
        info("\n*** Car " + str(idx + 1) + " : ")
        i.cmd("python3 " + GRAPH_INIT_FILE_PATH + " &")
    sleep(10)

    for i in cars:
        i.cmd("python3 " + DATA_HANDLE_FILE + " &")
    

    car1.cmd('tc qdisc add dev car1-wlan0 root netem loss 30%')
    car2.cmd('tc qdisc add dev car2-wlan0 root netem loss 1%')
    car3.cmd('tc qdisc add dev car3-wlan0 root netem loss 1%')
    car4.cmd('tc qdisc add dev car4-wlan0 root netem loss 1%')

    info("\n*** Starting the simulation")
    for i in range(NUMBER_OF_ITERATION):
        n = random.sample(range(1,5), 3)
        if i % 20 == 0:
            cars[n[0] - 1].cmd("python3 " + ASK_OPINION_FILE + " -dst 10.0.0." + str(n[1]) + " -on 10.0.0." + str(n[2]))
        else:
            cars[n[0] - 1].cmd("python3 " + PING_FILE_PATH + " -dst 10.0.0." + str(n[1]))
        print("\n" + str(round(i/NUMBER_OF_ITERATION*100, 2)) + "%")


    info("\n\n")
    CLI(net)
    
    info("*** Stopping network\n")
    net.stop()

    #Save all the json file if the '-s' flag is used
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--save', action='store_true', help='Use this flag to store the json files after the simulation')
    args = parser.parse_args()
    if args.save:
        e = datetime.timestamp(datetime.now())
        os.system('mkdir sim4n3g_' + str(e))
        os.system('mv *.json sim4n3g_' + str(e))
        os.system('mv trust* sim4n3g_' + str(e))
    else:
        os.system('rm -rf trust*')
        os.system('rm -rf *.json')

def init():
    setLogLevel('info')
    topology()

init()