# -*- coding: utf-8 -*-
"""
Created on Sat Jan 07 16:50:22 2017
@author: jpelda"""

import sys
import os

from Finder import Finder
from Pipe import Pipe
from Node import Node

import numpy as np


class HeatGrid():

    def __init__(self, tableOfPipes, tableOfNodes,
                 nodeSupply=None, nodeReturn=None):
        '''
        input:
            tableOfPipes = [] # contains all Pipes of network, \
            allocation Dictionary can be found in Dictionary \n
            tableOfNodes = [] # same as tabelOfPipes but for nodes \n
            nodeSupply = [] is given by 
            [[val, None],[val, None], ...], out of this all pipes with
            val and additional numbers are written into pipes_sp\n
            nodeReturn = [] is given by 
                [[val, None], [val, None], ...], out of this all pipes with
                val and additional numbers are written into pipes_rp\n
        '''

        self._instancesPipe = self.__importPipes(tableOfPipes)
        self._instancesNode = self.__importNodes(tableOfNodes)


        arr = self.__pipes()
        self.v_pipes_index = arr[0]
        self.v_pipes_start_x = arr[1]
        self.v_pipes_start_y = arr[2]
        self.v_pipes_end_x = arr[3]
        self.v_pipes_end_y = arr[4]
        self.v_pipes_sNode = arr[5]
        self.v_pipes_eNode = arr[6]
        self.v_pipes_length = np.asarray(arr[7])
        self.v_pipes_diameter_inner = np.asarray(arr[8])
        self.v_pipes_diamter_outer = np.asarray(arr[9])
        self.v_pipes_sHeight = np.asarray(arr[10])
        self.v_pipes_eHeight = np.asarray(arr[11])
        self.v_pipes_roughness = np.asarray(arr[12])
        self.v_pipes_element = arr[13]
        self.v_pipes_Q = np.asarray(arr[14])
        self.v_pipes_m = np.asarray(arr[15])
        self.v_pipes_Ta = np.asarray(arr[16])
        self.v_pipes_Tb = np.asarray(arr[17])
        self.v_pipes_Pa = np.asarray(arr[18])
        self.v_pipes_Pb = np.asarray(arr[19])
        self.v_pipes_m_max = tableOfPipes['m_max']
        
        arr = self.__nodes()
        self.v_nodes_index = arr[0]
        self.v_nodes_x = arr[1]
        self.v_nodes_y = arr[2]
        self.v_nodes_name = arr[3]
        self.v_nodes_height = np.asarray(arr[4])
        self.v_nodes_element = arr[5]

        self.v_pipes_seNode = np.column_stack(
                                    (self.v_pipes_sNode, self.v_pipes_eNode))
        seNodes_sprp = self.__get_pipes_sprp(nodeSupply)
        self.v_pipes_sprp = self.__set_pipes_sprp(seNodes_sprp)
        self.v_nodes_sprp = self.__set_nodes_sprp(seNodes_sprp)
        
        self.v_nodes_T = 0
        self.v_nodes_P = 0

#        self.v_pipes_index = tableOfPipes['index']
#        self.v_pipes_start_x = tableOfPipes['start_x']
#        self.v_pipes_start_y = tableOfPipes['start_y']
#        self.v_pipes_end_x = tableOfPipes['end_x']
#        self.v_pipes_end_y = tableOfPipes['end_y']
#        self.v_pipes_sNode = tableOfPipes['sNode']
#        self.v_pipes_eNode = tableOfPipes['eNode']
#        self.v_pipes_length = tableOfPipes['length']
#        self.v_pipes_diameter_inner = tableOfPipes['diameter_inner']
#        self.v_pipes_diameter_middleinner = tableOfPipes['diameter_middleinner']
#        self.v_pipes_diameter_middleouter = tableOfPipes['diameter_middleouter']
#        self.v_pipes_diamter_outer = tableOfPipes['diameter_outer']
#        self.v_pipes_sHeight = tableOfPipes['start_height']
#        self.v_pipes_eHeight = tableOfPipes['end_height']

