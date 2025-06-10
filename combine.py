# -*- coding: utf-8 -*-
import numpy as np
import sys
import time

class Combine():
    def __init__(self,data,tiles,t_max,shape=None,bonus=1):
        self.data = data
        self.tiles = tiles
        if shape is None:
            sys.exit()
        else:
            self.shape = shape
        self.t_max = t_max
        self.bonus = bonus
        self.covered_zeros = []
        self.covered_zeros_frac = []
        self.tilegroup = range(0,len(tiles))
        start = time.time()
        for i,tile in enumerate(tiles):
            zeros = self.getCoveredZeros(tile)
            self.covered_zeros.append(zeros)
            self.covered_zeros_frac.append(zeros/len(tile))

        best_error = np.inf
        for i,tile in enumerate(tiles):
            error = len(self.data) - (len(tile)-self.covered_zeros[i]) + self.covered_zeros[i]
            if error < best_error:
                best_error = error
                best_tile = i
        self.biggest_tile = best_tile
        self.chosen_factors = [best_tile]    
        self.current_error = self.getError(self.chosen_factors)
        end = time.time()
        self.times = [end-start]

    def getCoveredZeros(self,factor):
        return len(set(factor) - set(self.data))

    def getTrueCover(self,factors):
        cands = [set(self.tiles[x]) for x in factors]
        candcover = set.union(*cands)
        return len(set(self.data).intersection(candcover))
    
    def getZeroCover(self,factors):
        cands = [set(self.tiles[x]) for x in factors]
        candcover = set.union(*cands)
        return len(candcover.difference(set(self.data)))
    
    def getError(self,factors):
        cands = [set(self.tiles[x]) for x in factors]
        candcover = set.union(*cands)
        zeros = len(candcover.difference(set(self.data)))
        ones = len(set(self.data).difference(candcover))
        return (zeros+(self.bonus*ones))/(np.prod(self.shape)-len(self.data) + self.bonus*len(self.data))