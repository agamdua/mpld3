"""
Plugins to add behavior to mpld3 charts
"""

__all__ = ['ToolTip']

import jinja2
import json


class PluginBase(object):
    JS = jinja2.Template("")
    FIG_JS = jinja2.Template("")
    HTML = jinja2.Template("")
    STYLE = jinja2.Template("")

    def set_figure(self, figure):
        self.figure = figure

    def _html_args(self):
        return {}

    def html(self):
        return self.HTML.render(self._html_args())

    def _style_args(self):
        return {}

    def style(self):
        return self.STYLE.render(self._style_args())

    def _js_args(self):
        return {}

    def js(self):
        return self.JS.render(self._js_args())

    def _fig_js_args(self):
        return {}

    def fig_js(self):
        return self.FIG_JS.render(self._fig_js_args())


class ToolTip(PluginBase):
    #JS = jinja2.Template("""
    #<script src={{ d3tip_url }}></script>
    #""")

    FIG_JS = jinja2.Template("""
    var tooltip = fig.canvas.append("text")
                  .attr("class", "text")
                  .attr("x", 0)
                  .attr("y", 0)
                  .style("visibility", "hidden")
                  .text("")
                  .attr("style", "text-anchor: middle;");

    var labels = {{ labels }};

    ax{{ axid }}.axes.selectAll(".points{{ lineid }}")
        .text(function(d){ "(" + d[0] + "," + d[1] + ")"})
	.on("mouseover", function(d, i){return tooltip
                                      .style("visibility", "visible")
                                      .text(labels[i]);})
        //                              .text("(" + d[0] + ", " + d[1] + ")");})
	.on("mousemove", function(d, i){return tooltip.attr("x", event.x)
                                                  .attr("y", event.y - 20);})
	.on("mouseout", function(d, i){return tooltip.style("visibility",
                                                        "hidden");});
    """)

    def __init__(self, line, labels,
                 d3tip_url=("http://labratrevenge.com/d3-tip/javascripts/"
                            "d3.tip.min.js")):
        self.d3tip_url = d3tip_url
        self.line = line
        self.labels = labels

    def _fig_js_args(self):
        obj = self._get_line_obj()
        return dict(d3tip_url=self.d3tip_url,
                    axid=obj.axid,
                    lineid=obj.lineid,
                    labels=json.dumps(self.labels))

    def _get_line_obj(self):
        obj = None
        for ax in self.figure.axes:
            obj = obj or ax.objmap.get(self.line, None)
        return obj

    def html(self):
        line = self._get_line_obj()
        print type(line)
        return ''

    
