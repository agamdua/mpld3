"""
Plugins to add behavior to mpld3 charts
"""

__all__ = ['ToolTip']

import jinja2
import json
import uuid


class PluginBase(object):
    JS = jinja2.Template("")
    FIG_JS = jinja2.Template("")
    HTML = jinja2.Template("")
    STYLE = jinja2.Template("")

    @staticmethod
    def generate_unique_id():
        return str(uuid.uuid4()).replace('-', '')

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


class LineToolTip(PluginBase):
    FIG_JS = jinja2.Template("""

    var tooltip = fig.canvas.append("text")
                  .attr("class", "tooltip-text")
                  .attr("x", 0)
                  .attr("y", 0)
                  .text("")
                  .attr("style", "text-anchor: middle;")
                  .style("visibility", "hidden");

    {% if labels %}
    var labels = {{ labels }};
    {% endif %}

    ax{{ axid }}.axes.selectAll(".points{{ lineid }}")
	.on("mouseover", function(d, i){
                           tooltip
                              .style("visibility", "visible")
                              {% if labels %}
                              tooltip.text(labels[i])
                              {% else %}
                              tooltip.text("(" + d[0] + ", " + d[1] + ")")
                              {% endif %};})
	.on("mousemove", function(d, i){
                                   tooltip
                                       .attr('x', event.x - {{ hoffset }})
                                       .attr('y', event.y - {{ voffset }});})
	.on("mouseout", function(d, i){tooltip.style("visibility",
                                                     "hidden");});
    """)

    def __init__(self, line, labels=None,
                 hoffset=0, voffset=20):
        self.line = line
        self.labels = labels
        self.voffset = voffset
        self.hoffset = hoffset
        self.id = self.generate_unique_id()

    def _fig_js_args(self):
        obj = self._get_line_obj()
        return dict(id=self.id,
                    hoffset=self.hoffset,
                    voffset=self.voffset,
                    axid=obj.axid,
                    lineid=obj.lineid,
                    labels=json.dumps(self.labels))

    def _get_line_obj(self):
        obj = None
        for ax in self.figure.axes:
            obj = obj or ax.objmap.get(self.line, None)
        return obj


class CollectionToolTip(PluginBase):
    FIG_JS = jinja2.Template("""

    var tooltip = fig.canvas.append("text")
                  .attr("class", "tooltip-text")
                  .attr("x", 0)
                  .attr("y", 0)
                  .text("")
                  .attr("style", "text-anchor: middle;")
                  .style("visibility", "hidden");

    {% if labels %}
    var labels = {{ labels }};
    {% endif %}

    console.log(ax{{ axid }}.axes.selectAll(".paths{{ collid }}"))

    ax{{ axid }}.axes.selectAll(".paths{{ collid }}")
	.on("mouseover", function(d, i){
                           tooltip
                              .style("visibility", "visible")
                              {% if labels %}
                              tooltip.text(labels[i])
                              {% else %}
                              tooltip.text("(" + d[0] + ", " + d[1] + ")")
                              {% endif %};})
	.on("mousemove", function(d, i){
                                   tooltip
                                       .attr('x', event.x - {{ hoffset }})
                                       .attr('y', event.y - {{ voffset }});})
	.on("mouseout", function(d, i){tooltip.style("visibility",
                                                     "hidden");});
    """)

    def __init__(self, points, labels=None,
                 hoffset=0, voffset=20):
        print "initing"
        self.points = points
        self.labels = labels
        self.voffset = voffset
        self.hoffset = hoffset
        self.id = self.generate_unique_id()

    def _fig_js_args(self):
        obj = self._get_collection_obj()
        return dict(id=self.id,
                    hoffset=self.hoffset,
                    voffset=self.voffset,
                    axid=obj.axid,
                    collid=obj.collid,
                    labels=json.dumps(self.labels))

    def _get_collection_obj(self):
        obj = None
        for ax in self.figure.axes:
            obj = obj or ax.objmap.get(self.points, None)
        return obj