#        
#        self.v_pipes_conductivity_inner = tableOfPipes['conductivity_inner']
#        self.v_pipes_conductivity_middle = tableOfPipes['conductivity_middle']
#        self.v_pipes_conductivity_outer = tableOfPipes['conductivity_outer']


        self.__str__(nodes=0)
        print("%i pipes \t----> OK" % (len(self.v_pipes_index)))
        self.__str__(pipes=0)
        print("%i nodes \t----> OK\n" % (len(self.v_nodes_index)))
        self._calcVals = []

    def pipes(self, i=slice(None, None)):
        return self._instancesPipe[i]

    def nodes(self, i=slice(None, None)):
        return self._instancesNode[i]

    def __get_pipes_sprp(self, nodeSupply):
        '''
        gets an arr of all supply pipes,
        find by class Finder method findAllItems
        '''
        search_list = []
        for item in self.pipes():
            search_list.append(item.seNode)
        arr = Finder().findAllItems(nodeSupply,
                                    self.v_pipes_seNode)
        return arr

    def __set_pipes_sprp(self, arr):
        '''
        names all pipes at sp_rp with 1 for supply pipe and 0 for return pipe
        '''
        arr_pipes = self.v_pipes_seNode

        for index, item in enumerate(arr_pipes):
            for item1 in arr:
                if np.array_equal(item, item1):
                    self.pipes(index).sprp = 1
                    break
                else:
                    self.pipes(index).sprp = 0

        retarr_sprp = [0]*len(self.pipes())
        for index, item in enumerate(self.pipes()):
            retarr_sprp[index] = item.sprp

        return retarr_sprp

    def __set_nodes_sprp(self, arr):
        '''
        names all nodes at sprp with 1 for supply node and 0 for return node
        '''
        arr_nodes = self.v_nodes_name
        for index, item in enumerate(arr_nodes):
            for item1 in arr:
                if np.array_equal(item, item1[0])\
                    or np.array_equal(item, item1[1]):
                    self.nodes(index).sprp = 1
                    break
                else:
                    self.nodes(index).sprp = 0

        retarr_sprp = [0]*len(self.nodes())
        for index, item in enumerate(self.nodes()):
            retarr_sprp[index] = item.sprp

        return retarr_sprp

    def __importPipes(self, df):
        arr = []
        for index, row in df.iterrows():
            arr.append(Pipe(index, row))
        return arr

    def __importNodes(self, df):
        arr = []
        for index, row in df.iterrows():
            arr.append(Node(index, row))
        return arr

    def __pipes(self):
        length = len(self.pipes())
        retarr_index = np.asarray([0.]*length)
        retarr_start_x = np.asarray([0.]*length)
        retarr_start_y = np.asarray([0.]*length)
        retarr_end_x = np.asarray([0.]*length)
        retarr_end_y = np.asarray([0.]*length)
        retarr_sNode = [0]*length
        retarr_eNode = [0]*length
        retarr_length = np.asarray([0.]*length)
        retarr_diameter_inner = np.asarray([0.]*length)
        retarr_diameter_outer = np.asarray([0.]*length)
        retarr_start_height = np.asarray([0.]*length)
        retarr_end_height = np.asarray([0.]*length)
        retarr_roughness = np.asarray([0.]*length)
        retarr_element = [0.]*length
        retarr_Q = np.asarray([0.]*length)
        retarr_m = np.asarray([0.]*length)
        retarr_Ta = np.asarray([0.]*length)
        retarr_Tb = np.asarray([0.]*length)
        retarr_Pa = np.asarray([0.]*length)
        retarr_Pb = np.asarray([0.]*length)
        retarr_m_max = np.asarray([0.]*length)
        for index, item in enumerate(self.pipes()):
            retarr_index[index] = item.index
            retarr_start_x[index] = item.start_x
            retarr_start_y[index] = item.start_y
            retarr_end_x[index] = item.end_x
            retarr_end_y[index] = item.end_y
            retarr_sNode[index] = item.sNode
            retarr_eNode[index] = item.eNode
            retarr_length[index] = item.length
            retarr_diameter_inner[index] = item.diameter_inner
            retarr_diameter_outer[index] = item.diameter_outer
            retarr_start_height[index] = item.start_height
            retarr_end_height[index] = item.end_height
            retarr_roughness[index] = item.roughness
            retarr_element[index] = item.element
            retarr_Q[index] = item.Q
            retarr_m[index] = item.m
            retarr_Ta[index] = item.Ta
            retarr_Tb[index] = item.Tb
            retarr_Pa[index] = item.Pa
            retarr_Pb[index] = item.Pb
            retarr_m_max[index] = item.m_max_set
        return retarr_index, retarr_start_x, retarr_start_y, retarr_end_x,\
            retarr_end_y, retarr_sNode, retarr_eNode,\
            retarr_length, retarr_diameter_inner, retarr_diameter_outer,\
            retarr_start_height, retarr_end_height, retarr_roughness,\
            retarr_element, retarr_Q, retarr_m, retarr_Ta, retarr_Tb,\
            retarr_Pa, retarr_Pb, retarr_m_max


    def __nodes(self):
        length = len(self.nodes())
        retarr_index = [0]*length
        retarr_x = [0]*length
        retarr_y = [0]*length
        retarr_name = [0]*length
        retarr_height = [0]*length
        retarr_element = [0]*length
        for index, item in enumerate(self.nodes()):
            retarr_index[index] = item.index
            retarr_x[index] = item.x
            retarr_y[index] = item.y
            retarr_name[index] = item.name
            retarr_height[index] = item.height
            retarr_element[index] = item.element
        return retarr_index, retarr_x, retarr_y,\
            retarr_name, retarr_height, retarr_element


    def setCalculations(self):
        attr = self.__dict__
        attr = {item: attr[item] for item in attr if item not in
                ("_instancesPipe",
                 "_instancesNode",
                 "__str__",
                 "calcVals")}
        self._calcVals.append(attr)


    def getCalculations(self, i=slice(None,None)):
        return self._calcVals[i]

    def pipes_operatingLoad(self):
        arr = self.v_pipes_m_max / 100
        arr = self.v_pipes_m / arr
        return arr

    def __str__(self, pipes=1, nodes=1):
        if pipes is 1:

            for element, sprp, sNode, eNode, length,\
                diameter_inner, diameter_outer, sprp in zip(
                        self.v_pipes_element, self.v_pipes_sprp,
                        self.v_pipes_sNode, self.v_pipes_eNode,
                        self.v_pipes_length,
                        self.v_pipes_diameter_inner,
                        self.v_pipes_diamter_outer,
                        self.v_pipes_sprp):
                print("%s: sprp %i length %4.1f [m] "
                      "d_i %4.2f [m] d_o %4.2f [m] sNode %s "
                      "eNode %s" % (element, sprp, length,
                                    diameter_inner, diameter_outer,
                                    sNode, eNode))
        if nodes is 1:
            for element, name, sprp in zip(
                                            self.v_nodes_element,
                                            self.v_nodes_name,
                                            self.v_nodes_sprp):
                        print("%s: sprp %s \t\t\t\t\t\t\t\t\t Node %s" % (
                                element, sprp, name))

if __name__ == "__main__":
    from DataIO import DataIO
    import Dictionary

    print('HeatGrid \t\t run directly')

    DataIO = DataIO(
                os.path.dirname(os.getcwd()) + os.sep +
                'input' + os.sep + 'TestNetz',
                os.path.dirname(os.getcwd()) + os.sep +
                'output' + os.sep + 'TestNetz')

    heatgrid_nodes = DataIO.importDBF(
            'KTestNetz.DBF', dtype=Dictionary.STANET_nodes_allocation)

    heatgrid_pipes = DataIO.importDBF(
            'STestNetz.DBF', dtype=Dictionary.STANET_pipes_allocation)

    testGrid = HeatGrid(heatgrid_pipes, heatgrid_nodes, [["K1017", None]])


else:
    print('HeatGrid \t\t was imported into another module')
    sys.path.append(os.getcwd())
#    print(os.getcwd())
