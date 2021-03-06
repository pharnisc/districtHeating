# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:30:59 2017

@author: jpelda
"""
import numpy as np

def inzidenzmatrix(rows, cols, inzidenzmatrix_name):
    '''
    arranges an inzidenzmatrix for a directed graph for further
    calculations:
                pipes
                f_0  f_1  f_2  f_3
        node 0   1    0    -1   0
        node 1   0    0    1   -1
    Flows towards a node are -1. Flows away from node are 1.
    
    input:
        rows = []
        cols = [[,],[,]] # cols[0] is away from value of row -> -1,\
                            cols[1] is towards value of row-> 1
    '''
    inzMatrix = np.array(len(rows) * [len(cols)*[0]])

    for index, item in enumerate(rows):
        for index_cols, item_cols in enumerate(cols):
            if item_cols[0] == item:
                inzMatrix[index][index_cols] = 1
        for index_cols, item_cols in enumerate(cols):
            if item_cols[1] == item:
                inzMatrix[index][index_cols] = -1

#    print(str(inzidenzmatrix_name))
#    for row, item in zip(rows, returnMatrix):
#        print(str(row), str(item), sep='  |  ')
#    print('\n')

    return inzMatrix

def adjacencyMatrix(nodes, edges_seNode):
    '''
    arranges an adjacencyMatrix undirected:
            A B C D
    A       0 0 1 0
    B       0 0 1 1
    C ...
    D ...
    
    input:
        nodes = numpy.array([])
        edges = numpy.array([]) defining the conjunctions.
    return:
        adjacencyMatrix = numpy.array([]) --> square array
    '''
    pass


if __name__ == "__main__":
    print('Plotter \t\t run directly \n')
    edges_seNode = np.array([['A', 'B'], ['A', 'C'], ['C', 'B'],['B', 'C'], ['C', 'A'], ['B', 'A']])
    nodes = np.array(['A', 'B', 'C', 'D'])
    adjacencyMatrix(nodes, edges_seNode)
else:
    print('Plotter \t\t was imported into another module')

