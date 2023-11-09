import sub_logic
import os
import ifcfg

ips = []
for name, interface in ifcfg.interfaces().items():
    for i in interface['inet4']:
        if(i != "127.0.0.1"):
            ips.append(i)
ip = ips[0]

g = sub_logic.Graph(ip)
os.system('mkdir trust' + str(ip))
for i in g.get_my_nodes():
    os.system('touch trust' + str(ip) + '/' + str(i) + '.txt')