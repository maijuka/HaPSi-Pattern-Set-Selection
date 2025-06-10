# -*- coding: utf-8 -*-
import numpy as np
from sympy import nextprime
import math
from operator import itemgetter
from combine import Combine
import time

class Hapsi(Combine):
    def __init__(self,data,tiles,t_max,nb_hashvalues=11,k=30,shape=None,bonus=1,m=30):
        super().__init__(data,tiles,t_max,shape,bonus)
        self.k = k
        self.p = 0.8
        self.alpha = 0.5
        self.rowcol = []
        start = time.time()
        for factor in self.tiles:
            rows = set()
            cols = set()
            for ind in factor:
                row = ind%self.shape[0]
                rows.add(row)
                col = math.floor(ind/self.shape[0])
                cols.add(col)
            self.rowcol.append([list(rows),list(cols)])
        self.hashmatrix,tilegroup = self.makeHashMatrix(nb_hashvalues)
        self.combinedmatrix = self.hashmatrix.copy()
        group = tilegroup
        if group is None:
            self.tilegroup = range(0,len(tiles))
        else:
            self.tilegroup = group
        self.m = m
        end = time.time()
        self.times.append(end-start)

    def combineHashes(self,H,Hj):
        comb = set(H).union(set(Hj))
        return sorted(list(comb))[:self.k]
    
    def findTileHapsi(self):
        tile_candidates = []
        best_tile = None
        found_tile = False
        for i in [x for x in self.tilegroup if x not in self.chosen_factors]:
            ests = []
            for t,h in enumerate(self.combinedmatrix):
                if self.hashmatrix[t][i] != [-1]:
                    self.combinedmatrix[t][i] = self.combineHashes(self.combinedmatrix[t][self.chosen_factors[-1]],self.combinedmatrix[t][i])
                    ests.append(self.k/self.combinedmatrix[t][i][-1])
            value = self.bonus*self.alpha*(np.median(ests)) - (1-self.alpha)*self.covered_zeros[i]
            tile_candidates.append((value,i))
        tile_candidates = sorted(tile_candidates,key=itemgetter(0),reverse=True)
        for (value,i) in tile_candidates[:self.m]:
            if (besterror := self.getError(self.chosen_factors + [i])) < self.current_error: 
                self.current_error = besterror
                best_tile = i
                found_tile = True
                break
        return best_tile, found_tile
    
    def findTiles(self):
        cover = []
        errors = []
        for j in range(self.t_max-1):
            start = time.time()
            next_tile,found = self.findTileHapsi()
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
    
    def makeHashMatrix(self,size):
        newhashvals = [self.makeHashvals(self.shape[0],size),self.makeHashvals(self.shape[1],size)]
        newhashes = []
        tilegroup = set()
        for hi in range(size):
            hashes = []
            for fi, factor in enumerate(self.rowcol):
                a = newhashvals[0][:,hi][factor[0]]
                b = newhashvals[1][:,hi][factor[1]]
                S=set()
                F=set()
                if len(a)*len(b)>self.k:
                    a.sort()
                    b.sort()
                    p = self.p
                    s_ = 0
                    for bj in b:
                        while (a[s_]-bj)%1 > (a[(s_-1)%len(a)]-bj)%1:
                            s_ = (s_+1)%len(a)
                        s = s_
                        aloop = 0
                        while ((a[s]-bj)%1) < p and aloop < len(a):
                            F.add((a[s]-bj)%1)
                            if len(F)==self.k:
                                S = sorted(list(S.union(F)))[:self.k]
                                p = S[-1]
                                S = set(S)
                                F=set()
                            s = (s+1)%len(a)
                            aloop += 1
                    S = sorted(list(S.union(F)))[:self.k]
                    if len(S) == self.k:
                        hashes.append(list(S))
                        tilegroup.add(fi)
                    else:
                        hashes.append([-1])
                else:
                    hashes.append([-1])
            newhashes.append(hashes)
        tilegroup = list(tilegroup)
        return newhashes, tilegroup

    def makeHashvals(self,n,size=1):
        next_prime = nextprime(n)
        coeffA = np.random.randint(2,100,size)
        coeffB = np.random.randint(2,100,size)
        if size == 1:
            return ((np.outer(np.arange(n), coeffA) + coeffB)%next_prime/next_prime).flatten()
        return ((np.outer(np.arange(n), coeffA) + coeffB)%next_prime/next_prime)