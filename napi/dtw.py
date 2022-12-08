# AUTOGENERATED! DO NOT EDIT! File to edit: ../004_dtw.ipynb.

# %% auto 0
__all__ = ['dtw']

# %% ../004_dtw.ipynb 2
from numba import jit
import numpy as np


# %% ../004_dtw.ipynb 3
@jit()
def _local_squared_dist(x, y):
    return (x - y)*(x-y)


@jit()
def dtw(s1, s2):
    l1 = s1.shape[0]
    l2 = s2.shape[0]
    cum_sum = np.full((l1 + 1, l2 + 1), np.inf)
    cum_sum[0, 0] = 0.

    for i in range(l1):
        for j in range(l2):

            cum_sum[i + 1, j + 1] = _local_squared_dist(s1[i], s2[j])
            cum_sum[i + 1, j + 1] += min(
                cum_sum[i, j + 1],
                cum_sum[i + 1, j],
                cum_sum[i, j])
    return cum_sum[-1, -1]

