import numpy as np
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins

from astroML.datasets import fetch_LINEAR_geneva, fetch_LINEAR_sample
data = fetch_LINEAR_geneva()
lcdata = fetch_LINEAR_sample()

fig, ax = plt.subplots()

# draw the scatter-plot
dots = ax.scatter(data['gi'][::10],
                  data['logP'][::10],
                  c=data['amp'][::10],
                  s=60, alpha=0.3)

fig.colorbar(dots, ax=ax)
ax.set_xlabel('g - i color')
ax.set_ylabel('log(P)')

labels = ["id={0}".format(id) for id in data['LINEARobjectID']]
fig.plugins = [plugins.CollectionToolTip(dots, labels=labels)]
mpld3.show_d3()
