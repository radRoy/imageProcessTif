import math
import stat
import statistics

import random as r
r.seed(240220)

#import numpy as np

sequence = []
for i in range(7):
    x = r.randint(1, 7)
    while x in sequence:
        x = r.randint(1, 7)
    sequence.append(x)
print(sequence)
# sequence for dataset11: [7, 5, 2, 1, 4, 6, 3] - see [imageProcessTif]/README.md for info
# [test, val, train_1-5]