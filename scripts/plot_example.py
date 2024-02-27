import os

import matplotlib.pyplot as plt

import pyhector
from pyhector import ssp119, ssp126, ssp245, ssp370, ssp434, ssp460, ssp534_over, ssp585

plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = 10, 5
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 12


path = os.path.join(os.path.dirname(__file__), "../docs/example-plot.png")

for ssp in [ssp119, ssp126, ssp245, ssp370, ssp434, ssp460, ssp534_over, ssp585]:
    output = pyhector.run(ssp, {"core": {"endDate": 2100}})
    temp = output["temperature.global_tas"]
    temp = temp.loc[1850:] - temp.loc[1850:1900].mean()
    temp.plot(label=ssp.name)
plt.title("Global mean temperature")
plt.ylabel("°C over pre-industrial (1850-1900 mean)")
plt.legend(loc="best")

plt.savefig(path, dpi=96)
