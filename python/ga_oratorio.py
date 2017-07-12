#!/usr/bin/python
import sys
import os
import math

# add script folder to path for imports
full_path = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(full_path)

import test


class ga_oratorio:

    def __init__(self):
        print("hello, ga")

    def roulette_select(self, ftns, pcnt):
        # input: chromosome fitnesses, output: indices of surviving chromosomes
        # fitness closer to 0: better
        # smaller values should have a bigger chunk; invert (val = 1-val)
        s = min(ftns)
        # subtract every value from s to invert importance
        ftns[:] = [1 - x / s for x in ftns]
        print(ftns)

        # create roulette_wheel
        ss = 0
        wheel = []
        for n in ftns:
            ss = ss + n
            wheel += [ss]
        print(wheel)

        surv_ids = []
        # pcnt == percentage of survivers
        surv = math.ceil(len(ftns) * pcnt)
        # return i survivers
        for i in range(0, surv):
            # random
            r = (int.from_bytes(os.urandom(4), byteorder="big")) % wheel[-1]
            # pick a chromosome
            idx = 0
            for j in range(0, len(wheel)):
                idx = j
                if r < wheel[j]:
                    break
            surv_ids += [idx]
        print(surv_ids)
        return surv_ids


class chromosome:

    def __init__(self):
        print("hello, chromosome")

    def fitness():
        print("fitness")


if __name__ == "__main__":
    ga = ga_oratorio()
    ga.roulette_select([-30, -50, -1, -20, -70], 5)








