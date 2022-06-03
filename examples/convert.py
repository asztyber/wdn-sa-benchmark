import sys
sys.path.append('.')
from wdn_sa_benchmark import EpanetConverter

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
