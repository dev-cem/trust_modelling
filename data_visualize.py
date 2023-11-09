import matplotlib.pyplot as plt
import numpy as np
import sys
import copy

SIM = sys.argv[1]
IPS = ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4"]
IPS_COLORS = ["#E83711", "#1155E8", "#E5A110", "#47C10D"]
i = 0
for IP in IPS:
       IPS_TO_USE = copy.deepcopy(IPS)
       IPS_COLORS_TO_USE = copy.deepcopy(IPS_COLORS)
       IPS_TO_USE.remove(IP)
       IPS_COLORS_TO_USE.pop(i)
       FILENAME_1 = SIM + "/trust" + IP + "/" + IPS_TO_USE[0] + ".txt" 
       FILENAME_2 = SIM + "/trust" + IP + "/" + IPS_TO_USE[1] + ".txt" 
       FILENAME_3 = SIM + "/trust" + IP + "/" + IPS_TO_USE[2] + ".txt" 
       FILENAME = SIM + "/" + IP + ".png"

       data1 = np.loadtxt(FILENAME_1, delimiter=",", dtype=str)
       data1 = data1[0:50].astype(np.float)
       data2 = np.loadtxt(FILENAME_2, delimiter=",", dtype=str)
       data2 = data2[0:50].astype(np.float)
       data3 = np.loadtxt(FILENAME_3, delimiter=",", dtype=str)
       data3 = data3[0:50].astype(np.float)

       plt.style.use('seaborn-talk')

       x = np.linspace(0, 50)
       plt.figure(figsize=(8,8))

       plt.plot(x, data1, linewidth=1.5, label=IPS_TO_USE[0], color=IPS_COLORS_TO_USE[0])
       plt.plot(x, data2, linewidth=1.5, label=IPS_TO_USE[1], color=IPS_COLORS_TO_USE[1])
       plt.plot(x, data3, linewidth=1.5, label=IPS_TO_USE[2], color=IPS_COLORS_TO_USE[2])

       plt.xlim(0, 50)
       plt.ylim(0, 1)

       plt.title("Trusts levels of car " + IP)
       plt.xlabel("Number of interactions")
       plt.ylabel("Trust level")
       plt.legend()

       plt.savefig(FILENAME)
       i = i + 1

