import os

import matplotlib.pyplot as plt
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = 10, 5
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 12

import pyhector
from pyhector import rcp26, rcp45, rcp60, rcp85

path = os.path.join(os.path.dirname(__file__),
                    '../docs/example-plot.png')

for rcp in [rcp26, rcp45, rcp60, rcp85]:
    output = pyhector.run(rcp, {"core": {"endDate": 2100}})
    temp = output["temperature.Tgav"]
    temp = temp.loc[1850:] - temp.loc[1850:1900].mean()
    temp.plot(label=rcp.name.split("_")[0])
plt.title("Global mean temperature")
plt.ylabel("°C over pre-industrial (1850-1900 mean)")
plt.legend(loc="best")

plt.savefig(path, dpi=96)
