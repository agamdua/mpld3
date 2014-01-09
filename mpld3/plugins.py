"""
Plugins to add behavior to mpld3 charts
"""


class PluginBase(object):
    def body(self):
        return ''

    def style(self):
        return ''

    def js(self):
        return ''


class TooltipPlugin(PluginBase):
    def __init__(self, line, labels):
        self.line = line
        self.labels = labels
