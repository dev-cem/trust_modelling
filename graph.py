import sub_logic
import ifcfg

#Get the ip of the node
ips = []
for name, interface in ifcfg.interfaces().items():
    for i in interface['inet4']:
        if(i != "127.0.0.1"):
            ips.append(i)
ip = ips[0]

#Init the graph with the IP address
sub_logic.Graph(ip)