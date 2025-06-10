# -*- coding: utf-8 -*-
from combine import Combine
import time

class Baselines(Combine):
    def __init__(self,data,tiles,t_max,shape=None,bonus=1,algo="greedy"):
        super().__init__(data,tiles,t_max,shape,bonus)
        if algo == "greedy":
            self.method = self.findTileGreedy
        elif algo == "naive":
            self.method = self.findTileNaive

    def findTileGreedy(self):
        smallesterror = 1
        for i in [x for x in self.tilegroup if x not in self.chosen_factors]:
            error = self.getError(self.chosen_factors + [i])
            if error < smallesterror:
                smallesterror = error
                besttile = i
        if smallesterror < self.current_error:
            self.current_error = smallesterror
            return besttile, True
        else:
            return None, False
        
    def findTileNaive(self):
        best_tile = None
        found_tile = False
        biggestvalue = 0
        for i in [x for x in self.tilegroup if x not in self.chosen_factors]:
            value = len(self.tiles[i]) - self.covered_zeros[i]
            if value > biggestvalue:
                biggestvalue = value
                best_tile = i
                found_tile = True
        self.current_error = self.getError(self.chosen_factors + [best_tile])
        return best_tile, found_tile

    def findTiles(self):
        cover = []
        errors = []
        for j in range(self.t_max-1):
            start = time.time()
            next_tile,found = self.method()
            end = time.time()
            self.times.append(end-start)
            if not found:
                break
            else:
                errors.append(self.current_error)
                self.chosen_factors.append(next_tile)
                truennz = self.getTrueCover(self.chosen_factors)
                covered_zeros = self.getZeroCover(self.chosen_factors)
                cover.append((truennz,covered_zeros))
        return self.chosen_factors,self.times,cover,errors