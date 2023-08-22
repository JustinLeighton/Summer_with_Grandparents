# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 13:52:59 2023

@author: Justin Leighton
"""

# Import packages
from random import random
from math import floor
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Movement mapping
def move(loc: str, sunny: bool) -> str:
    if loc=='farm':
        return 'coffee' if sunny else 'diner'
    if loc=='diner':
        return 'park' if sunny else 'farm'
    if loc=='coffee':
        return 'tennis' if sunny else 'farm'
    if loc=='tennis':
        return 'park' if sunny else 'coffee'
    if loc=='park':
        return 'tennis' if sunny else 'diner'
    raise 'error'

# One day's movement simulated
def day(key: dict) -> np.array:
    sunny = random() > 0.5
    switch_flag = random() < 0.3 if sunny else random() > 0.5
    switch_when = floor(random() * 5) if switch_flag else -1  
    loc = 'farm'
    hst = np.array([1,0,0,0,0], dtype=int)
    for mvmt in range(0, 5):
        if mvmt==switch_when:
            sunny = not(sunny)
            switch_when = -1
        loc = move(loc, sunny)
        hst[key[loc]] += 1
        
    return hst

# Simulation - Modify n to vary number of simulated days
n = 10000000
locMap = {'farm': 0, 'diner': 1, 'coffee': 2, 'park': 3, 'tennis': 4}
days = np.zeros(shape=(n,5), dtype=int)
for d in range(0,n):
    days[d] = day(locMap)
debug = pd.DataFrame(days, columns=locMap.keys())
debug = debug.groupby(list(locMap.keys())).size().reset_index(name='counts')
debug['pct'] = debug['counts'] / n
print(debug)
    
# Summarize data
summary = np.zeros(shape=(1,5), dtype=int)
for i in range(0,5):
    summary[:,i] = np.sum(days[:,i] > 0)
summary = pd.DataFrame(data = {'loc': list(locMap.keys()),
                                'n': summary.tolist()[0]})
summary['pct'] = summary['n'] / n

# Plot
people = list(locMap.keys())
y_pos = list(locMap.values())
performance = summary['pct']
fig, ax = plt.subplots()
hbars = ax.barh(y_pos, performance, align='center')
ax.set_yticks(y_pos, labels=people)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Probability')
ax.set_title(f'Days simulated: {n}')
ax.bar_label(hbars, fmt='%.4f')
ax.set_xlim(right=1.1)  # adjust xlim to fit labels
plt.show()


