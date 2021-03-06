# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 20:26:34 2016
@author: jpelda
This class plots figures.
It inherits from Plotter_helper
yAxis must be importet as array always.
"""
import numpy as np

import geopandas as gp
from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import MultiLineString

import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from matplotlib import rc
import pandas as pd
import igraph

import datetime



class Plotter():

    def __init__(self, title='', figsize=0.6):

        self.title = ''
        self.figsize = figsize
        self._formate()

    def grid(self):
        pass

    def color(self, i):
        self.__color = [
                        ['black',                '#000000'],
                        ['hawk_red',             '#C24C43'],
                        ['hawk_blue',            '#43B9C2'],
                        ['hawk_green',           '#B9C243'],
                        ['orange',               '#FFA500'],
                        ['blue',                 '#0000FF'],
                        ['hawk_magenta',         '#C243B9'],
                        ['olive',                '#808000'],
                        ]
        return self.__color[i][1]

    def scatter(self, x, y, s=2,  # 0 to 15 point radii
                c='blue', alha=0.5):
        plt.scatter(x, y, s, c, alpha=0.5)
        plt.show()

    def plot_xyLine(self,
                    xAxis, yAxis,
                    lineStyle="-",
                    xLabel='', yLabel='',
                    title='', legend='',
                    position="upper right", rotation=None,
                    pltStyle='latex-classic'):
        """
        Parameters
        -----------
        xAxis = [] \n
        yAxis = [[],[],[], ...] \n
        lineStyle = 'string' str: '-', '--', '-.', ':' etc. \n
        xLabel = 'string' \n
        yLabel = 'string' \n
        title = 'string' \n
        legend = ['string x Achse', 'string x Achse 2'] \n
        positon = 'string' str: "upper right", "upper left", "lower right" etc.
        rotation= 0 - 360 \n
        Return
        ------------
        fig
        """
        self.__xAxis = xAxis
        self.__yAxis = yAxis
        self.__title = title
        self.__lineStyle = lineStyle

        fig = plt.figure(figsize=(12.6, 7.09))
        ax = fig.add_subplot(111)
        plt.style.use(pltStyle)
        try:
            if isinstance(self.__xAxis[0], (datetime.datetime, datetime.date)):
                if len(self.__xAxis) <= 15000:
                    years = mdates.YearLocator()
                    months = mdates.MonthLocator()
                    days = mdates.DayLocator()
                    ax.xaxis_date()
                    ax.xaxis.set_major_locator(months)
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
                    ax.xaxis.set_minor_locator(days)
                    for index, item in enumerate(self.__yAxis):
                        if item is not None:
                            plt.plot(self.__xAxis, item,
                                     color=self.color(index))
                        else:
                            break
                else:
                    years = mdates.YearLocator()
                    months = mdates.MonthLocator()
                    days = mdates.DayLocator()
                    ax.xaxis_date()
                    ax.xaxis.set_major_locator(years)
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
                    ax.xaxis.set_minor_locator(months)
                    for index, item in enumerate(self.__yAxis):
                        if item is not None:
                            plt.plot(self.__xAxis, item,
                                     colo=self.color(index))
                        else:
                            break

            elif isinstance(float(self.__xAxis[0]), float):
                '''loops through all y values and adds them to the figure'''

                ax.tick_params(direction="out", pad=5)

                plt.plot(self.__xAxis, self.__yAxis[0], color=self.color(0))
                for index, item in enumerate(self.__yAxis[1:]):
                    if item is not None:
                        plt.plot(self.__xAxis, item, color=self.color(index+1))
    #        elif isinstance(str(self.__xAxis[0]), str):
    #            plt.xticks(np.arange(len(xAxis)), xAxis)
    #            for index, item in enumerate(self.__yAxis):
    #                if item is not None:
    #                    ax.plot(np.arange(len(xAxis)), item, self.__lineStyle)

    #            ax.set_xlim(xmin = self.__xMin, xmax = self.__xMax)
    #            ax.set_ylim(self.__yMin, self.__yMax)
        except:
            raise

        plt.show()
        return fig

    def plot_xyLinehvLine(self,
                          xData,
                          yData,
                          yMax=0,
                          xMax=0,
                          lineStyle="-",
                          xLabel='', yLabel='',
                          title='', legend='',
                          rotation=None,
                          pltStyle='latex-classic'):
        """
        Parameters
        -----------
        xData = [Values of xAxis0]
        yData = [[Values of yAxis0], [Values of yAxis1], ...]
        lineStyle = str
        """
        self.__xAxis = xData
        self.__yAxis = yData
        self.__title = title
        self.__lineStyle = ['-', '--', ':']
        fig = plt.figure(figsize=(12.6, 7.09))
        mpl.rcParams["figure.figsize"] = 8, 4.5
#        Plotter_Helper.font(self)

        plt.style.use(pltStyle)
        ax_0 = fig.add_subplot(111)
#        ax_0.tick_params(axis="x", pad=105)
        ax_1 = fig.add_subplot(111)
        ax_2 = fig.add_subplot(111)
        try:
            if isinstance(self.__xAxis[0], datetime.date):
                years = mdates.YearLocator()
                months = mdates.MonthLocator()
                days = mdates.DayLocator()
                yearsFmt = mdates.DateFormatter('%b %y')
                ax_0.xaxis_date()
                ax_0.xaxis.set_major_locator(months)
                ax_0.xaxis.set_major_formatter(yearsFmt)
                ax_0.xaxis.set_minor_locator(days)
                for index, item in enumerate(self.__yAxis):
                    if item is not None:
                        ax_0.plot(self.__xAxis[index], item,
                                  color=self.color(index))
                    else:
                        break
            elif isinstance(float(self.__xAxis[0][0]), float):
                '''loops through all y values
                and adds them to the figure'''
                ax_0.tick_params(direction="out", top="off",
                                 right="off", pad=5)
                ax_1.tick_params(direction="out", top="off",
                                 right="off", pad=5)
                ax_2.tick_params(direction="out", top="off",
                                 right="off", pad=5)
                for index0, item0 in enumerate(self.__yAxis):
                    legend_index = 0
                    if index0 == 0:
                        for index, item in enumerate(item0):
                            if item is not None:
                                if index == 0 or index % 2 != 0:
                                    '''checks for the legend setting'''
                                    ax_0.plot(self.__xAxis[index], item,
                                              self.__lineStyle[index0],
                                              linewidth=3,
                                              color=self.color(
                                                     round(index / 2 + 0.40)),
                                              label=legend[index0]
                                              [legend_index])
                                    legend_index = legend_index + 1
                                else:
                                    ax_0.plot(self.__xAxis[index],
                                              item, self.__lineStyle[index0],
                                              linewidth=3,
                                              color=self.color(
                                                      round(index / 2 + 0.40)))
                        ax_0.set_yticks(self.__yAxis[0][0])
                    elif index0 == 1:
                        for index, item in enumerate(item0):
                            if item is not None:
                                if index == 0 or index % 2 != 0:
                                    print(legend[index0][legend_index])
                                    '''checks for the legend setting'''
                                    ax_1.plot(self.__xAxis[index], item,
                                              self.__lineStyle[index0],
                                              linewidth=1,
                                              color=self.color(
                                                     round(index / 2 + 0.40)),
                                              label=legend[index0]
                                              [legend_index])
                                    legend_index += 1
                                else:
                                    ax_1.plot(self.__xAxis[index],
                                              item, self.__lineStyle[index0],
                                              linewidth=1,
                                              color=self.color(
                                                      round(index / 2 + 0.40)))

                        ax_0.set_yticks(self.__yAxis[0][0] +
                                        self.__yAxis[1][0])
                    elif index0 == 2:
                        for index, item in enumerate(item0):
                            if item is not None:
                                if index == 0 or index % 2 != 0:
                                    '''checks for the legend setting'''
                                    ax_2.plot(self.__xAxis[index],
                                              item, self.__lineStyle[index0],
                                              linewidth=1.5,
                                              color=self.color(
                                                      round(index / 2 + 0.40)),
                                              label=legend[index0]
                                              [legend_index])
                                    legend_index += 1
                                else:
                                    ax_2.plot(self.__xAxis[index],
                                              item, self.__lineStyle[index0],
                                              linewidth=1.5,
                                              color=self.color(
                                                      round(index / 2 + 0.40)))
                        ax_0.set_yticks(self.__yAxis[0][0] +
                                        self.__yAxis[1][0] +
                                        self.__yAxis[2][0])

    #        elif isinstance(str(self.__xAxis[0]), str):
    #            plt.xticks(np.arange(len(xAxis)), xAxis)
    #            for index, item in enumerate(self.__yAxis):
    #                if item is not None:
    #                    ax.plot(np.arange(len(xAxis)), item, self.__lineStyle)

    #            ax.set_xlim(xmin = self.__xMin, xmax = self.__xMax)
        except:
            print("in Plotter.plot_xyLine: No format for xAxis found")


#        Plotter_Helper.figureLabelingXYLineHVLine(self, xLabel,
#                                                  yLabel, title,
#                                                  ax_0,rotation,
#                                                  bbox = len(self.__yAxis))
#        Plotter_Helper.font(self)

        ax_0.set_xticks(self.__xAxis[0])
        ax_0.annotate("Teilnetz Vogelstang", xy=(100, 400), xytext=(100, 400))
        ax_1.annotate("Teilnetz Nord", xy=(100, 699), xytext=(100, 699))
        ax_2.annotate("Teilnetz Ost", xy=(100, 1026), xytext=(100, 1026))
#        ax_0.set_xlim(0, yMax)
#        ax_1.set_yticks(self.__yAxis[1][0])
#        ax_2.set_yticks(self.__yAxis[2][0])
#        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#        plt.subplots_adjust(bottom =0.5)
#        plt.grid("off")
        return fig

    def plot_xyyLine(self, xAxis, yAxis0, yAxis1, legend0, legend1,
                     xLabel="", yLabel0="", yLabel1="",
                     title="", rotation=0, lineStyle0="-",
                     lineStyle1=["-", "-", "-"],
                     kind=None, alpha0=1, pltStyle='latex-classic'):
        """
        xAxis must be of []
        yAxis0 must be of [[]]
        yAxis1 must be of [[]]
        legends must be of []
        kind can be of bar, then first yAxis is a bar-plot
        """
        self.__xAxis = xAxis
        self.__yAxis0 = yAxis0
        self.__yAxis1 = yAxis1
        self.__lineStyle0 = lineStyle0
        self.__lineStyle1 = lineStyle1

#        Plotter_Helper.font(self)
        plt.style.use(pltStyle)
        fig = plt.figure(figsize=(12.6, 7.09))

        plt.xticks(np.arange(len(self.__xAxis)),
                   self.__xAxis,
                   rotation=rotation)  # stays here, otherwise no rotation

        ax_0 = fig.add_subplot(111)
        ax_1 = ax_0.twinx()
        if isinstance(self.__xAxis[0], datetime.date):
            self.__xAxis
            years = mdates.YearLocator()
            months = mdates.MonthLocator()
            days = mdates.DayLocator()
            yearsFmt = mdates.DateFormatter('%b %y')
            ax_0.xaxis_date()
            ax_0.xaxis.set_major_locator(months)
            ax_0.xaxis.set_major_formatter(yearsFmt)
            ax_0.xaxis.set_minor_locator(days)
            ax_1.xaxis_date()
            ax_1.xaxis.set_major_locator(months)
            ax_1.xaxis.set_major_formatter(yearsFmt)
            ax_1.xaxis.set_minor_locator(days)

        else:
            '''loops through all y values and adds them to the figure'''

        ax_0.tick_params(direction="out", pad=5)
        ax_1.tick_params(direction="out", pad=5)

        index0 = 0
        for index0, item in enumerate(self.__yAxis0):
            if item is not None:
                if kind is None:
                    ax_0.plot(np.arange(len(self.__xAxis)), item,
                              self.__lineStyle0, color=self.color(index0),
                              label=legend0[index0])
                elif kind == "bar":
                    ax_0.bar(np.arange(len(self.__xAxis)), item, width=0.3,
                             align="center", color=self.color(index0),
                             alpha=alpha0, label=legend0[index0])
        index0 = 0
        index1 = 0

        for index1, item1 in enumerate(self.__yAxis1):
                if item is not None:
                    ax_1.plot(np.arange(len(self.__xAxis)), item1,
                              self.__lineStyle1[index1],
                              color=self.color(index0 + index1 + 1),
                              label=legend1[index1], markersize=10)

#      # automatically update ylim of ax2 when ylim of ax1 changes.
##        ax_0.callbacks.connect("ylim_changed", convert_ax_1_to_celsius)
#        ax_0.plot(np.linspace(-40, 120, 100))
#        ax_1.set_ylim(0, 6)

#        Plotter_Helper.figureLabelingXYYLine(self, ax_0, ax_1, xLabel=xLabel,
#                                             yLabel0=yLabel0,
#                                             yLabel1=yLabel1, title=title)
#        Plotter_Helper.font(self)
#        plt.tight_layout()
        plt.show()

        return fig


    def plot_DHS(self, 
                 v_pipes_start_x=None,
                 v_pipes_start_y=None,
                 v_pipes_end_x=None,
                 v_pipes_end_y=None,
                 v_pipes_Q=None,
                 v_nodes_x=None,
                 v_nodes_y=None,
                 v_consumers_start_x=None,
                 v_consumers_start_y=None,
                 v_consumers_end_x=None,
                 v_consumers_end_y=None,
                 v_consumers_Q=None,
                 v_producers_start_x=None,
                 v_producers_start_y=None,
                 v_producers_end_x=None,
                 v_producers_end_y=None,
                 v_producers_Q=None,
                 title=''):
        if title is '':
            title = self.title

        fig, ax = self._newfig(self.figsize)
#        fig, ax = plt.subplots()
        if (v_pipes_start_x is not None and
                v_pipes_start_y is not None and
                v_pipes_end_x is not None and
                v_pipes_end_y is not None):
            self.plot_elements(v_pipes_start_x,
                               v_pipes_start_y,
                               v_pipes_end_x,
                               v_pipes_end_y,
                               v_element_Q=v_pipes_Q, fig=fig, ax=ax)
        if v_nodes_x is not None and v_nodes_y is not None:
             self.plot_nodes(v_nodes_x, v_nodes_y, ax=ax,
                            marker='o', marker_color='grey')
        if (v_consumers_start_x is not None and
                v_consumers_start_y is not None and
                v_consumers_end_x is not None and
                v_consumers_end_y is not None):
             self.plot_elements(v_consumers_start_x,
                                v_consumers_start_y,
                                v_consumers_end_x,
                                v_consumers_end_y,
                                v_element_Q=v_consumers_Q, fig=fig, ax=ax,
                                marker='v', marker_color='blue')
        print(v_producers_end_x, v_producers_end_y, v_producers_Q, v_producers_start_x,
              v_producers_start_y)
        if (v_producers_start_x is not None and
                v_producers_start_y is not None and
                v_producers_end_x is not None and
                v_producers_end_y is not None):
             self.plot_elements(v_producers_start_x,
                                v_producers_start_y,
                                v_producers_end_x,
                                v_producers_end_y,
                                v_element_Q=v_producers_Q, fig=fig, ax=ax,
                                marker='^', marker_color='red')

        return fig
    
    def plot_DHS2(self, 
                  v_pipes_start_x=None,
                  v_pipes_start_y=None,
                  v_pipes_end_x=None,
                  v_pipes_end_y=None,
                  v_pipes_Q=None,
                  v_nodes_x=None,
                  v_nodes_y=None,
                  v_consumers_start_x=None,
                  v_consumers_start_y=None,
                  v_consumers_end_x=None,
                  v_consumers_end_y=None,
                  v_consumers_Q=None,
                  v_producers_start_x=None,
                  v_producers_start_y=None,
                  v_producers_end_x=None,
                  v_producers_end_y=None,
                  v_producers_Q=None,
                  title=''):
        from matplotlib.collections import LineCollection
        
        xy = (np.random.random((1000, 2)) - 0.5).cumsum(axis=0)
        
        # Reshape things so that we have a sequence of:
        # [[(x0,y0),(x1,y1)],[(x0,y0),(x1,y1)],...]
#        x = np.stack([np.concatenate((v_pipes_start_x,
#                            v_consumers_start_x,
#                            v_producers_start_x)),
#                       np.concatenate((v_pipes_end_x,
#                                        v_consumers_end_x,
#                                        v_producers_end_x))],axis=0)
#        y = np.stack([np.concatenate((v_pipes_start_y,
#                       v_consumers_start_y,
#                       v_producers_start_y)),
#                        np.concatenate((v_pipes_end_y,
#                       v_consumers_end_y,
#                       v_producers_end_y))], axis=0)
#        xy = np.stack([x,y], axis=1)
        xy = xy.reshape(-1, 1, 2)
        segments = np.hstack([xy[:-1], xy[1:]])
        
        fig, ax = plt.subplots()
        coll = LineCollection(segments, cmap=plt.cm.gist_ncar)
        coll.set_array(np.random.random(xy.shape[0]))
        
        ax.add_collection(coll)
        ax.autoscale_view()
        
        plt.show()

    def plot_elements(self, v_start_x, v_start_y,
                      v_end_x, v_end_y,
                      v_element_Q=None,
                      title=None,
                      marker=None, marker_color=None,
                      line_style='-', line_color=None,
                      fig=plt.subplot(),
                      ax=plt.subplot()
                      ):
        '''plots Heatgrid elements
        input:\n
                v_start_x as []\n
                v_start_y as []\n
                v_end_x as []\n
                v_end_y as []\n
                v_Q as []\n
                v_nodes_x as []\n
                v_nodes_y as []\n
        output: matplotlib.figure.Figure'''

        self._formate_heatgrid()
        sPoint = [Point(xy) for xy in zip(v_start_x, v_start_y)]
        ePoint = [Point(xy) for xy in zip(v_end_x, v_end_y)]

        element_LineString = [LineString(xy) for xy in zip(sPoint, ePoint)]

        if v_element_Q is None:
            v_element_Q = np.zeros(len(element_LineString))
        gdf_elements = gp.GeoDataFrame({'elements': element_LineString,
                                        'Q': np.abs(v_element_Q)},
                                       geometry='elements')

        fig = gdf_elements.plot(ax=ax, column='Q', k=3, legend=True,
                                cmap='cool', scheme='quantiles',
                                linestyle=line_style,
                                )

        if marker is not None:
            gdf_elements_centroid = gdf_elements.centroid
            gdf_elements_centroid.plot(ax=ax, marker=marker,
                                       color=marker_color)
#        fig.colorbar(ax)

        return fig

    def plot_nodes(self, v_nodes_x, v_nodes_y,
                   marker='o', marker_color='grey', ax=plt.subplot()):

        nodes_Point = [Point(xy) for xy in zip(v_nodes_x, v_nodes_y)]
        gdf_nodes = gp.GeoDataFrame({'elements': nodes_Point},
                                        geometry='elements')
        gdf_nodes.plot(ax=ax, color=marker_color, marker=marker)
        return plt

    def _formate_heatgrid(self):
         plt.ioff
         plt.tick_params(
#            axis='both',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='off',  # labels along the bottom edge are off
            labelleft='off',
            left='off',
            right='off')




    def _figsize(self, scale):
        fig_width_pt = 469.755  # Get this from LaTeX using \the\textwidth
        inches_per_pt = 1.0 / 72.27  #  Convert pt to inch
        golden_mean = (np.sqrt(5.0) - 1.0) / 2.0
        # Aesthetic ratio (you could change this)
        fig_width = fig_width_pt * inches_per_pt * scale    # width in inches
        fig_height = fig_width * golden_mean              # height in inches
        fig_size = [fig_width, fig_height]
        return fig_size

    def _formate(self):
        rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman']})
        rc('text', usetex=False)
#        pgf_with_latex = {  # setup matplotlib to use latex for output
#            "pgf.texsystem": "pdflatex",
#            # change this if using xetex or lautex
#            "text.usetex": True,  # use LaTeX to write all text
#            "font.family": "serif",
#            "font.serif": [],
#            # blank entries should cause plots to inherit fonts from document
#            "font.sans-serif": [],
#            "font.monospace": [],
#            "axes.labelsize": 10,  # LaTeX default is 10pt font.
#            "font.size": 10,
#            "legend.fontsize": 8,
#            # Make the legend/label fonts a little smaller
#            "xtick.labelsize": 8,
#            "ytick.labelsize": 8,
#            "figure.figsize": self._figsize(0.9),
#            #  default fig size of 0.9 textwidth
#            "pgf.preamble": [
#                r"\usepackage[utf8x]{inputenc}",
#                #  use utf8 fonts becasue your computer can handle it :)
#                r"\usepackage[T1]{fontenc}",
#                #  plots will be generated using this preamble
#                ]
#                        }
#        mpl.rcParams.update(pgf_with_latex)

    def _newfig(self, width):
        plt.clf()
        fig = plt.figure(figsize=self._figsize(width))
        ax = fig.add_subplot(111)
        return fig, ax
    
    def plot_graph(self, nodes, edges_esNode,
                   nodes_label=None, edges_label=None,
                   weight = None):
        visual_style = {}
        visual_style["vertex_size"] = 15
        visual_style["vertex_shape"] = "circle"
        visual_style["layout"] = 'lgl'
        visual_style["bbox"] = (1024, 1024)
        visual_style["margin"] = 10

        g = igraph.Graph()
        g.add_vertices(nodes)
        g.add_edges(edges_esNode)
        g.es['label'] = edges_label
        g.vs['label'] = nodes_label
#        g.vs['shape'] = "circle"
#        g.vs['size'] ='5'
        fig = igraph.plot(g, **visual_style)
        fig.show()


        
        
if __name__ == "__main__":
    print('Plotter \t\t run directly \n')
    testPlotter = Plotter()
#    testPlotter.get_symbol(pointXY=Point(5, 5), scale=326, rotation=0,
#                           element='consumer')
#    nodes_name = ['A', 'B', 'C', 'D']
#    weight = [12,12,12,12]
#    elements_name = ['e1', 'e2', 'e3', 'e4']
#    edges_esNode = np.array([['A', 'B'], ['A', 'C'],
#                             ['C', 'B'],['B', 'C'],
#                             ['C', 'A'], ['B', 'A']])
#    
#    testPlotter.plot_graph(nodes_name, edges_esNode, nodes_label=nodes_name,
#                           edges_label=elements_name,
#                           weight=weight)
    pipes_start_x = [1,3]
    pipes_start_y = [1,3]
    pipes_end_x = [2,4]
    pipes_end_y = [2,4]
    pipes_Q = [1000, 10]
    nodes_x = [1, 3]
    nodes_y = [1, 3]
    consumers_start_x = [3]
    consumers_start_y = [4]
    consumers_end_x = [5]
    consumers_end_y = [5]

    fig =testPlotter.plot_elements(pipes_start_x, pipes_start_y, pipes_end_x,
                                   pipes_end_y)
    fig2 = testPlotter.plot_nodes(nodes_x, nodes_y)
    
    fig = testPlotter.plot_DHS(v_pipes_start_x=pipes_start_x,
              v_pipes_start_y=pipes_start_y,
              v_pipes_end_x=pipes_end_x,
              v_pipes_end_y=pipes_end_y,
              v_pipes_Q=pipes_Q,
              v_consumers_start_x=consumers_start_x,
              v_consumers_start_y=consumers_start_y,
              v_consumers_end_x=consumers_end_x,
              v_consumers_end_y=consumers_end_y)
    fig.savefig('test1')
    pipes_start_x.append(5)
    pipes_start_y.append(5)
    pipes_end_x.append(7)
    pipes_end_y.append(7)
    pipes_Q.append(10)

    fig.savefig('test')
    testPlotter.plot_DHS2()
#    plt.show()
else:
    print('Plotter \t\t was imported into another module')


#    def plot_HeatSource(self, v_producers_start_x,
#                        v_producers_start_y, v_producers_end_x,
#                        v_producers_end_y,  title=None,
#                        ax=plt.subplot()):
#        '''Plots all sources of Heatsource.\n
#        import: heatsource.getCalculations() or DataIO.importNumpyArr[i]'''
#
#        sources_sPoint = [Point(xy) for xy in zip(v_producers_start_x,
#                                                  v_producers_start_y)]
#        sources_ePoint = [Point(xy) for xy in zip(
#                heatsource.v_producers_end_x,
#                heatsource.v_producers_end_y)]
#        sources_LineString = [LineString(xy) for xy in zip(
#                                                sources_sPoint,
#                                                sources_ePoint)]
#
#        gdf = gp.GeoDataFrame({
#                'sPoints': sources_sPoint,
#                'ePoints': sources_ePoint,
#                'elements': sources_LineString,
#                'Q': np.abs(heatsource.v_producers_Q)},
#                              geometry='elements')
#
#        fig = gdf.plot(marker='p', color='red', markersize=2)
#        lines_centroid = gdf.centroid
#        lines_length = gdf.length
#        for center, l, sPoints, ePoints, element in zip(
#                lines_centroid,
#                lines_length,
#                gdf['sPoints'],
#                gdf['ePoints'],
#                heatsource.v_producers_element):
##            print(l)
#            rotation = np.arcsin((sPoints.x-ePoints.x) / l)
#            rotation = np.rad2deg(rotation)
#            self.get_symbol(pointXY=center, scale=l/4, rotation=rotation,
#                            fig=fig, ax=ax, element=element)
#        return fig
#
#    def plot_HeatSink(self, heatsink=None, title=None,
#                      fig=plt.figure(), ax=plt.subplot()):
#        '''Plots all sinks of Heatsink.\n
#        import: heatsink.getCalculations() or DataIO.importNumpyArr[i]'''
#
#        sinks_sPoint = [Point(xy) for xy in zip(
#                                                heatsink.v_consumers_start_x,
#                                                heatsink.v_consumers_start_y)]
#        sinks_ePoint = [Point(xy) for xy in zip(
#                                                heatsink.v_consumers_end_x,
#                                                heatsink.v_consumers_end_y)]
#        sinks_LineString = [LineString(xy) for xy in zip(
#                                                sinks_sPoint,
#                                                sinks_ePoint)]
#
#        gdf = gp.GeoDataFrame({'sPoints': sinks_sPoint,
#                               'ePoints': sinks_ePoint,
#                               'elements': sinks_LineString,
#                               'Q': np.abs(heatsink.v_consumers_Q)},
#                              geometry='elements')
#        fig = gdf.plot(marker='D', color='blue', markersize=2)
##        lines_centroid = gdf.centroid
##        lines_length = gdf.length
##        for center, l, sPoints, ePoints, element in zip(
##                lines_centroid,
##                lines_length, gdf['sPoints'],
##                gdf['ePoints'], heatsink.v_consumers_element):
##            rotation = np.arcsin((sPoints.x-ePoints.x) / l)
##            rotation = -np.rad2deg(rotation)
##            self.get_symbol(pointXY=center, scale=l/4, rotation=rotation,
##                            fig=fig, ax=ax, element=element)
##        fig.plot()
#
##        return fig
#    
#        def get_symbol(self, pointXY=Point(0, 0), scale=1,
#                   rotation=0, fig=plt.subplot(), ax=plt.subplot(),
#                   element=''):
#        # TODO implement plt.collection to speed up
#        # TODO use scale from gepandas to scale all lines
#        # TODO use translate to shift all lines
#        x = pointXY.x
#        y = pointXY.y
#        middle = (x, y)
#        radius = 0.5 * scale
#        if element is 'consumer':
#            leftdown = (-0.2 * scale + x, -0.25 * scale + y)
#            leftup = (leftdown[0], 0.25 * scale + y)
#            middle_lines = (0.2 * scale + x, 0 * scale + y)
#            middleup = (x, y + radius)
#            middledown = (x, y - radius)
#            top = (middleup[0], y + scale * 2)
#            down = (middledown[0], y - 1 * scale * 2)
#            rightup = (0.8 * scale + x, 0.25 * scale + y)
#            rightdown = (0.8 * scale + x, -0.25 * scale + y)
#
#            #  reads in coords into geopandas Geodataframe to rotate coords
#            coords = [(leftdown, rightdown),  # 0
#                      (leftdown, middle),  # 1
#                      (middle_lines, leftup),  # 2
#                      (leftup, rightup),  # 3
#                      (middleup, top),  # 4
#                      (middledown, down)]  # 5
#
#            lines = MultiLineString(coords)
#            gdf = gp.GeoDataFrame({'lines': lines}, geometry='lines')
#            gdf = gdf.rotate(rotation, origin=middle)
#
#            #  reads coords back into tuples
#            leftdown, rightdown = gdf.get_values()[0].coords
#            middle_lines, leftup = gdf.get_values()[2].coords
#            rightup = gdf.get_values()[3].coords[1]
#            middleup, top = gdf.get_values()[4].coords
#            middledown, down = gdf.get_values()[5].coords
#
#            circle = plt.Circle(middle, radius, linewidth=1.5,
#                                color='black', fill=False)
#            lines_x = [rightdown[0], leftdown[0],
#                       middle_lines[0], leftup[0], rightup[0]]
#            lines_y = [rightdown[1], leftdown[1],
#                       middle_lines[1], leftup[1], rightup[1]]
#
#            #  plot symbol
#            plt.plot(lines_x, lines_y, color='black')
#            ax.add_artist(circle)
#            #  plot line up
#            plt.plot([down[0], middledown[0]], [down[1],
#                     middledown[1]], color='black')
#            #  plot line down
#            plt.plot([top[0], middleup[0]], [top[1],
#                     middleup[1]], color='black')
#
#    #
#    #        fig.show()
#            '''####################'''
#        if element is 'producer':
#
#            leftdown = (x - 0.2 * scale , y - 0.3 * scale)
#            leftup = (leftdown[0] , y)
#            chimneyleft = (x + 0.1 * scale , leftup[1])
#            chimneyleftup = (chimneyleft[0], chimneyleft[1] + 0.3 * scale)
#            chimneyrightup = (chimneyleft[0] + 0.1 * scale, chimneyleftup[1])
#            chimneyrightdown = (chimneyrightup[0], leftdown[1])
#            middleup = (x, y + radius)
#            middledown = (x, y - radius)
#            top = (middleup[0], y + scale * 2)
#            down = (middledown[0], y - 1 * scale * 2)
#            
#            
#            coords = [(leftdown, leftup),
#                      (leftup, chimneyleft),
#                      (chimneyleft, chimneyleftup),
#                      (chimneyleftup, chimneyrightup),
#                      (chimneyrightup, chimneyrightdown),
#                      (chimneyrightdown, leftdown),
#                      (middleup, top),
#                      (middledown, down)]
#            lines = MultiLineString(coords)
#            gdf = gp.GeoDataFrame({'lines': lines}, geometry='lines')
#            gdf = gdf.rotate(rotation, origin=middle)
#            
#            # reads coords back into tuples
#            leftdown, leftup = gdf.get_values()[0].coords
#            chimneyleft, chimneyleftup = gdf.get_values()[2].coords
#            chimneyrightup, chimneyrightdown = gdf.get_values()[4].coords
#            leftdown = gdf.get_values()[5].coords[1]
#            middleup, top = gdf.get_values()[6].coords
#            middledown, down = gdf.get_values()[7].coords
#            
#            lines_x = [leftdown[0], leftup[0],
#                       chimneyleft[0], chimneyleftup[0],
#                       chimneyrightup[0], chimneyrightdown[0], leftdown[0]]
#            lines_y = [leftdown[1], leftup[1],
#                       chimneyleft[1], chimneyleftup[1],
#                       chimneyrightup[1], chimneyrightdown[1], leftdown[1]]
#            # plot symbol
#            plt.plot(lines_x, lines_y, color='red')
#            # plot line up
#            plt.plot([middleup[0], top[0]],
#                     [middleup[1], top[1]], color='black')
#            # plot line down
#            plt.plot([middledown[0], down[0]],
#                     [middledown[1], down[1]], color='black')
#            
#            circle = plt.Circle(middle, radius, linewidth=1.5,
#                                color='black', fill=False)
#            ax.add_artist(circle)
#        plt.axis('equal')
#
#        return fig