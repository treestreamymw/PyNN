"""

Small network created with the Population and Projection classes

Andrew Davison, UNIC, CNRS
May 2006

$Id$

"""

import sys

simulator_name = sys.argv[-1]

exec("from pyNN.%s import *" % simulator_name)
from NeuroTools.stgen import StGen

# === Define parameters ========================================================

n = 10    # Number of cells
w = 0.2   # synaptic weight (nA)
cell_params = {
    'tau_m'      : 20.0, # (ms)
    'tau_syn_E'  : 2.0,  # (ms)
    'tau_syn_I'  : 4.0,  # (ms)
    'tau_refrac' : 2.0,  # (ms)
    'v_rest'     : 0.0,  # (mV)
    'v_init'     : 0.0,  # (mV)
    'v_reset'    : 0.0,  # (mV)
    'v_thresh'   : 20.0, # (mV)
    'cm'         : 0.5}  # (nF)
dt         = 0.1         # (ms)
syn_delay  = 1.0         # (ms)
input_rate = 50.0       # (Hz)
simtime    = 1000.0      # (ms)

# === Build the network ========================================================

setup(timestep=dt,max_delay=syn_delay)

cells = Population((n,), IF_curr_alpha, cell_params, "cells")

spikeGenerator = StGen()
spike_times = list(spikeGenerator.poisson_generator((input_rate/1000.0),simtime)) # rate in spikes/ms
spike_source = Population((n,), SpikeSourceArray,{'spike_times': spike_times})

cells.record()
cells.record_v()

input_conns = Projection(spike_source, cells, AllToAllConnector())
input_conns.setWeights(w)
input_conns.setDelays(syn_delay)

# === Run simulation ===========================================================

run(simtime)

cells.printSpikes("Results/small_network_%s.ras" % (simulator_name, ))
cells.print_v("Results/small_network_%s.v" % (simulator_name, ))

print "Mean firing rate: ", cells.meanSpikeCount()*1000.0/simtime, "Hz"

# === Clean up and quit ========================================================

end()
sys.exit(0)