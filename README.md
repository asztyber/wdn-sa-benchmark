# wdn-sa-benchmark
Tool for creating water distribution network examples for structural analysis diagnostic algorithms benchmarking

## Installation

```
pip3 install git+https://github.com/asztyber/wdn-sa-benchmark.git
```

Or for the development purposes:

```
git clone https://github.com/asztyber/wdn-sa-benchmark.git
cd wdn-sa-benchmark
pip3 install .
```

## Usage

### Minimal example

```
from wdn_sa_benchmark import EpanetConverter
#   INP file that will be converted to a structural model
input_file_name = 'networks/TLN.inp'

pressure_sensors = ['1', '2', '3']
flow_sensors = ['6']
leaks = ['1', '4', '6']
epn_conv = EpanetConverter(input_file_name, pressure_sensors=pressure_sensors, flow_sensors=flow_sensors,
                           leaks=leaks, sensor_faults=True)
epn_conv.structural_from_epanet()

print(epn_conv.model)
print()
print(epn_conv.eq_name_map)
print()
print(epn_conv.f_name_map)

epn_conv.save_files('output', 'TLN_simple')
```

### Documentation

Detailed documentation is in `EpanetConverter` docstrings:

```
from wdn_sa_benchmark import EpanetConverter

help(EpanetConverter)
```


### Examples

Library usage:
* `examples/convert.py` - convert an INP file to a structural model with a predefined set of parameters
* `examples/convert_random.py` - convert an INP file to a structural model with random placement of sensors and leaks
* `examples/network_preview.py` - prints basic network information and plots the network structural_from_epanet

Scripts that don't use the library, but utilize the assets and/or library output:
* `examples/fdt.py` - exemplary reading of structural model benchmark in Pyton and MSO and MTES sets calculation with
faultdiagnosistoolbox
* `examples/Matlab_examples`  - Matlab examples

## Assets

* `networks` - water network structures in .inp format (used as na input for conversion to structural model)

  Additionally L-TOWN network was provided in two versions: L-TOWN (original) and L-TOWN_simplified (skeletonized). The file L-TOWN_simplified_node_name_map.json provides a mapping from the nodes of the original network to the nodes of the simplified one.

* `structural_models` - structural models for the water networks. The naming convention is as follows:
[network name]\_[number of pressure sensors]\_[number of flow sensors]\_[number of leaks]
Structural model is saved in json format as a dictionary with fields:
  - model - dictionary with the equation names as keys and the sets of variables as values
  - unknown - list of unknown variables
  - known - list of known variables
  - faults - list of faults
  
 The naming convention of the model is as follows:
   - equations are labelled with letter _e_ and are sequentially numbered from 0,
   - flows are labelled with letter _q_ and a number; the number corresponds to pipe number in .inp file, i.e. _q1_ is flow in a pipe with id _1_,
   - pressures are labelled with letter _p_ and a number corresponding to the junction number in .inp file, i.e. _p1_ is pressure in a junction with id _1_,
   - faults are labelled with letter _f_ and are sequentially numbered from 0,
   - measurements are labelled with prefix _m_ and variable name.

 

* `measurements` - simulated measurements for L-TOWN network including leaks, faults and cyber attacks
  - .xlsx files contain measurements
  - .yaml files describe the configuration of leaks, faults and cyber attacks


## L-TOWN
 * https://zenodo.org/record/4017659 - the source of the L-TOWN.inp file
 * https://github.com/KIOS-Research/BattLeDIM - code from this repo was extended with the simulation of faults and cyber-attacks to provide measurement data for scenarios 1 and 2 