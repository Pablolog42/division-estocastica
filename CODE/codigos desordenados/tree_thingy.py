# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 10:34:01 2023

@author: sepul
"""

import networkx as nx
import random
import numpy as np

    
def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.  
    Licensed under Creative Commons Attribution-Share Alike 
    
    If the graph is a tree this will return the positions to plot this in a 
    hierarchical layout.
    
    G: the graph (must be a tree)
    
    root: the root node of current branch 
    - if the tree is directed and this is not given, 
      the root will be found and used
    - if the tree is directed and this is given, then 
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given, 
      then a random choice will be used.
    
    width: horizontal space allocated for this branch - avoids overlap with other branches
    
    vert_gap: gap between levels of hierarchy
    
    vert_loc: vertical location of root
    
    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))
            
    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''
    
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos

            
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

#G= nx.read_gpickle('myGraph.gpickle')

#nx.draw(G, tree, node_color= 'red', node_size= 10)


def clean(G): 
    '''  Toma un grafo G y saca los nodos que tienen grado dos, quitando también las
    conexiones entre esos nodos'''
    import copy 
    copia= copy.copy(G)
    nodos= G.nodes
   
    
    for i in range(len(copia.nodes)): 
        
        if copia.degree(i)== 2: 
            neighbours = [n for n in copia[i]]
            copia.add_edge(neighbours[0], neighbours[1])
            copia.remove_node(i)

        else: 
            pass 
            
    return  nodos , copia  



def histogram(G): 
    
   degree_sequence= sorted([d for n,d in G.degree()], reverse=True)
   from collections import Counter
   import matplotlib.pyplot as plt

   ndegree= Counter(degree_sequence)
   deg, cnt = zip(*ndegree.items())
   plt.title('Node degree distribution')
   plt.xlabel(r'Node degree $k$ ')
   plt.ylabel(r'Distribution $\mathcal{P(k)}$')
   plot= plt.bar(deg, cnt, width=0.80, color='b')
   
   return plot 

