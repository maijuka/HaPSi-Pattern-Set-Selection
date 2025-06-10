# HaPSi-Pattern-Set-Selection

This repository contains the implementations for the algorithms in the paper
> **Hashing for Fast Pattern Set Selection**<br>
> Maiju Karjalainen and Pauli Miettinen<br>
> To appear at ECML-PKDD 2025

## Contents

* _hapsi.py_ contains implementation for the main algorithm HaPSi
* _baselines.py_ contains implementations for the "Greedy" and "Naive" algorithms used for comparison against HaPSi
* _combine.py_ contains common initialization steps and error computations


## Data format

All algorithms need as an input the original data matrix and the rank-1 matrices (patterns, tiles). Flatten the input matrices in column-major (Fortran-style) order, and create a list containing indices of the 1s in the flattened format. For example:
```math
\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 1 \\ 1 & 0 & 1 \end{bmatrix}
```
Should be input as [0,2,4,7,8].

All algorithms return the chosen patterns (index of the tile in the list that was given as an input), the runtimes for finding each tile, how many ones and zeros each found tile covered, and the reconstruction errors.

## Parameters for all algorithms

* data = the indices of 1s of the original data matrix in the flattened format
* tiles = list of lists containing the flattened tiles
* t_max = maximum number of patterns searched 
* shape = shape of the data matrix (rows,cols)
* bonus = multiplier to weigh the 1s in the patterns, used for sparse matrices, default value 1

## Parameters for HaPSi

* nb_hashbalues = how many times the hash values are computed (estimate is the median over these values)
* k = k for the bottom-k hashing method
* m = how many times the true reconstruction error is computed during the search phase before stopping

## Running experiments with HaPSi

To run HaPSi experiments, use the class Hapsi in hapsi.py. Below is an example of how to run an experiment searching for a maximum of 200 patterns with HaPSi.
```
h = Hapsi(data,tiles,200,nb_hashvalues=15,k=30,shape=(1000,1200))
patterns,runtime,cover,errors = h.findTiles()
```

## Running experiments with the baseline algorithms

To run the Greedy and Naive algorithms, use the baselines.py. 
```
g = Baselines(data,tiles,200,shape=(1000,1200),algo="greedy")
patterns,runtime,cover,errors = g.findTiles()

n = Baselines(data,tiles,200,shape=(1000,1200),algo="naive")
patterns,runtime,cover,errors = n.findTiles()
```




