import numpy as np
import math
from scipy.stats import beta

YEARS = 30
DAYS_PER_YEAR = 365
TRIALS = 100_000

def rp(x):
    return 1. / (1. - math.exp(-DAYS_PER_YEAR * x))
    # return 1./(DAYS_PER_YEAR*x)

def trial():
    extremes = []
    for i in range(YEARS):
        events = np.random.uniform(size = DAYS_PER_YEAR)
        most_extreme = rp(min(events))
        extremes.append(most_extreme)
    extremes.sort()
    return extremes[::-1]

def bb(k):
    return 1./(1-beta.ppf(0.5, 30-k, k+1))


thirties = [trial() for _ in range(TRIALS)]
quartiles = []
zipped = list(zip(*thirties))
for z in zipped:
    lz = list(z)
    lz.sort()
    quartiles.append( (lz[TRIALS//100], lz[TRIALS//4],lz[TRIALS//2], lz[(TRIALS * 3) // 4], lz[(TRIALS*99)//100] ))

#     "---- ------- ------- ------- ------- ------- ------- ------- ----------"
print("Rank  Simple     FEH  Theor.      1%      Q1  Median      Q3        99%")
for (i,q) in enumerate(quartiles):
    print (f"{i+1:4d} {YEARS/(i+1):7.3f} {(YEARS+0.12)/(i+0.56):7.3f} {bb(i):7.3f} {q[0]:7.3f} {q[1]:7.3f} {q[2]:7.3f} {q[3]:7.3f} {q[4]:10.3f}")
