#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from lmfit import minimize, Minimizer, Parameters, Parameter, report_fit


k  = 0.0369

def predict(params, time, current):
    globals().update(params.valuesdict())
    I = current[0]
    sol = [ t*k*I/Cr + k*I*Jr/Cr**2*np.exp(-t*Cr/Jr) - k*I*Jr/Cr**2 for t in time]
    print(k*I/Cr)
    return sol

def energy(params, data):
    E = 0.
    for run in data:
        y = predict(params, run[0], run[1])
        for i in range(len(run[2])):
            E = E + ((y[i]-run[2][i])/run[2][-1]) **2
    print(params.valuesdict(),"\n", E)
    return E


params = Parameters()
#params.add('k',  value=0.0369,   min=.0001, max=.5)
params.add('Jr', value=0.001184, min=.00001,    max=.5)
params.add('Cr', value=0.00001,  min=.0, max=.5)

runs = []
runs = runs + ['vise-constant-0.25a.csv']
#runs = runs + ['vise-constant-0.375a.csv']
runs = runs + ['vise-constant-0.5a.csv']
#runs = runs + ['vise-constant-0.625a.csv']
runs = runs + ['vise-constant-0.75a.csv']
#runs = runs + ['vise-constant-0.875a.csv']
runs = runs + ['vise-constant-1a.csv']
#runs = runs + ['vise-constant--1a.csv']

print(runs)


data = []
for run in runs:
    [time, refcurrent, current, Qr, Q] = np.loadtxt(run, delimiter=',', skiprows=1, unpack=True)
    data.append([time[:int(len(time)/3)], refcurrent[:int(len(time)/3)], Qr[:int(len(time)/3)]])

minner = Minimizer(energy, params, fcn_args=[data])
#result = minner.minimize(method='powell')
#report_fit(result)
#params=result.params

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.set_title("Pendulum parameters fitting")
ax1.set_xlabel('Time, sec')

energy(params, data)
for run in data:
    synthetic = predict(params, run[0], run[1])
    ax1.plot(run[0], run[2],   label='RW angle, rad')
    ax1.plot(run[0], synthetic, label='synthetic angle')

ax1.legend()
plt.show()

