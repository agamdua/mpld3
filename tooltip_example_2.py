import numpy as np
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins

from astroML.datasets import fetch_LINEAR_geneva, fetch_LINEAR_sample
data = fetch_LINEAR_geneva()
lcdata = fetch_LINEAR_sample()

fig, ax = plt.subplots(2)

# draw the scatter-plot
dots = ax[0].scatter(data['gi'][::10],
                  data['logP'][::10],
                  c=data['amp'][::10],
                  s=60, alpha=0.3)

fig.colorbar(dots, ax=ax[0])
ax[0].set_xlabel('g - i color')
ax[0].set_ylabel('log(P)')

# get the light curve data
lightcurves = []
for id in data['LINEARobjectID'][::10]:
    try:
        d = lcdata[int(id)]
    except KeyError:
        d = np.zeros((1, 3))
    lightcurves.append(d[:, :2].tolist())


line, = ax[1].plot(d[:, 0], d[:, 1])

labels = ["id={0}".format(id) for id in data['LINEARobjectID']]
fig.plugins = [plugins.ObjViewToolTip(dots, labels, line_to_change=line,
                                      linedata=lightcurves)]
mpld3.show_d3()
